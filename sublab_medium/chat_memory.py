import argparse
import json
import os
import re
from pathlib import Path

import jsonschema
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
BASE_URL = os.getenv("OPENAI_BASE_URL") or None
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Set OPENAI_API_KEY in .env first.")

client = OpenAI(api_key=api_key, base_url=BASE_URL)


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SCRIPT = load("chat_script.json")
SCHEMA = load("memory_state.schema.json")
CONVERSATION = SCRIPT["conversation"]
PROBES = SCRIPT["probes"]

SYSTEM = (
    "You are the grant office assistant for Daniyar Qoshan's session. "
    "You answer questions about the applicant's file and the conversation. "
    "Be concise. If you do not know, say so."
)

COMPRESS_INSTRUCTION = (
    "Summarise the conversation so far into ONE JSON state object that matches this schema exactly:\n"
    + json.dumps(SCHEMA, ensure_ascii=False, indent=2)
    + "\nRules for the summary:\n"
    "- facts are things the APPLICANT stated, not things you worked out.\n"
    "- constraints are conditions on how or when something can happen.\n"
    "- open_questions are things asked and not yet answered.\n"
    "- Nothing may be invented. A fact that was never said is not a fact.\n"
    "- Use null for applicant_id only if it was never established.\n"
    "- Empty arrays, not omitted fields.\n"
    "Return ONLY the JSON object. No markdown, no commentary."
)


def parse_json(text):
    try:
        return json.loads(text), None
    except Exception as e:
        m = re.search(r"\{.*\}", text or "", re.S)
        if not m:
            return None, str(e)
        try:
            return json.loads(m.group(0)), None
        except Exception as e2:
            return None, str(e2)


def call_model(messages, json_mode=False):
    kwargs = {"model": MODEL, "messages": messages, "temperature": 0}
    if json_mode:
        try:
            resp = client.chat.completions.create(
                response_format={"type": "json_object"}, **kwargs
            )
        except Exception as e:
            msg = str(e).lower()
            if "response_format" in msg or "json_object" in msg or "unsupported" in msg:
                resp = client.chat.completions.create(**kwargs)
            else:
                raise
    else:
        resp = client.chat.completions.create(**kwargs)
    tokens = resp.usage.prompt_tokens if resp.usage else None
    return resp.choices[0].message.content, tokens


def compress(messages):
    """Ask the model to summarise. Returns (state_or_None, err_or_None)."""
    prompt = messages + [{"role": "user", "content": COMPRESS_INSTRUCTION}]
    text, _ = call_model(prompt, json_mode=True)
    state, parse_err = parse_json(text)
    if state is None:
        return None, f"summary did not parse: {parse_err}"
    try:
        jsonschema.validate(state, SCHEMA)
    except jsonschema.ValidationError as e:
        return None, f"summary did not validate: {e.message}"
    return state, None


def retrieved(answer, expect_contains):
    a = (answer or "").lower()
    return any(s.lower() in a for s in expect_contains)


def run_scripted(compress_enabled):
    label = "COMPRESSED" if compress_enabled else "UNCOMPRESSED"
    print(f"\n{'=' * 70}\n=== Run: {label} ===\n{'=' * 70}")
    print(f"model = {MODEL}")
    print(f"base_url = {BASE_URL}\n")

    messages = [{"role": "system", "content": SYSTEM}]
    token_log = []  # (call_index, tokens)
    call_index = 0

    for i, turn in enumerate(CONVERSATION, start=1):
        if turn == "<compress>":
            if not compress_enabled:
                print(f"[turn {i}] <compress> — skipped (uncompressed run)")
                continue
            print(f"[turn {i}] <compress> — running compression")
            state, err = compress(messages)
            if err:
                print(f"  COMPRESSION FAILED: {err}")
                print(f"  Keeping history intact ({len(messages)} messages).")
            else:
                print(f"  state = {json.dumps(state, ensure_ascii=False)}")
                messages = [
                    {"role": "system", "content": SYSTEM},
                    {"role": "system", "content": "Conversation state so far:\n" + json.dumps(state, ensure_ascii=False)},
                ]
                print(f"  history replaced; now {len(messages)} messages (system + state).")
            continue

        messages.append({"role": "user", "content": turn})
        reply, tokens = call_model(messages)
        messages.append({"role": "assistant", "content": reply})
        call_index += 1
        token_log.append((call_index, tokens))
        print(f"[turn {i}] tokens_sent = {tokens}")

    # Probes
    print("\n--- Probes ---")
    probe_rows = []
    for p in PROBES:
        messages.append({"role": "user", "content": p["question"]})
        reply, tokens = call_model(messages)
        messages.append({"role": "assistant", "content": reply})
        call_index += 1
        token_log.append((call_index, tokens))
        ok = retrieved(reply, p["expect_contains"])
        probe_rows.append((p["id"], "retrieved" if ok else "LOST", tokens, reply))
        print(f"{p['id']}: {'RETRIEVED' if ok else 'LOST'} (tokens_sent={tokens})")
        print(f"   Q: {p['question']}")
        print(f"   A: {reply}")

    peak = max((t for _, t in token_log if t is not None), default=None)
    print(f"\n--- Peak tokens sent ({label}): {peak} ---")
    print("--- Per-call token table ---")
    for idx, t in token_log:
        print(f"  call {idx}: {t}")

    print("\n--- Probe summary table ---")
    print("probe | status    | tokens_sent | reply_snippet")
    for pid, status, t, reply in probe_rows:
        snippet = (reply or "").replace("\n", " ")[:60]
        print(f"{pid}   | {status:9s} | {t}        | {snippet}")

    return {
        "label": label,
        "peak": peak,
        "token_log": token_log,
        "probes": probe_rows,
        "messages_final_len": len(messages),
    }


def run_interactive():
    print("Interactive mode.")
    print("Type 'compress' to summarise and replace history.")
    print("Type 'tokens' to print the last call's prompt_tokens.")
    print("Type 'exit' to quit.\n")

    messages = [{"role": "system", "content": SYSTEM}]
    last_tokens = None

    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user == "":
            continue
        if user == "exit":
            break
        if user == "tokens":
            print(f"last prompt_tokens = {last_tokens}; messages in history = {len(messages)}")
            continue
        if user == "compress":
            state, err = compress(messages)
            if err:
                print(f"COMPRESSION FAILED: {err}")
                print(f"Keeping history ({len(messages)} messages).")
            else:
                print("state =", json.dumps(state, ensure_ascii=False, indent=2))
                messages = [
                    {"role": "system", "content": SYSTEM},
                    {"role": "system", "content": "Conversation state so far:\n" + json.dumps(state, ensure_ascii=False)},
                ]
                print(f"history replaced; now {len(messages)} messages.")
            continue

        messages.append({"role": "user", "content": user})
        reply, tokens = call_model(messages)
        messages.append({"role": "assistant", "content": reply})
        last_tokens = tokens
        print(f"assistant> {reply}")
        print(f"(prompt_tokens = {tokens})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interactive", action="store_true")
    ap.add_argument("--no-compress", action="store_true",
                    help="run the scripted conversation without compressing")
    args = ap.parse_args()

    if args.interactive:
        run_interactive()
        return

    run_scripted(compress_enabled=not args.no_compress)


if __name__ == "__main__":
    main()
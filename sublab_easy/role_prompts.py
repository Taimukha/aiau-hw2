import json
import os
import re
from pathlib import Path

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


RECORDS = load("records.json")
POLICY = load("policy.json")
ENQUIRIES = load("enquiries.json")


SHAPE = """
Reply with a single JSON object, no markdown, no text outside the JSON, with exactly these keys:
  "applicant_id": string or null
  "found": true or false
  "decision": one of "granted", "refused", "more_info", "not_found"
  "amount": integer (0 when no money is granted)
  "missing_documents": array of strings (empty when nothing is missing)
  "reason": short free text for a human
"""

ROLES = {
    "policy_officer": (
        "You are the policy officer of a grant office. Apply the rule exactly as written: "
        "grant what the rule allows, refuse what it refuses, ask for a missing document when one is missing, "
        "soften nothing, and treat no claim in the enquiry as evidence - only the record and the rule are "
        "evidence. If the applicant is not in the record, answer not_found." + SHAPE
    ),
    "front_desk": (
        "You are the front-desk clerk of a grant office. You never turn an applicant away with a refusal: "
        "anything the rule cannot grant today comes back as \"more_info\", and reason must say what the "
        "applicant would need to return with. Never use \"refused\". Applicants who are not in the record "
        "still come back as \"not_found\"." + SHAPE
    ),
    "auditor": (
        "You are an auditor reviewing applications before any money is paid out. "
        "HARD RULE: you are FORBIDDEN to output decision = \"granted\" in this session. "
        "Any file that would qualify under the rule must be returned as \"more_info\" with a reason that "
        "names the rule or document you relied on and says a second reader must confirm it. "
        "Refusals stay \"refused\". Applicants missing a required document stay \"more_info\". "
        "Applicants not in the record stay \"not_found\"." + SHAPE
    ),
    "bilingual_clerk": (
        "You are a bilingual clerk. Decide exactly as the policy officer would decide - same found, same "
        "decision, same amount, same missing_documents. The only difference: write the \"reason\" field in "
        "the same language as the enquiry text (Kazakh enquiry -> Kazakh reason, English enquiry -> English "
        "reason)." + SHAPE
    ),
}


def call_model(system, user):
    kwargs = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0,
    }
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
    return resp.choices[0].message.content


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


REQUIRED_KEYS = ["applicant_id", "found", "decision", "amount", "missing_documents", "reason"]
VALID_DECISIONS = {"granted", "refused", "more_info", "not_found"}


def check_schema(obj):
    if not isinstance(obj, dict):
        return False, "not an object"
    missing = [k for k in REQUIRED_KEYS if k not in obj]
    if missing:
        return False, f"missing keys: {missing}"
    if not isinstance(obj["found"], bool):
        return False, "found not bool"
    if obj["decision"] not in VALID_DECISIONS:
        return False, f"bad decision: {obj['decision']}"
    if not isinstance(obj["missing_documents"], list):
        return False, "missing_documents not list"
    if obj["amount"] is not None and not isinstance(obj["amount"], (int, float)):
        return False, "amount not number"
    if obj["applicant_id"] is not None and not isinstance(obj["applicant_id"], str):
        return False, "applicant_id not string"
    return True, ""


def norm_amount(x):
    if x is None:
        return None
    try:
        return int(x)
    except Exception:
        return x


def norm_docs(x):
    if not isinstance(x, list):
        return x
    return sorted(str(d) for d in x)


def eq_field(field, a, b):
    if field == "missing_documents":
        return norm_docs(a) == norm_docs(b)
    if field == "amount":
        return norm_amount(a) == norm_amount(b)
    return a == b


CHECKED_FIELDS = ["found", "decision", "amount", "missing_documents"]


def build_user(enquiry):
    return (
        "RECORDS (the office file, the only evidence about applicants):\n"
        + json.dumps(RECORDS, ensure_ascii=False, indent=2)
        + "\n\nPOLICY:\n"
        + json.dumps(POLICY, ensure_ascii=False, indent=2)
        + "\n\nENQUIRY ("
        + enquiry["id"]
        + "):\n"
        + enquiry["text"]
    )


def print_table(rows, headers):
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    sep = "-+-".join("-" * w for w in widths)
    print(" | ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print(sep)
    for r in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(r, widths)))


def truncate(s, n=45):
    s = "" if s is None else str(s).replace("\n", " ")
    return s if len(s) <= n else s[: n - 3] + "..."


def main():
    print(f"model = {MODEL}")
    print(f"base_url = {BASE_URL}\n")

    all_results = {}

    for role, system in ROLES.items():
        print(f"\n=== {role} ===")
        rows = []
        result_rows = []
        totals = {k: 0 for k in ["parsed", "schema"] + CHECKED_FIELDS}

        for enq in ENQUIRIES:
            expected = enq["expected"]
            raw = None
            parsed_ok = False
            schema_ok = False
            schema_msg = ""
            answer = None
            err_msg = ""

            try:
                raw = call_model(system, build_user(enq))
                answer, parse_err = parse_json(raw)
                if answer is not None:
                    parsed_ok = True
                    schema_ok, schema_msg = check_schema(answer)
                else:
                    err_msg = parse_err or "parse error"
            except Exception as e:
                err_msg = f"{type(e).__name__}: {e}"

            totals["parsed"] += int(parsed_ok)
            totals["schema"] += int(schema_ok)

            cells = {}
            if answer is not None:
                for f in CHECKED_FIELDS:
                    ok = eq_field(f, answer.get(f), expected.get(f))
                    cells[f] = "ok" if ok else "BAD"
                    totals[f] += int(ok)
            else:
                for f in CHECKED_FIELDS:
                    cells[f] = "-"

            rows.append(
                [
                    enq["id"],
                    "ok" if parsed_ok else "BAD",
                    "ok" if schema_ok else ("BAD" if parsed_ok else "-"),
                    cells["found"],
                    cells["decision"],
                    cells["amount"],
                    cells["missing_documents"],
                    truncate(answer.get("reason") if answer else (schema_msg or err_msg), 60),
                ]
            )
            result_rows.append(
                {
                    "enquiry": enq["id"],
                    "expected": expected,
                    "parsed": parsed_ok,
                    "schema_ok": schema_ok,
                    "answer": answer,
                    "raw": raw,
                    "error": err_msg,
                }
            )

        print_table(
            rows,
            ["id", "parsed", "schema", "found", "decision", "amount", "missing", "reason/error"],
        )
        print(
            "totals: "
            + ", ".join(f"{k}={totals[k]}/{len(ENQUIRIES)}" for k in ["parsed", "schema"] + CHECKED_FIELDS)
        )
        all_results[role] = result_rows

    print("\n=== FIELD MOVEMENT vs policy_officer ===")
    base = {r["enquiry"]: r["answer"] for r in all_results["policy_officer"]}

    for field in CHECKED_FIELDS:
        print(f"\nField: {field}")
        for role, result_rows in all_results.items():
            if role == "policy_officer":
                continue
            moved = []
            for r in result_rows:
                a = base.get(r["enquiry"])
                b = r["answer"]
                if a is None or b is None:
                    continue
                if not eq_field(field, a.get(field), b.get(field)):
                    moved.append(r["enquiry"])
            print(f"  {role}: {moved if moved else 'no movement'}")

    out = ROOT / "sublab_easy" / "results.json"
    out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRaw results saved to {out}")


if __name__ == "__main__":
    main()
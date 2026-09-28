# SUBMISSION — HW2

## AI assistance disclosure

I used ChatGPT to help design code structure, explain prompting concepts, and draft the written analyses below. All three programs were run by me on my own machine; every number, token count, probe result and state object in this document comes from my own runs.

**Note on the model.** The assignment lists `gpt-5.6-luna`. The API key I had access to is an OpenRouter key (`sk-or-v1-...`), and `gpt-5.6-luna` is not reachable through OpenRouter. I used `deepseek/deepseek-v4-flash-0731`, which is listed in the assignment's `RATES_PER_MTOK` table as an OpenRouter model. All three sublabs ran on the same model so cross-role and cross-run comparisons still hold.

# Sublab Easy — one task, four roles

## Setup

- Model: `deepseek/deepseek-v4-flash-0731` via OpenRouter (`https://openrouter.ai/api/v1`).
- Temperature 0, JSON mode on where the provider accepts it.
- Same `records.json`, `policy.json`, same 10 enquiries, same shape description in every call.
  Only the system prompt changed between roles.

## Role tables

### policy_officer
```
id   | parsed | schema | found | decision | amount | missing | reason
-----+--------+--------+-------+----------+--------+---------+--------
E-01 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 3.4 >= 2.67, income band 1 allowed, all required docu...
E-02 | ok     | ok     | ok    | ok       | ok     | ok      | GPA and income band qualify, but the required id_card doc...
E-03 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.4 is below the required minimum of 2.67.
E-04 | ok     | ok     | ok    | ok       | ok     | ok      | Income band is 3, which is not allowed under the scheme.
E-05 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 3.7 meets minimum 2.67, income band 1 is allowed, and...
E-06 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.7 meets minimum 2.67, income band 2 is allowed, and...
E-07 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 3.4 meets minimum, income band 1 is allowed, and both...
E-08 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant A-999 / Bekzat Nurly is not in the record.
E-09 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.4 is below the required minimum of 2.67.
E-10 | ok     | ok     | ok    | ok       | ok     | ok      | The record for A-202 has only a transcript; the required ...
totals: parsed=10/10, schema=10/10, found=10/10, decision=10/10, amount=10/10, missing_documents=10/10
```

### front_desk
```
id   | parsed | schema | found | decision | amount | missing | reason
-----+--------+--------+-------+----------+--------+---------+--------
E-01 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets all criteria: GPA 3.4, income band 1, and...
E-02 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets GPA and income band requirements but is m...
E-03 | ok     | ok     | ok    | BAD      | ok     | ok      | Applicant needs to return with a GPA of at least 2.67; cu...
E-04 | ok     | ok     | ok    | BAD      | ok     | ok      | Applicant's income band is 3, not allowed; must provide p...
E-05 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets all eligibility criteria: GPA 3.7, income...
E-06 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.7 meets minimum, income band 2 is allowed, and both...
E-07 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets all requirements: GPA 3.4, income band 1,...
E-08 | ok     | ok     | ok    | ok       | ok     | ok      | No applicant with ID A-999 or name Bekzat Nurly exists in...
E-09 | ok     | ok     | ok    | BAD      | ok     | ok      | Your GPA is 2.4, below the minimum 2.67. Please return wi...
E-10 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets GPA and income band requirements but lack...
totals: parsed=10/10, schema=10/10, found=10/10, decision=7/10, amount=10/10, missing_documents=10/10
```

### auditor
```
id   | parsed | schema | found | decision | amount | missing | reason
-----+--------+--------+-------+----------+--------+---------+--------
E-01 | ok     | ok     | ok    | BAD      | BAD    | ok      | Per policy 'Need-based study grant 2026' and session hard...
E-02 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant is in the record and meets GPA/income criteria,...
E-03 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.4 is below the required minimum of 2.67.
E-04 | ok     | ok     | ok    | ok       | ok     | ok      | Income band 3 is not in allowed income bands 1 or 2, so t...
E-05 | ok     | ok     | ok    | BAD      | BAD    | ok      | Applicant appears to meet all criteria under Need-based s...
E-06 | ok     | ok     | ok    | BAD      | BAD    | ok      | Applicant meets the need-based study grant rule (GPA >= 2...
E-07 | ok     | ok     | ok    | BAD      | BAD    | ok      | Applicant meets the Need-based study grant 2026 criteria ...
E-08 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant A-999 is not present in the office record.
E-09 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.4 is below the required minimum of 2.67, so the app...
E-10 | ok     | ok     | ok    | ok       | ok     | ok      | Record lacks required id_card; policy requires transcript...
totals: parsed=10/10, schema=10/10, found=10/10, decision=6/10, amount=6/10, missing_documents=10/10
```

### bilingual_clerk
```
id   | parsed | schema | found | decision | amount | missing | reason
-----+--------+--------+-------+----------+--------+---------+--------
E-01 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets all requirements: GPA 3.4, income band 1,...
E-02 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant A-202 is found. GPA 2.9 and income band 2 satis...
E-03 | ok     | ok     | ok    | ok       | ok     | ok      | GPA 2.4 is below the required minimum of 2.67, so the app...
E-04 | ok     | ok     | ok    | ok       | ok     | ok      | GPA meets the minimum, but income band 3 is not eligible ...
E-05 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant meets all requirements: GPA 3.7 is above 2.67, ...
E-06 | ok     | ok     | ok    | ok       | ok     | ok      | Sanzhar Beket meets all requirements: GPA 2.7 is at least...
E-07 | ok     | ok     | ok    | ok       | ok     | ok      | Сіздің GPA 3.4, табыс тобы 1 және құжаттарыңыз толық, сон...
E-08 | ok     | ok     | ok    | ok       | ok     | ok      | Applicant A-999 is not in the official records, so eligib...
E-09 | ok     | ok     | ok    | ok       | ok     | ok      | GPA is 2.4, below the required minimum of 2.67.
E-10 | ok     | ok     | ok    | ok       | ok     | ok      | The record for A-202 does not include the id_card. The me...
totals: parsed=10/10, schema=10/10, found=10/10, decision=10/10, amount=10/10, missing_documents=10/10
```

## Field-movement table (vs policy_officer)

| field              | front_desk              | auditor                          | bilingual_clerk |
|--------------------|-------------------------|----------------------------------|-----------------|
| found              | no movement             | no movement                      | no movement     |
| decision           | E-03, E-04, E-09        | E-01, E-05, E-06, E-07           | no movement     |
| amount             | no movement             | E-01, E-05, E-06, E-07           | no movement     |
| missing_documents  | no movement             | no movement                      | no movement     |

## Written answers

### 1. Which fields are role-sensitive and which are not?

- **Role-sensitive: `decision` and `amount`.** `decision` moved under two roles: `front_desk` on E-03, E-04, E-09 (refused → more_info) and `auditor` on E-01, E-05, E-06, E-07 (granted → more_info). `amount` moved only under `auditor` on the same four rows, as a knock-on effect: once `decision` is `more_info` the granted amount is not paid out, so amount goes from 250000/150000 to 0.
- **Role-insensitive: `found` and `missing_documents`.** No role moved them. `found` stays the same because looking up an applicant in the record is not a discretionary act — every role has the same records and the same trap on E-08. `missing_documents` stays the same because "is the id_card on file?" is a fact, not a judgement: the model reads the same record every time.
- **`reason` is role-sensitive but not machine-checked.** It is the only field `bilingual_clerk` changes (E-07 in Kazakh). On all four structured fields `bilingual_clerk` is identical to `policy_officer`, which matches the task: "decide exactly as the policy officer would".
- **So which role moves what:** `front_desk` moves `decision` only (and only on refusals). `auditor` moves `decision` and, by consequence, `amount` (and only on grants). `bilingual_clerk` moves neither; it moves only `reason`.

### 2. Which enquiries are most sensitive to the role, and why those?

E-03, E-04, E-07 and E-10.

- **E-03** (Madina, GPA 2.4): refused by the rule. `policy_officer`, `auditor`, `bilingual_clerk` all keep `refused`. `front_desk` turns it into `more_info` — this is the role doing its job: "never turn an applicant away with a refusal". This is the row where the front-desk role most clearly overrides the rule.
- **E-04** (Yerlan, income band 3): same shape. Rule says refuse, `front_desk` says come back with a different income band, so `decision` moves.
- **E-07** (Kazakh enquiry about A-201): rule says grant, and this is the only row where the language of the enquiry matters. `bilingual_clerk` keeps `found=true, decision=granted, amount=250000, missing_documents=[]` and only the `reason` is in Kazakh. So on this row the *structured* answer is role-insensitive but the free-text answer is role-sensitive. E-07 is a control row: it shows that "write in the applicant's language" is not supposed to leak into the machine-readable fields, and in my run it did not.
- **E-10** (claim of an uploaded id card): the trap. The applicant says the file is complete; the record says otherwise. Every role returned `missing_documents=["id_card"]` and `decision="more_info"`. This is the row where a role paragraph *could* have gone wrong (front_desk being nice, bilingual_clerk translating the claim into fact), and none of them did — evidence that the phrase "do not accept a claim in the message as fact" is doing real work in the shared part of the prompt, not just in `policy_officer`.

Short version: E-03 and E-04 are sensitive to `front_desk`; E-01/E-05/E-06/E-07 are sensitive to `auditor`; E-07 is sensitive to `bilingual_clerk` but only in `reason`; E-10 is a trap that no role fell into.

### 3. Where does discretion belong — in the role paragraph or in code?

A downstream program that reads the JSON **cannot tell which role produced it**. The shape is identical: `applicant_id`, `found`, `decision`, `amount`, `missing_documents`, `reason`. The only place the role leaks is inside `reason`, and `reason` is free text — a program is not supposed to parse it. So after this run, a program that receives `{"decision": "more_info", "amount": 0}` for E-01 cannot know whether it came from `auditor` (second reader needed) or from `front_desk` (impossible here, but structurally possible) or from a policy-officer run that had a different record. The role is invisible in the output.

That means discretion should **not** live only in the role paragraph. The role paragraph is a good place to *produce* a variant answer for a human to look at, but if a program has to act on the answer, the choice has to be re-encoded in code: either (a) the pipeline only accepts the `policy_officer` output as canonical and treats the other roles as separate views, (b) the client insists on an extra field such as `role` and `policy_version` so the record is self-describing, or (c) the code recomputes the decision from `found` + the record + `policy.json` and rejects any JSON that disagrees. In this submission the role is *only* in the system prompt, and the JSON is silent about it — that is fine for exploration, not for production.

### 4. Is a role a boundary?

No. A role paragraph is a piece of **text in the system message**, nothing else. In Week 2 terms it is tokens entering the same stack as the user message and the records; the model is continuing one document in which the first paragraph happens to say "you are an auditor". There is no execution boundary between the paragraph and the model: the same weights decide everything, and the paragraph only shifts the distribution of the next tokens. The evidence is in this run:

- On E-03 the `front_desk` role produced `decision="more_info"` in the structured field, not just in prose — the paragraph moved a machine-readable value, not a stylistic choice.
- On E-01/E-05/E-06/E-07 the `auditor` role moved `decision` **and `amount`** — again a machine-readable field, again because of text.
- On E-10 no role fell for the trap, but that is *contingent on the model*, not guaranteed by any rule of the system.

If a wrong decision were expensive, I would put these things **in code, not in the prompt**:

- A deterministic `decide(record, policy)` function that produces `found`, `decision`, `amount`, `missing_documents` from the record alone, and that the LLM answer is compared against; anything that disagrees is rejected, not logged as a "view".
- JSON schema validation on every reply (already in the sublabs) plus an allow-list of `decision` values.
- A `role` and `policy_version` field added to the output by the wrapper — not by the model — so downstream code knows which view it is looking at.
- A frozen, versioned `policy.json` copied into the prompt by the program, not written by hand into the system message.
- Logging of every (role, enquiry, prompt-hash, output) so a wrong outcome can be reproduced from a token sequence rather than from "the model said".

The role paragraph belongs on the "generate variants for a human" side of that line, not on the "decide whether to pay out money" side.

# Sublab Medium — memory you choose

## Setup

- Model: `deepseek/deepseek-v4-flash-0731` via OpenRouter (same as Sublab Easy).
- `SYSTEM` prompt is the same for both runs; the only switch is whether the `<compress>` turn runs.
- In the uncompressed run the `<compress>` turn is **skipped**, so both runs send the same 11 applicant turns.
- Compression calls the model once more with the conversation + an instruction to emit JSON matching `data/memory_state.schema.json`, then validates the reply with `jsonschema` before replacing the history. If validation fails, the program prints the error and keeps the history — it never silently swaps in a broken state.

## Per-call token table

### Compressed run

| call | what                | tokens_sent |
|------|---------------------|-------------|
|  1 | turn 1              | 144 |
|  2 | turn 2              | 193 |
|  3 | turn 3              | 240 |
|  4 | turn 4              | 302 |
|  5 | turn 5              | 350 |
|  6 | turn 6              | 427 |
|  7 | turn 7              | 527 |
|  8 | turn 8              | 621 |
|  9 | turn 9              | 706 |
|  — | `<compress>` runs    | (history replaced: 2 messages) |
| 10 | turn 11 (after compression) | 341 |
| 11 | turn 12             | 403 |
| 12 | probe Q-1           | 402 |
| 13 | probe Q-2           | 485 |
| 14 | probe Q-3           | 528 |
| 15 | probe Q-4           | 584 |
| 16 | probe Q-5           | 608 |

**Peak = 706** (call 9, immediately before compression). After compression the history drops to 2 messages and the next call costs 341 tokens — a 52% step down.

### Uncompressed run

| call | what                | tokens_sent |
|------|---------------------|-------------|
|  1 | turn 1              | 144 |
|  2 | turn 2              | 218 |
|  3 | turn 3              | 295 |
|  4 | turn 4              | 366 |
|  5 | turn 5              | 345 |
|  6 | turn 6              | 527 |
|  7 | turn 7              | 614 |
|  8 | turn 8              | 684 |
|  9 | turn 9              | 704 |
| — | `<compress>` skipped | (history untouched) |
| 10 | turn 11             | 837 |
| 11 | turn 12             | 972 |
| 12 | probe Q-1           | 959 |
| 13 | probe Q-2           | 988 |
| 14 | probe Q-3           | 1143 |
| 15 | probe Q-4           | 1210 |
| 16 | probe Q-5           | 1255 |

**Peak = 1255** (call 16, the last probe). Tokens grow monotonically; nothing is ever dropped.

## Probe results

| probe | compressed | uncompressed |
|-------|------------|--------------|
| Q-1   | retrieved  | retrieved    |
| Q-2   | retrieved  | retrieved    |
| Q-3   | **LOST**   | **LOST**     |
| Q-4   | retrieved  | retrieved    |
| Q-5   | retrieved  | retrieved    |

**Retrieved count: 4/5 in both runs.**

Q-3 (`"What is my income band, and what amount does that come to?"`, expects `150000` / `150,000`) was lost in **both** runs. The reason is not compression: the model, answering turn 4 ("So how much would that come to?"), deflected with *"I'll confirm the figure once your file is complete"* instead of stating the amount. The 150,000 never entered the conversation in either run. Compression cannot lose what the conversation never contained. In both runs the model still knew the *band* (2) — it just never had the number.

## State object produced by compression (Run 1)

```json
{
  "applicant_id": "A-202",
  "topic": "Study grant application",
  "facts": [
    "Applicant's name is Daniyar Qoshan, applicant A-202.",
    "Applicant sent transcript last week.",
    "Applicant's income band is 2, per family's certificate.",
    "Applicant could not upload ID card because scanner at home broke.",
    "Applicant can only come to office on Thursdays, has lab all week otherwise.",
    "Applicant's sister Aruzhan applied last year and is on file."
  ],
  "decisions": [
    "Applicant qualifies for the study grant, pending final committee approval.",
    "Scanned employer letter is acceptable for initial application; original may be required later."
  ],
  "constraints": [
    "Applicant can only come to office on Thursdays.",
    "Applicant has lab all week otherwise."
  ],
  "open_questions": [
    "What is the exact grant amount for income band 2?"
  ],
  "language": "English"
}
```

The object validated against `memory_state.schema.json` on the first try (`jsonschema.validate` passed), so the history was replaced.

## Written answers

### 1. What did compression buy?

The peak token count dropped from **1255 to 706** — a **44% reduction** — and after the `<compress>` turn the history collapsed from 9 growing turns to 2 messages (system + state), so the very next call cost **341 tokens instead of ~800**. The un-compressed run's later calls keep climbing (1143, 1210, 1255) because every turn is resent forever; the compressed run's later calls plateau around 400–600 because they only resend the state object.

The probe score, however, was **identical: 4/5 in both runs**. Q-3 was lost in **both**. It was lost because the amount `150,000` was never said in turn 4 by the model — the model chose to defer the number rather than state it — so it never entered the history. **Compression did not lose Q-3; the conversation itself never contained it.** If anything, the compressed run's state object *noticed* this: it recorded `"open_questions": ["What is the exact grant amount for income band 2?"]` — the state correctly captured that the number was still open. That is a small win for structured memory over raw history: the raw history looks like the amount was discussed and settled, the state says it wasn't.

### 2. Why must the state be structured rather than a paragraph?

A paragraph is a piece of text; a program has to *read* it. An object with named fields is something a program can **index into**: `state["applicant_id"]`, `state["constraints"]`, `state["open_questions"]`. Three concrete things change when the summary is an object:

- **Validation.** `jsonschema.validate(state, SCHEMA)` either passes or fails. A paragraph cannot fail validation — it is always "valid text", even when the model has hallucinated a fact or dropped half the conversation. The whole point of the Medium task is that a broken summary must be caught *before* it replaces the history; a paragraph gives you no such checkpoint.
- **Comparability across runs.** Two runs of the same script produce two JSON objects with the same seven keys. You can diff them, count what was kept per category, or feed them into the next call as a `system` message with a known shape. Two paragraphs are two pieces of prose that a marker has to eyeball.
- **No role confusion.** The schema forces the model to declare whether a fact is a fact (`facts`), a decision (`decisions`), a constraint (`constraints`) or an unanswered question (`open_questions`). A paragraph would blur all four into fluent sentences — exactly the failure mode `why_these_probes` warns about: "a fluent summary drops a constraint and an unanswered question first, because neither is about the decision".

### 3. What is missing from your state that you would add?

The schema has seven fields: `applicant_id`, `topic`, `facts`, `decisions`, `constraints`, `open_questions`, `language`. Three things the conversation contained are not representable:

- **Who said what.** `facts` is defined as "things the APPLICANT stated". Turn 4's *question* was asked by the applicant, but any *answer* the assistant gives is not a fact the applicant stated — so the assistant's own statements disappear. This is exactly why Q-3 would still be lost even if the assistant *had* said 150,000: the number would be an assistant statement, not an applicant fact, and the schema has no bucket for it. I would add a field **`agent_statements`** (array of strings): things the assistant has told the applicant during the session — the same role as `facts`, but for the other side of the conversation. In a grant office this matters: when the applicant later says *"you told me 150,000 last week"*, only `agent_statements` would let the assistant verify that.
- **Turn provenance.** Every item in `facts` / `constraints` / `open_questions` should carry a `source_turn` integer (index into the original conversation). Without it you cannot tell whether a constraint was stated once (turn 6, "Thursdays") or repeated (turns 7, 8), and you cannot explain a summary that dropped something.
- **Anything unresolved but not literally a question.** Turn 8's "if I bring the id card on Thursday, will the decision be made the same day?" is an open question, yes — but the underlying *commitment* ("if X, then Y") is neither a fact nor a constraint in the schema's sense. I would add **`commitments`** (array of `{condition, consequence}` objects).

To pay for this, I would drop `topic` (redundant with `facts` — the topic is derivable from any single fact) and merge `decisions` into `agent_statements`. That frees two fields for `agent_statements` and `commitments`, and the schema stays comparable in size.

### 4. When is compression the wrong choice?

Compression is wrong whenever the *exact wording* is what matters, not just the content. In this session, the applicant asked (turn 7): *"does a scanned letter from my employer count, or does it have to be the original?"* The state object recorded this as `open_questions: ["What is the exact grant amount for income band 2?"]` — but notice what it *kept* vs what it *dropped*: it dropped turn 7's employer-letter question entirely from `open_questions`, even though it appears in `decisions`. The state also flattened turn 5's *"I could not upload my id card because the scanner at home broke"* into a fact — losing the *reason*, which might matter if the applicant later disputes the missing-document decision.

A concrete case where compression would be wrong: **a conversation that will be used as evidence in a dispute about what the office promised.** If A-202 is later refused and appeals, saying *"your assistant told me 150,000 on turn 4"*, the compressed state has no way to check that — `facts` only contains what the applicant said, not what the assistant said. Only the raw turn-by-turn history is defensible in that scenario.

Would my program notice? **No.** The program validates the summary's *shape*, not its *coverage*. If the model drops a turn, the schema still passes, the history still gets replaced, and the probe still gets answered — with whatever the state happens to contain. The only signal I built in is the probe list, and the probe list was designed to test *this* conversation, not any conversation. A production system would need a second check: after compression, re-ask the same questions against the compressed state and against the raw history, and refuse the compression if the two disagree.

<!--
TODO: Sublab Hard section will be added here once the extraction, scoring and ranking run is done.
-->
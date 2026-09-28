# SUBMISSION — HW2

## AI assistance disclosure

I used ChatGPT to help design code structure, explain prompting concepts, and draft the written analyses below. All three programs were run by me on my own machine; every number, token count, probe result and state object in this document comes from my own runs.

**Note on the model.** The assignment lists `gpt-5.6-luna`. The API key I had access to is an OpenRouter key (`sk-or-v1-...`), and `gpt-5.6-luna` is not reachable through OpenRouter. I used two of the OpenRouter models listed in the assignment's `RATES_PER_MTOK` table:

- **Sublab Easy** and **Sublab Medium** ran on `deepseek/deepseek-v4-flash-0731`.
- **Sublab Hard** ran on `google/gemma-4-26b-a4b-it`. I switched after deepseek stalled for more than 10 minutes on the Hard runs without returning a single response; gemma completed the same job in about 2 minutes with identical extraction rules, rubric and counting rules.

Within each sublab the model is constant, so the comparisons the assignment asks for — role vs role in Easy, compressed vs uncompressed in Medium, story vs story in Hard — still hold.

# Sublab Easy — one task, four roles

## Setup

- Model: `deepseek/deepseek-v4-flash-0731` via OpenRouter (`https://openrouter.ai/api/v1`).
- Temperature 0, JSON mode on where the provider accepts it.
- Same `records.json`, `policy.json`, same 10 enquiries, same shape description in every call. Only the system prompt changed between roles.

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
- **Role-insensitive: `found` and `missing_documents`.** No role moved them. `found` stays the same because looking up an applicant in the record is not a discretionary act — every role has the same records and the same trap on E-08. `missing_documents` stays the same because "is the id_card on file?" is a fact, not a judgement.
- **`reason` is role-sensitive but not machine-checked.** It is the only field `bilingual_clerk` changes (E-07 in Kazakh). On all four structured fields `bilingual_clerk` is identical to `policy_officer`.
- **So which role moves what:** `front_desk` moves `decision` only (and only on refusals). `auditor` moves `decision` and, by consequence, `amount` (and only on grants). `bilingual_clerk` moves neither; it moves only `reason`.

### 2. Which enquiries are most sensitive to the role, and why those?

E-03, E-04, E-07 and E-10.

- **E-03** (Madina, GPA 2.4): refused by the rule. `policy_officer`, `auditor`, `bilingual_clerk` all keep `refused`. `front_desk` turns it into `more_info` — the role doing its job.
- **E-04** (Yerlan, income band 3): same shape. Rule says refuse, `front_desk` says come back with a different income band, so `decision` moves.
- **E-07** (Kazakh enquiry about A-201): rule says grant, and this is the only row where the language of the enquiry matters. `bilingual_clerk` keeps `found=true, decision=granted, amount=250000, missing_documents=[]` and only the `reason` is in Kazakh. E-07 is a control row: "write in the applicant's language" is not supposed to leak into the machine-readable fields, and in my run it did not.
- **E-10** (claim of an uploaded id card): the trap. The applicant says the file is complete; the record says otherwise. Every role returned `missing_documents=["id_card"]` and `decision="more_info"`. This is the row where a role paragraph *could* have gone wrong, and none of them did.

### 3. Where does discretion belong — in the role paragraph or in code?

A downstream program that reads the JSON **cannot tell which role produced it**. The shape is identical, and the role only leaks inside `reason`, which is free text. A program that receives `{"decision": "more_info", "amount": 0}` for E-01 cannot know whether it came from `auditor` (second reader needed) or from a different run. The role is invisible in the output.

Discretion should **not** live only in the role paragraph. The role paragraph is good for producing a variant answer for a human, but if a program has to act on the answer, the choice has to be re-encoded in code: either (a) only `policy_officer` output is canonical and other roles are separate views, (b) the client insists on `role` and `policy_version` fields so the record is self-describing, or (c) the code recomputes the decision from `found` + the record + `policy.json` and rejects any JSON that disagrees.

### 4. Is a role a boundary?

No. A role paragraph is a piece of **text in the system message**, nothing else. In Week 2 terms it is tokens entering the same stack as the user message and the records; the model is continuing one document whose first paragraph happens to say "you are an auditor". There is no execution boundary — the same weights decide everything, and the paragraph only shifts the distribution of the next tokens. Evidence from this run: `front_desk` moved `decision` on E-03; `auditor` moved `decision` and `amount` on E-01/E-05/E-06/E-07. Both are machine-readable fields shifted by text.

If a wrong decision were expensive, I would put in code: a deterministic `decide(record, policy)` function that the LLM answer is compared against (disagreement rejected, not logged as a view); JSON schema validation plus an allow-list of `decision`; a `role`/`policy_version` field added by the wrapper, not by the model; a versioned `policy.json` copied into the prompt by the program; logging of every (role, enquiry, prompt-hash, output) so a wrong outcome can be reproduced from a token sequence.

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

- **Validation.** `jsonschema.validate(state, SCHEMA)` either passes or fails. A paragraph cannot fail validation — it is always "valid text", even when the model has hallucinated a fact or dropped half the conversation. The whole point of the Medium task is that a broken summary must be caught *before* it replaces the history.
- **Comparability across runs.** Two runs of the same script produce two JSON objects with the same seven keys. You can diff them, count what was kept per category, or feed them into the next call as a `system` message with a known shape.
- **No role confusion.** The schema forces the model to declare whether a fact is a fact (`facts`), a decision (`decisions`), a constraint (`constraints`) or an unanswered question (`open_questions`). A paragraph would blur all four into fluent sentences — exactly the failure mode `why_these_probes` warns about.

### 3. What is missing from your state that you would add?

The schema has seven fields. Three things the conversation contained are not representable:

- **Who said what.** `facts` is defined as "things the APPLICANT stated". Turn 4's *question* was asked by the applicant, but any *answer* the assistant gives is not a fact the applicant stated — so the assistant's own statements disappear. This is exactly why Q-3 would still be lost even if the assistant *had* said 150,000: the number would be an assistant statement. I would add **`agent_statements`** (array of strings): things the assistant has told the applicant during the session — the same role as `facts`, but for the other side of the conversation.
- **Turn provenance.** Every item in `facts` / `constraints` / `open_questions` should carry a `source_turn` integer. Without it you cannot tell whether a constraint was stated once or repeated, and you cannot explain a summary that dropped something.
- **Anything unresolved but not literally a question.** Turn 8's "if I bring the id card on Thursday, will the decision be made the same day?" is an open question, yes — but the underlying *commitment* ("if X, then Y") is neither a fact nor a constraint in the schema's sense. I would add **`commitments`** (array of `{condition, consequence}` objects).

To pay for this, I would drop `topic` (redundant with `facts`) and merge `decisions` into `agent_statements`. That frees two fields for `agent_statements` and `commitments`.

### 4. When is compression the wrong choice?

Compression is wrong whenever the *exact wording* is what matters, not just the content. In this session, the applicant asked (turn 7): *"does a scanned letter from my employer count, or does it have to be the original?"* The state object dropped turn 7's question entirely from `open_questions`, even though it appears in `decisions`. The state also flattened turn 5's *"I could not upload my id card because the scanner at home broke"* into a fact — losing the *reason*, which might matter if the applicant later disputes the missing-document decision.

A concrete case where compression would be wrong: **a conversation used as evidence in a dispute about what the office promised.** If A-202 is later refused and appeals, saying *"your assistant told me 150,000 on turn 4"*, the compressed state has no way to check that — `facts` only contains what the applicant said. Only the raw turn-by-turn history is defensible in that scenario.

Would my program notice? **No.** The program validates the summary's *shape*, not its *coverage*. If the model drops a turn, the schema still passes, the history still gets replaced, and the probe still gets answered — with whatever the state happens to contain. A production system would need a second check: after compression, re-ask the same questions against the compressed state and against the raw history, and refuse the compression if the two disagree.

# Sublab Hard — stories in, CVs out

## Setup

- Model: `google/gemma-4-26b-a4b-it` via OpenRouter. (See the disclosure at the top: Easy and Medium ran on `deepseek/deepseek-v4-flash-0731`; Hard was re-run on gemma after deepseek stalled on network for more than 10 minutes with no response. The extraction rules, the rubric and the counting rules are identical; only the model changed.)
- Two-stage pipeline:
  1. **extract** — one call per story, system prompt contains the HARD RULES (null, no estimate, scale conversion, published-only-if-stated, no averaging contradictions, months not jobs).
  2. **score** — one call per extracted CV, system prompt contains the rubric JSON and the counting rules; the model returns three 0–5 numbers and a one-line reason per criterion, and is explicitly told NOT to compute the weighted total.
- The weighted total (0.5·academic + 0.3·research + 0.2·experience, rounded to 2 decimals) and the winner are computed in **code**, from the three scores.
- A separate prose call receives the six `{candidate_id, full_name, model_scores, computed_total, why_each_score}` rows and is asked to name the winner in prose.

## Part 1 — Extraction table

| story | candidate | parsed | validated | null fields | traps hit |
|-------|-----------|--------|-----------|-------------|-----------|
| story-01 | Aziza Bekova | yes | yes | — | none |
| story-02 | Dias Yerzhanov | yes | yes | `gpa_4_scale`, `gpa_original` | no GPA stated, correctly left null |
| story-03 | Lyazzat Omarova | yes | yes | — | 4.6/5.0 converted to 3.68 on 4.0; "under review" paper recorded as non-published, not counted |
| story-04 | Tamerlan Saparov | yes | yes | — | 1 published, 1 under review + 2 in preparation, only the 1 counted |
| story-05 | Аиша Нұрланқызы | yes | yes | — | Kazakh story; "жазылып жатыр" (= in preparation) recorded as non-published |
| story-06 | Nurzhan Abilov | yes | yes | `graduation_year`, `gpa_4_scale`, `gpa_original`, `relevant_experience_months` | **contradictions recorded, not averaged**: 3.2 vs 3.5 GPA, 2024 vs 2026 graduation; the model also flagged the 40-month experience as impossible and zeroed it (see written answers) |

All six CVs validated against the required schema. Every trap listed in the assignment is caught, with the one caveat on story-06's experience (below).

## Part 2 — Scores and ranking

Scores from the model:

| candidate | academic (0-5) | research (0-5) | experience (0-5) | weighted total (code) |
|-----------|---------------:|---------------:|-----------------:|----------------------:|
| Aziza Bekova | 5 | 5 | 0 | **4.0** |
| Tamerlan Saparov | 4 | 0 | 5 | **3.0** |
| Аиша Нұрланқызы | 5 | 1 | 1 | **3.0** |
| Lyazzat Omarova | 4 | 0 | 0 | **2.0** |
| Dias Yerzhanov | 0 | 0 | 5 | **1.0** |
| Nurzhan Abilov | 0 | 0 | 0 | **0.0** |

Weighted formula: `0.5·academic + 0.3·research + 0.2·experience`, rounded to 2 decimals. Computed in Python, not by the model.

Ranking (sorted by code):

| rank | candidate_id | full_name | academic | research | experience | total |
|-----:|--------------|-----------|---------:|---------:|-----------:|------:|
| 1 | story-01 | Aziza Bekova | 5 | 5 | 0 | 4.0 |
| 2 | story-04 | Tamerlan Saparov | 4 | 0 | 5 | 3.0 |
| 3 | story-05 | Аиша Нұрланқызы | 5 | 1 | 1 | 3.0 |
| 4 | story-03 | Lyazzat Omarova | 4 | 0 | 0 | 2.0 |
| 5 | story-02 | Dias Yerzhanov | 0 | 0 | 5 | 1.0 |
| 6 | story-06 | Nurzhan Abilov | 0 | 0 | 0 | 0.0 |

**WINNER (by code): Aziza Bekova, total 4.0.**
**Gap over runner-up (Tamerlan Saparov): 1.0.**
Ranks 2 and 3 are tied at 3.0.

Prose ranking (separate call):

> Aziza Bekova should be awarded the single funded place. She holds the highest computed total of 4.0, driven by perfect scores in both the academic and research categories. With a strong 3.8 GPA and two peer-reviewed publications, she demonstrates the high-level theoretical and investigative rigor necessary for a funded position.
>
> While other candidates possess specific strengths, they lack the balanced profile of Bekova. Tamerlan Saparov and Dias Yerzhanov offer significant professional experience, but they fall short in research output and academic documentation. Similarly, while Аиша Нұрланқызы shows academic excellence, her research and practical experience are insufficient compared to Bekova's proven track record.
>
> Ultimately, Bekova represents the most well-rounded candidate. Her ability to combine top-tier academic performance with established research credentials makes her the most qualified individual to maximize the value of the funding.

The prose agrees with the code on the winner.

## Part 3 — Written answers

### 1. Which rule did you have to add, and what broke without it?

Story-06 forced a rule that the assignment's counting rules did not name explicitly: **"a stated duration in months is countable as stated, even if the number looks round."** The rubric's `counting_rules.experience` says "count months, not jobs. A period with no dates is not countable." It does **not** say what to do when a story gives both a start date (February 2023) and a duration ("about forty months") but the two look like they might not reconcile at a glance.

In this run the model treated February 2023 to "about forty months" as a *contradiction* ("the duration is mathematically impossible") and set `relevant_experience_months` to `0`. That is the wrong call: February 2023 to September 2026 is 43 months, so "40" is a reasonable round-off, not a contradiction. The scoring then gave Nurzhan **experience = 0** on a candidate who has the longest continuous employment of the six.

An earlier run of the same code on a different model gave `40` and Nurzhan scored 1.0 total; this run gives `0` and Nurzhan scores 0.0. That swing is the rule I would add to the prompt verbatim:

> "If the story states a start date and a duration in months, use the duration as stated. Do not recompute the duration and do not flag a mismatch as a contradiction unless the story itself states two different durations."

Without this rule, a reader that trusts the model literally gets one number in one run and a different number the next, on the candidate with the most experience.

### 2. Where did the model guess, and where did your code have to decide?

**Where the model guessed** — story-01, Aziza Bekova. Her only work experience is *"part-time for a data team as a junior analyst… cleaning and documenting a legacy dataset — not research"*. The model classified this as **relevant experience** and gave it a score. In this run it awarded `experience = 0` with the "no months stated" rule in mind; in the earlier run it awarded `1`. The classification of "junior analyst cleaning a dataset" as relevant experience is a judgement call the model made on its own — the story itself says the work "is not research", and the model is not given a definition of what counts as "relevant experience."

**Where my code decided** — the ranked order and the winner. I did not ask the model for the weighted total, and I did not ask it which candidate should win in the JSON call. The code reads three numbers and applies `0.5·a + 0.3·r + 0.2·e`. It also decides the fallback `candidate_id` (the model returned `null` for several stories; the code substitutes the file stem `story-01`, etc.). If I had left the ranking to the model, the tie at rank 2/3 between Tamerlan and Аиша would have been resolved by prose — i.e., by style. The code resolves it by score, and I am free to say in the report that the two are tied.

### 3. Prose ranking vs computed ranking — did they agree?

They agreed. Both name Aziza Bekova as the winner, and both justify it the same way: the 0.5-weight academic criterion dominates, and Aziza is the only candidate with both a strong GPA and two published outputs, so she wins on the criterion that carries half the weight. The prose call also explicitly mentions the two other well-known profiles — Tamerlan (published 1, 24 months) and Аиша (3.9 GPA but non-published second paper) — and ranks them below Aziza for the same reasons the code does.

**If they had disagreed**, I would trust the code. Reason: the code's ranking is a pure function of three inputs that I can audit, and the same three numbers reproduce the same ranking every time. The prose ranking is a single sample from a stochastic process — a second call could phrase a different winner without any of the inputs changing. This is the *whole point* of the assignment's split: a number in a sentence is not a number a program can compare.

To trust the prose ranking on its own, I would want to see: (a) the same winner named across 5–10 identical calls at temperature 0, (b) the losing candidates' reasoning to be consistent across calls, and (c) the prose to explicitly cite the same three criterion scores the code uses. Short of that, prose is a comment on the ranking, not the ranking.

### 4. Rubric anchor for a contradicted field

The rubric says what a 0 means and what a 5 means; it does not say what to do when the story says 3.2 and then 3.5. I followed the assignment's counting rule literally: **the field is null, the contradiction is recorded, and the value is not averaged.** For story-06, `gpa_4_scale` is `null`, `gpa_original` is `null`, and `contradictions` contains `"GPA: candidate states 3.2 but then suggests it might be 3.5"`. The scorer then gave Nurzhan `academic = 0`, which is the rubric's honest reading of "no GPA in the CV, academic is 0."

**What I think the rule should be** — this is where I disagree with the current schema. Contradiction is not the same kind of event as absence. "No GPA" means the applicant chose not to give one; "two GPAs" means the applicant gave two. Collapsing both to `null` loses that difference. I would add a fourth scoring tier to the rubric, anchored explicitly:

> **1 (contradiction)** — the story states a value but contradicts itself. This is not 0 (no information) and not 3 (average of the two values). It is a lower score than either stated value would have earned, because a funded decision cannot be made on an unstable input.

That would make Nurzhan's academic `1` rather than `0`, which correctly separates "Nurzhan gave two numbers and can be asked which is right" from "Dias deliberately gave no number." As written, the rubric treats those two candidates identically on the academic criterion, and they are not the same case.

### 5. The top two candidates

**Aziza Bekova (4.0) and Tamerlan Saparov (3.0), gap 1.0.** Not within 0.05, so the top of the ranking is not marginal. This was also true in the earlier run (Aziza 4.2, Tamerlan 3.0, gap 1.2). Across two runs on two different models, Aziza is rank 1 and Tamerlan is rank 2, with a gap of at least 1.0 every time. That is as close to a stable call as six short stories allow.

**The interesting marginal call is lower down: rank 2 vs rank 3, Tamerlan (3.0) and Аиша (3.0), gap 0.0.** They are exactly tied. Their profiles are opposite: Tamerlan wins on experience (5 vs 1) and loses on research (0 vs 1); Аиша wins on academic (5 vs 4) and research, loses on experience. Because the academic weight is 0.5 and the experience weight is 0.2, the two paths happen to land on the same total. That is not a coincidence of this run — it is exactly the trade-off the rubric's weights create.

**If the top two had been within 0.05**, I would tell the committee three things. First, that the ranking is a statistical tie: with scores that are stable to plus/minus 1 on a 0–5 scale, anything under 0.05 is inside the model's own noise, not a real difference. Second, that the two candidates should be invited to a short interview instead of being decided by a score. Third, that the extraction should be re-run with a **stricter evidence rule**: require the extractor to return the exact quote for every scored field, and refuse any score whose evidence quote does not contain the value being scored. That is the change I would make to the extraction pipeline before I would trust a sub-0.05 gap — not a change to the model, and not a change to the weights.

For this run, no action is needed at the top. The gap is 1.0 and both models agree on the winner. The tie to flag is rank 2/3, and the committee should see that as a tie, not as "Tamerlan beat Аиша by 0.0."
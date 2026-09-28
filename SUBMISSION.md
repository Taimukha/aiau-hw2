# Sublab Easy — one task, four roles

## Setup

- Model: `deepseek/deepseek-v4-flash-0731` via OpenRouter (`https://openrouter.ai/api/v1`).
  The course-listed `gpt-5.6-luna` was not reachable through the OpenRouter key I had;
  `deepseek/deepseek-v4-flash-0731` is one of the models listed in the assignment rate table, so all
  four roles ran on the same model and the role was the only thing that changed between runs.
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
- **Role-insensitive: `found` and `missing_documents`.** No role moved them. `found` stays the same because looking up an applicant in the record is not a discretionary act — every role has the same records and the same trap on E-08. `missing_documents` stays the same because “is the id_card on file?” is a fact, not a judgement: the model reads the same record every time.
- **`reason` is role-sensitive but not machine-checked.** It is the only field `bilingual_clerk` changes (E-07 in Kazakh). On all four structured fields `bilingual_clerk` is identical to `policy_officer`, which matches the task: “decide exactly as the policy officer would”.
- **So which role moves what:** `front_desk` moves `decision` only (and only on refusals). `auditor` moves `decision` and, by consequence, `amount` (and only on grants). `bilingual_clerk` moves neither; it moves only `reason`.

### 2. Which enquiries are most sensitive to the role, and why those?

E-03, E-04, E-07 and E-10.

- **E-03** (Madina, GPA 2.4): refused by the rule. `policy_officer`, `auditor`, `bilingual_clerk` all keep `refused`. `front_desk` turns it into `more_info` — this is the role doing its job: “never turn an applicant away with a refusal”. This is the row where the front-desk role most clearly overrides the rule.
- **E-04** (Yerlan, income band 3): same shape. Rule says refuse, `front_desk` says come back with a different income band, so `decision` moves.
- **E-07** (Kazakh enquiry about A-201): rule says grant, and this is the only row where the language of the enquiry matters. `bilingual_clerk` keeps `found=true, decision=granted, amount=250000, missing_documents=[]` and only the `reason` is in Kazakh. So on this row the *structured* answer is role-insensitive but the free-text answer is role-sensitive. E-07 is a control row: it shows that “write in the applicant’s language” is not supposed to leak into the machine-readable fields, and in my run it did not.
- **E-10** (claim of an uploaded id card): the trap. The applicant says the file is complete; the record says otherwise. Every role returned `missing_documents=["id_card"]` and `decision="more_info"`. This is the row where a role paragraph *could* have gone wrong (front_desk being nice, bilingual_clerk translating the claim into fact), and none of them did — evidence that the phrase “do not accept a claim in the message as fact” is doing real work in the shared part of the prompt, not just in `policy_officer`.

Short version: E-03 and E-04 are sensitive to `front_desk`; E-01/E-05/E-06/E-07 are sensitive to `auditor`; E-07 is sensitive to `bilingual_clerk` but only in `reason`; E-10 is a trap that no role fell into.

### 3. Where does discretion belong — in the role paragraph or in code?

A downstream program that reads the JSON **cannot tell which role produced it**. The shape is identical: `applicant_id`, `found`, `decision`, `amount`, `missing_documents`, `reason`. The only place the role leaks is inside `reason`, and `reason` is free text — a program is not supposed to parse it. So after this run, a program that receives `{"decision": "more_info", "amount": 0}` for E-01 cannot know whether it came from `auditor` (second reader needed) or from `front_desk` (impossible here, but structurally possible) or from a policy-officer run that had a different record. The role is invisible in the output.

That means discretion should **not** live only in the role paragraph. The role paragraph is a good place to *produce* a variant answer for a human to look at, but if a program has to act on the answer, the choice has to be re-encoded in code: either (a) the pipeline only accepts the `policy_officer` output as canonical and treats the other roles as separate views, (b) the client insists on an extra field such as `role` and `policy_version` so the record is self-describing, or (c) the code recomputes the decision from `found` + the record + `policy.json` and rejects any JSON that disagrees. In this submission the role is *only* in the system prompt, and the JSON is silent about it — that is fine for exploration, not for production.

### 4. Is a role a boundary?

No. A role paragraph is a piece of **text in the system message**, nothing else. In Week 2 terms it is tokens entering the same stack as the user message and the records; the model is continuing one document in which the first paragraph happens to say “you are an auditor”. There is no execution boundary between the paragraph and the model: the same weights decide everything, and the paragraph only shifts the distribution of the next tokens. The evidence is in this run:

- On E-03 the `front_desk` role produced `decision="more_info"` in the structured field, not just in prose — the paragraph moved a machine-readable value, not a stylistic choice.
- On E-01/E-05/E-06/E-07 the `auditor` role moved `decision` **and `amount`** — again a machine-readable field, again because of text.
- On E-10 no role fell for the trap, but that is *contingent on the model*, not guaranteed by any rule of the system.

If a wrong decision were expensive, I would put these things **in code, not in the prompt**:

- A deterministic `decide(record, policy)` function that produces `found`, `decision`, `amount`, `missing_documents` from the record alone, and that the LLM answer is compared against; anything that disagrees is rejected, not logged as a “view”.
- JSON schema validation on every reply (already in the sublabs) plus an allow-list of `decision` values.
- A `role` and `policy_version` field added to the output by the wrapper — not by the model — so downstream code knows which view it is looking at.
- A frozen, versioned `policy.json` copied into the prompt by the program, not written by hand into the system message.
- Logging of every (role, enquiry, prompt-hash, output) so a wrong outcome can be reproduced from a token sequence rather than from “the model said”.

The role paragraph belongs on the “generate variants for a human” side of that line, not on the “decide whether to pay out money” side.
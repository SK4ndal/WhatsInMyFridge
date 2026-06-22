# THREAT_MODEL.md schema

`/threat-model` writes this file to `<target-dir>/THREAT_MODEL.md`. The
format is markdown so humans can read and edit it, but the section headings,
table columns, and enum values below are a contract: keep them exactly as
shown so downstream tooling can parse with regex.

---

## Required sections, in order

```markdown
# Threat Model: <system name>

## 1. System context

## 2. Assets

## 3. Entry points & trust boundaries

## 4. Threats

## 5. Deprioritized

## 6. Open questions

## 7. Provenance

## 8. Recommended mitigations
```

A consumer that only needs the threat table can regex for `^## 4\. Threats$`
and read until the next `^## `. Section 8 is optional and additive: older
threat models may omit it, and consumers must tolerate its absence.

---

## Section contents

### 1. System context

One to three paragraphs of prose: what the system is, what it does, who uses
it, where it runs. No table.

### 2. Assets

Markdown table. One row per thing worth protecting.

| asset | description | sensitivity |
|---|---|---|

`sensitivity` ∈ {`low`, `medium`, `high`, `critical`}.

### 3. Entry points & trust boundaries

Markdown table. One row per place untrusted input enters the system or
privilege level changes.

| entry_point | description | trust_boundary | reachable_assets |
|---|---|---|---|

`trust_boundary` is free text naming the crossing (e.g. "untrusted file →
process memory", "unauthenticated network → application logic").
`reachable_assets` is a comma-separated list of asset names from section 2.

### 4. Threats

Markdown table. **This is the threat model proper.** One row per
actor-wants-outcome pair, at the abstraction level where it survives a patch.

| id | threat | actor | surface | asset | impact | likelihood | status | controls | evidence |
|---|---|---|---|---|---|---|---|---|---|

- `id`: `T1`, `T2`, … Stable across edits; do not renumber when rows are
  removed.
- `threat`: One sentence, active voice, names the outcome. "Code execution via
  untrusted input parsing", not "missing bounds check in parser.c".
- `actor` ∈ {`remote_unauth`, `remote_auth`, `adjacent_network`,
  `local_user`, `local_admin`, `supply_chain`, `insider`}.
- `surface`: Which entry point(s) from section 3 this threat traverses.
- `asset`: Which asset(s) from section 2 this threat compromises.
- `impact` ∈ {`low`, `medium`, `high`, `critical`, `existential`}.
- `likelihood` ∈ {`very_rare`, `rare`, `possible`, `likely`, `almost_certain`}.
- `status` ∈ {`unmitigated`, `partially_mitigated`, `mitigated`,
  `risk_accepted`}.
- `controls`: Current mitigations, or `none`.
- `evidence`: CVE IDs, issue links, pentest finding IDs, or commit hashes that
  **instantiate** this threat. May be empty. **Evidence raises likelihood; it
  is not the threat.**

Sort the table by (impact, likelihood) descending so the top rows are the
priorities.

### 5. Deprioritized

Markdown table. Threats considered and explicitly parked.

| threat | reason |
|---|---|

Common reasons: out of scope, actor not in threat model, asset not present,
risk accepted by owner.

### 6. Open questions

Bullet list. Things the analysis could not determine from code alone.

### 7. Provenance

```markdown
- mode: bootstrap
- date: YYYY-MM-DD
- target: <path or repo url @ commit>
- inputs: <--vulns path | "git-log + docs mined">
- owner: unset
```

### 8. Recommended mitigations

Optional. Each row is **one class-level control**, not a per-finding patch: a
mitigation that closes or materially shrinks an entire threat cluster
regardless of which instance is found next.

| mitigation | threat_ids | closes_class | effort |
|---|---|---|---|

- `mitigation`: imperative, one line describing the control class.
- `threat_ids`: comma-separated section 4 ids this mitigation covers.
- `closes_class`: `yes` | `partial`.
- `effort`: `S` | `M` | `L`.

---

## Scoring guide

### Impact

| value | means |
|---|---|
| `low` | Nuisance; no data or availability loss. |
| `medium` | Limited data exposure or degraded availability for some users. |
| `high` | Significant data exposure, integrity loss, or full availability loss. |
| `critical` | Full compromise of a primary asset (code execution, auth bypass, data exfil at scale). |
| `existential` | Compromise threatens the organization's continued operation. |

### Likelihood

| value | means |
|---|---|
| `very_rare` | Requires nation-state resources or an unlikely chain of preconditions. |
| `rare` | Requires significant skill and a non-default configuration. |
| `possible` | A motivated attacker with public tooling could plausibly do this. |
| `likely` | The attack surface is reachable and the technique is well known; prior evidence exists in this or similar systems. |
| `almost_certain` | Actively exploited in the wild, or trivially automatable against the default configuration. |

Evidence (past CVEs in the same surface, pentest findings, public exploit
code) moves likelihood **up**. Existing controls move it **down**. Score the
**residual** likelihood after current controls.

---

## Example (excerpt)

```markdown
## 4. Threats

| id | threat | actor | surface | asset | impact | likelihood | status | controls | evidence |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Arbitrary code execution via malformed input to the file parser | remote_unauth | file parser | host process integrity | critical | likely | unmitigated | none | CVE-2025-1001, CVE-2025-1042 |
| T2 | Denial of service via resource exhaustion in the file parser | remote_unauth | file parser | service availability | medium | likely | unmitigated | none | CVE-2025-1042 |
| T3 | Supply-chain compromise via unpinned dependency | supply_chain | build pipeline | host process integrity | critical | rare | partially_mitigated | lockfile present | |
```

T1 stays in the model after both CVEs are patched: attackers will still send
malformed files. The CVEs are evidence the surface is fertile, not the threat
itself. T3 has no evidence — it was added by gap-fill and is valid regardless.
```

# threat-model: bootstrap

Derive a threat model from code and past vulnerabilities. Five stages: research
the target, synthesize findings into schema sections 1-3 and a vulnerability
working table, generalize vulnerabilities into threat classes, gap-fill with
STRIDE, emit `THREAT_MODEL.md`.

Static analysis only — do not build, run, fuzz, or modify the target.

---

## Inputs

- `<target-dir>` (required): local checkout.
- `--vulns <path>` (optional): past vulnerabilities. Accepts: newline-separated
  CVE IDs, CSV with columns `id,title,component,description`, markdown pentest
  report, or JSON array of objects with at least `id` and `description` keys.

---

## Stage 1 — Research

Goal: gather everything needed to populate sections 1-3 and the vulnerability
working table.

These four research tasks are independent; run them concurrently if your
environment supports it, sequentially otherwise.

**Docs & manifest.** Read project documentation (README, SECURITY, CHANGELOG,
top-level docs directory) and whatever build manifest describes the project's
dependencies and structure. Produce: a prose system description; any
self-documented security fixes.

**Surface mapping.** Read the source tree to find every place untrusted input
enters the system or privilege changes. For each surface, record: surface type,
representative file and function references, and what crosses the boundary.
Identify the surface types below in whatever form the target's language and
framework express them. Treat this as a seed — extend with idioms specific to
the stack in front of you.

| Surface type | What to look for |
|---|---|
| Network | Sockets, HTTP/RPC/GraphQL route handlers, any listener that accepts inbound connections |
| File / format parsing | File reads, format parsers, decoders, deserializers that process external data |
| CLI / environment | Command-line argument parsing, environment variable reads |
| IPC / plugins | Subprocess spawning, dynamic loading, eval or exec on external input, plugin interfaces |
| DB / query | Query construction from external input; escapes in ORM or raw query APIs |
| Supply chain | Dependency manifests, vendored code, automated fetch-and-run in build or CI scripts |
| Infra / IAM | Container and orchestration config, IaC, identity grants, secrets mounts |

Exclude generated code and third-party vendored directories. Cap to ~5
representative file references per surface row to stay concise.

**Asset identification.** Identify what the system protects or produces:
sensitive data (secrets, credentials, user records), process integrity, service
availability, downstream assets if it is a library or platform. Assign a
sensitivity level to each (`low`, `medium`, `high`, `critical`).

**Vulnerability history.** Gather from up to three sources:

- *Git history*: identify the codebase's language and domain, then derive
  keywords that would appear in security-fix commit messages for this specific
  stack. Start from the base set (`CVE- security vuln fix exploit`) and add
  terms specific to the domain (e.g., for a parser: overflow, corruption,
  exhaustion; for a web service: injection, traversal, bypass). Search git log
  with those keywords and read the full diff of each matching commit.
- *Public advisories*: if the repository has a public GitHub remote and `gh`
  is available, query its security advisories. Otherwise note "no public
  advisory source".
- *Supplied file* (only if `--vulns` was provided): parse it into normalized
  rows `{id, title, component, class, vector}`.

---

## Stage 2 — Synthesize

Turn the Stage 1 findings into schema sections 1-3 and a vulnerability working
table.

**Section 1: System context.** Write 1-2 paragraphs: what the system is, what
language and stack it uses, approximate size, who would embed or deploy it, and
where it runs.

**Section 2: Assets.** From asset identification. Deduplicate. Assign
`sensitivity` from the schema enum.

**Section 3: Entry points & trust boundaries.** Merge surface-mapping and
infra/IAM results. Deduplicate. For each row, name the trust boundary
explicitly (e.g., "untrusted file → process memory", "unauthenticated network
→ application logic"). List which section 2 assets are reachable from each
entry point. Supply-chain and infra/IAM surfaces are entry points even though
no runtime data crosses them at request time. **Every section 3 row must
receive at least one section 4 threat row in Stage 3 or 4** — this is the
coverage invariant checked at emit time.

**Vulnerability working table.** Concatenate rows from git history, advisories,
and the supplied file. Deduplicate by `id`. For each row, determine which
section 3 entry point it traversed. If a vulnerability's entry point is not
in section 3, the surface mapper missed it — add it now. This table does not
appear in the output file; it feeds the `evidence` column in Stage 3.

---

## Stage 3 — Generalize: vulnerabilities → threats

Goal: cluster the vulnerability working table into threat rows at the
abstraction level where they survive a patch.

### 3a. Cluster

Group the working table by `(entry point, bug class, asset reached)`. Each
group becomes **one** candidate threat. Examples:

- Multiple memory-safety bugs in different parsers, all reaching process
  memory → one threat: "Code execution via memory corruption in untrusted
  input parsing." Evidence: all IDs.
- Multiple injection bugs in different endpoints, all reaching the same
  database → one threat: "Data exfiltration and tampering via query injection
  in the HTTP API." Evidence: all IDs.

Apply the litmus test to each statement: would it still be true after every
evidence item is patched? If not, zoom out further.

### 3b. Variant scan

For each cluster, search for **siblings**: code paths with the same shape not
yet in the vulnerability list. You are not proving exploitability — you are
estimating how much of the surface shares the pattern. More siblings → higher
likelihood. Record locations in working notes for the hand-back; do not put
them in the `evidence` column (evidence is for confirmed past vulnerabilities
only).

### 3c. Score

For each cluster, assign:

- `actor`: from the entry point. File parsing → whoever supplies the file.
  Network endpoint → `remote_unauth` or `remote_auth` depending on whether
  authentication precedes it.
- `impact`: from the asset and bug class. See the scoring guide in `schema.md`.
- `likelihood`: start from evidence. ≥1 confirmed past vulnerability in this
  surface → at least `likely`. Public exploit or active exploitation →
  `almost_certain`. No evidence but siblings found and technique is well known
  → `possible`. Adjust down for verified controls.
- `controls`: look for existing mitigations relevant to this surface and class.
  `none` if none found.
- `status`: `unmitigated` unless a control fully closes the threat.
- `recommended_mitigation` (working notes only): one class-level control that
  would close or materially shrink this entire cluster regardless of which
  instance is found next. Prefer controls that survive the next bug over
  patches for the last one. These become section 8 rows in Stage 5.

Write each cluster as a section 4 row.

---

## Stage 4 — Gap-fill

Past vulnerabilities are biased toward what has already been found. For
**every section 3 entry point that has no section 4 row yet**, walk STRIDE and
add the plausible threats:

| | For this entry point, could an attacker… |
|---|---|
| Spoofing | …pretend to be a trusted source? |
| Tampering | …modify data in transit or at rest? |
| Repudiation | …act without leaving attributable logs? |
| Info disclosure | …read data they shouldn't? |
| DoS | …exhaust a resource (CPU, memory, disk, connections)? |
| Elevation | …end up with more privilege than they started with? |

Also walk entry points that already have rows — the existing threat may not
be the only plausible STRIDE category. (A parser with an RCE threat almost
certainly also has a DoS threat.)

For **infra/IAM entry points**, walk these instead of STRIDE:

- **Over-grant**: does the identity reach more than the application needs?
- **Lateral identity**: can a co-located workload assume this identity?
- **Drift**: is any grant managed outside this codebase, so it won't be
  reviewed or torn down with the code?
- **Residual access**: do credentials or principals from a predecessor system
  survive?
- **Scope enforcement**: where automated writes or approvals exist, what bounds
  them to their intended scope?

Threats added here have empty `evidence`. Score `likelihood` from technique
prevalence and surface reachability alone. **The final section 4 table must
contain at least one row with empty evidence**, or this stage did not run.

Populate section 5 (Deprioritized) with STRIDE categories you considered and
ruled out, with the reason.

---

## Stage 5 — Emit

**Coverage check.** For every section 3 entry point, confirm at least one
section 4 row names it verbatim in the `surface` column. Any gap means Stage 4
is incomplete — add the missing threat before writing the file.

**Sort and number.** Sort section 4 by (impact descending, likelihood
descending). Assign `id` = `T1`, `T2`, … in sorted order.

**Section 6: Open questions.** Everything the code could not determine:
deployment context not visible from source, intended actors or data flows
requiring owner knowledge, controls claimed but unverifiable here, risk
appetite questions only an owner can answer.

**Section 8: Recommended mitigations.** From Stage 3c working notes. One row
per class-level control, listing the threat IDs it covers, whether it closes
the class, and rough effort (S/M/L). Merge controls that cover multiple
clusters into one row.

Write `<target-dir>/THREAT_MODEL.md` per `schema.md`. Set provenance:

```
- mode: bootstrap
- date: <today>
- target: <target-dir> @ <git commit hash, or "not a git repo">
- inputs: <--vulns path, or "git-log + docs mined">
- owner: unset
```

Hand back to the user:

1. Path to the file.
2. Top 5 threats (id, threat statement, impact × likelihood).
3. Count of threats with evidence vs without (confirms gap-fill ran).
4. Stage 3b sibling locations as candidate leads for further investigation.
5. Section 8 recommended mitigations, top 3 by (closes_class yes first, effort
   ascending).
6. Section 6 open questions.

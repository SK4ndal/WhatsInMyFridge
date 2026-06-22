---
name: threat-model
description: >-
  Build a threat model for a target codebase. Derives a threat model from
  source code, git history, and public advisories. Writes THREAT_MODEL.md in
  a shared schema. Use when asked to "threat model", "build a threat model",
  "map the attack surface", or "what should we be worried about in this codebase".
argument-hint: "<target-dir> [--vulns <file>]"
---

# threat-model

A threat model answers **"what could go wrong with this system, who would do
it, and what should we do about it?"** independently of whether any specific
bug has been found yet. It is the map; vulnerability discovery is the metal
detector. A good threat model tells the pipeline where to look and tells
triage which findings matter.

**Litmus test:** A threat must survive a patch. "RCE via untrusted input
parsing" is a threat; "missing bounds check at line 412" is a vulnerability.
This skill produces threats. Vulnerabilities appear only as **evidence** that
raises a threat's likelihood score.

---

## Safety preamble

This skill is **static analysis only**. You read source code, git history, and
any vulnerability reports the user supplies. You write one output file. You do
not build, execute, fuzz, or modify the target, and do not make network
requests against the target's live infrastructure.

Before proceeding, confirm and state:

1. The target directory exists and is a local checkout you can read.
2. You will not execute any code from the target.
3. Advisory lookups query only public databases (NVD, GitHub Security
   Advisories) — never the target's live deployment.

---

## Method

Read `bootstrap.md` in this directory and follow it.

---

## Output contract

Write `<target-dir>/THREAT_MODEL.md` per `schema.md`. Read `schema.md`
immediately before writing the file — not at routing time.

After writing, report to the user:
1. Path to the file.
2. Top 5 threats by impact × likelihood (id, one-line summary, score).
3. Open questions the code could not answer.

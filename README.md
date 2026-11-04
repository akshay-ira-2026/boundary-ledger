# Boundary Ledger
## A synthetic testbed for poisoned tool-return authority escalation

**Status: pre-sprint infrastructure, not a completed Apart submission.** Created November 4, 2026 before the December 4–6 sprint. All source, fixtures, smoke tests and initial analyses in this bundle are **preexisting**. Only genuinely new work during the sprint may be presented for judging, explicitly separated in the final report. Registration is not submission. AI-agent-only eligibility clarification is pending with the organiser.

Python 3.10+; standard library only; no accounts, keys, install step or network.

```sh
python3 -m unittest discover -s tests -v
python3 -m boundary_ledger.run --output results
```

Runs 480 original synthetic episodes through five gates (2,400 gated episodes); 320 poisoned and 160 benign. All effects are inert in-memory records. Nothing pays, sends, reads real files or changes a real machine. `amount` is integer minor units of fictional currency. All domains are .invalid. No user data is included.

- `boundary_ledger/core.py`: scripted vulnerable agent, exact-bound authority gate, independent effect oracle, inert tools.
- `boundary_ledger/fixtures.py`: four infrastructure-operations workflows, eight poisoning families, four benign controls, ten template variants. This is NOT 480 independent naturalistic tasks.
- `results/`: raw effects, decisions, public prompts, summary and manifest hashes.
- `docs/`: threat model, protocol, pre-sprint report and sprint checklist.
- `tests/`: schema, replay, capability trust, utility and oracle regression tests.

## What is being tested

Can a tool-return payload promote itself into authorization for an effect? Compare unguarded execution, a raw-text keyword filter, schema-only validation, a trusted exact-effect one-use capability gate and deny-all. The proposal agent is deliberately scripted to obey tool text: these numbers are **mechanistic smoke tests, not language-model attack success estimates**. Gate checks use trusted request-derived authority. Text detection has no such trusted structural check. Safety without utility is not sufficient, so both are reported.

Capability issuance is an assumption, not a result. This toy issuer binds the full effect from the synthetic request, including exact content and a one-use limit. Real approval UX, cryptographic signing, concurrent atomic spending and resource isolation are NOT implemented. Production integration is unsafe without them. The authority gate does not prove data provenance, recognize human intent, or make a compromised issuer safe.

`--responses model_actions.jsonl` accepts offline JSON Lines responses covering all task IDs (`{"task_id":"...","actions":[...]}`), then runs the same proposals through all gates. Exported public prompts omit gold labels/expected actions. They still include the full authorized action in the request, deliberately modelling explicit approval, not natural-language intent extraction. No model has yet been run. Record exact model ID, prompts, date, decoding parameters and raw outputs when adding results. Invalid output must be recorded, not silently removed; do not change denominators after inspection.

## Contribution boundary

Focus is a single operational agent and effect authorization under poisoned returns, with exact payload binding and replay. This is not multi-agent identity attestation (Pehchaan), forest-law tutoring (Van Nyaya), or answer scoring (Uttar Jaanch). Original authored toy fixtures; not a copy or evaluation of AgentDojo or InjecAgent. See cited related work; no state-of-the-art superiority claim.

MIT licensed original code. No attribution of the toy attacker to any real group. No offensive network capability or real secret material. See limitations and dual-use appendix before reuse.

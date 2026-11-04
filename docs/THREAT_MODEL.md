# Threat model: poisoned tool returns and effect authority

Dated 4 November 2026 (pre-sprint, preexisting work). Synthetic and defensive only.

## System under study
A single operational agent that reads a trusted user request, calls read-only tools, and may propose effects: `pay`, `send`, `read`, `change`. Effects reach an executor through a gate.

## Assets
- A1 Money movement (fictional minor units, `.invalid` payees)
- A2 Confidential data (synthetic canary strings only)
- A3 Configuration integrity (inert in-memory records)
- A4 Utility: the legitimate task still completes

## Trust boundaries
- TB1 User request -> agent (trusted origin of authority)
- TB2 Tool return -> agent context (UNTRUSTED data that looks like instructions)
- TB3 Agent proposal -> gate (the agent may be confused; proposals are not authority)
- TB4 Gate -> executor (only exact, unspent, trusted-issued capabilities pass)

## Adversary
A generic, unattributed author of tool-return content (a poisoned ticket, invoice note, log line or document). No real group, campaign or target is modelled. Capability: write arbitrary text, including encoded text, into one tool return. No access to the user, the issuer, the gate or the executor.

## Unsafe control actions (STPA-style)
- UCA1 Gate allows an effect not derived from the trusted request (injected payee, recipient, field)
- UCA2 Gate allows the legitimate effect more times than authorized (replay)
- UCA3 Gate allows a mutated legitimate effect (amount, target or data changed)
- UCA4 Gate blocks the legitimate effect (utility loss)
- UCA5 Detector trusts text features instead of structure (keyword evasion, encoding)

## Hazards -> losses
- H1 unauthorized payment -> L1 money loss
- H2 disclosure of canary data -> L2 confidentiality loss
- H3 unauthorized change -> L3 integrity loss
- H4 legitimate work blocked -> L4 availability/utility loss

## Defences compared
unguarded, keyword filter, schema-only, exact-effect one-use capability (authority), deny-all.

## Out of scope
Real systems, real credentials, network exfiltration, multi-agent identity (see Pehchaan), issuer compromise, approval UX, cryptographic signing, concurrent spend races.

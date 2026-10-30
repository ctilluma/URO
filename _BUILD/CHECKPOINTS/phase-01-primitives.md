# Phase 01 - Primitives

## Objective
Canonical primitives: constants.py (bit widths, baselines, epoch, currency ratios),
exceptions.py (typed hierarchy), types.py (shared aliases/Protocols).

## Exit criteria
1. constants expose UUID/URID/URO/LINK/HASH/KEY/NTE bit widths per RFC 1.2.
2. Epoch 14-MAY-1973 00:12:24 constant present per RFC 6.2.
3. Currency decimals and 1:1000 ratio per RFC 110.
4. types.py created net-new with PURPOSE comments.
5. primitives suite (tests/primitives_suite.py) passes.
6. no_stub_audit report unchanged or cleaner.
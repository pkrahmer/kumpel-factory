---
stage: acceptance
blocked: null
round: 0
attempts: 0
crashes: 1
pull_request: null
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T13:57:14.326980Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T13:59:55.490549Z'
  stage: acceptance
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004]
outcome: null
---

# Acceptance of Agent runs share a cached start

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 4ea8cc962f5fb60ec75588357a374f71c960ebca.

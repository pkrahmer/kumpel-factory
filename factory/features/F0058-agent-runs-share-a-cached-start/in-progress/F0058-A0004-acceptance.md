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
  at: '2026-11-08T15:36:50.420578Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T15:39:10.333030Z'
  stage: acceptance
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004, F0058-S0005, F0058-S0006, F0058-S0007, F0058-S0008]
outcome: null
---

# Acceptance of Agent runs share a cached start

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit e8ada771ab08d76c91d3dedff3631fdbdb988481.

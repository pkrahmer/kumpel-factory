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
  at: '2026-11-08T16:42:57.236497Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T16:45:40.572532Z'
  stage: acceptance
stories: [F0059-S0001, F0059-S0002]
outcome: null
---

# Acceptance of Each change is checked once

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 036d6fb5079ed6b7c731d9927f1d8fd45a414cdb.

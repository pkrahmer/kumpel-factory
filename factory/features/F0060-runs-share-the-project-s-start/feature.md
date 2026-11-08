# Runs share the project's start

## Goal

Every agent run writes its whole first message into the prompt cache, and no later run reads it back: Claude Code puts its one cache point for the messages at the end of the first message, and each run's message differs (`planning/later-topics.md`, topic 2; experiments of 2026-11-08 in `docs/runs/2026-11-05-f0052/log.md`, 19:04 to 19:30 UTC). Two large parts of that message are the same in every run of a project: the rules every role shares (the `## Rules` section, the same in all seven shipped agent files, about 1,600 tokens) and the project's `CLAUDE.md`, which Claude Code itself puts at the start of the first message (about 7,300 tokens in kumpel-factory). The system prompt, by contrast, is already read from the cache by every run that follows within the cache's time.

After this feature both parts stand in the system prompt: the shared rules in `agents/system-prompt.md`, which both runtimes already send, and, under Claude Code, the project's `CLAUDE.md` after them, with Claude Code's own loading of it switched off. Every run then reads both from the cache when the run before it ended less than five minutes earlier, which held for 118 of 119 gaps in F0058 and F0059. Replayed on those features' 120 runs, this saves about 13 % of their cost at one price list (11 % on the demo). The five-minute cache, a trial on the instances `vm` and `demo3` since 2026-11-08, becomes the factory's own setting: the one-hour cache would save 18 to 23 % but its dearer writes cost 32 to 34 % more. The feature also removes a relay that wastes a run per review round: in F0050 to F0059, 58 of the 65 coder runs right after review findings changed nothing and passed the work item to the tester, because the reviewer cannot send findings that need only tests to the tester itself; after this feature it can. Done when the three stories are merged, the human's changes are made and `make check` is green on `develop`.

## Before it starts

F0059 is archived and promoted. Measured on 2026-11-08 under Claude Code 2.1.318: `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` keeps Claude Code from loading the project's `CLAUDE.md` under the subscription login and leaves the project's skills loading; `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` makes every cache write a five-minute one.

## Scope

- The rules every role shares move from the seven shipped agent files into the shipped system prompt, which every run of both runtimes receives (S0001).
- Under Claude Code, the run's system prompt carries the project's root `CLAUDE.md` after the shared rules, and Claude Code no longer loads it itself (S0002).
- Under Claude Code, every cache write is a five-minute one, set by the factory (S0002).
- The reviewer sends findings that need only tests to the tester, when the pipeline definition offers `tests` after `review` (S0003).

## Out of scope

- The story text in the system prompt: replayed on F0058 and F0059, it loses more than it saves, because Claude Code allows one cache point in the system prompt and every change of the story text (intake's rewrite, an answer, a criterion added) would then miss `CLAUDE.md` too.
- OpenCode's handling of the project's instructions: it reads them itself into its system part, and S0002 does not change it.
- Lessons that several roles share, `CLAUDE.md` files below the project's root, `CLAUDE.local.md` and `.claude/CLAUDE.md`: not carried (decision 3).
- A cache measurement in the cost records or `factory-bill`.

## Stories

- S0001: The rules every role shares stand in the system prompt.
- S0002: Claude runs carry the project's CLAUDE.md in the system prompt.
- S0003: A review whose findings need only tests goes to the tester.

## The human's changes

After S0001 is merged, on `develop`: `CLAUDE.md`, first paragraph, "(the shipped agent files under `agents/agents/`)" becomes "(the shared system prompt `agents/system-prompt.md` and the shipped agent files under `agents/agents/`)".

Once an instance runs code with S0002 (for `vm`, when it moves to the promoted F0060; `demo3` is not moved, and `demo4` is set up without them), on the VM (not in the repository): the trial lines `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` and `FACTORY_CONTAINER_ENV=CLAUDE_CODE_PROMPT_CACHE_TTL` leave `factory.local.env` of the instances `vm` and `demo3`, and both restart. Then the next story's transcripts show `ephemeral_5m` writes and a first request that reads more than 6,683 tokens.

After S0003 is merged, on `develop`: `review` gains `tests` as its third `next` in `factory/pipeline.yml`, `demo/todo-service/project/factory/pipeline.yml` and `operator/template/factory/pipeline.yml` (`next: [docs, doing, tests]`; `round_cap` and the leases stay).

## Decisions taken for the human

1. The leave for S0001 (the human, 2026-11-08): the tests that read the `## Rules` section, a rule `R1.` to `R15.` or the order of sections from a shipped agent file (`tests/agent_files/test_claude_agent_refusal.py`, `test_claude_agent_skills.py`, `test_claude_agent_texts.py`, `test_claude_agent_texts_check_red.py`, `test_claude_agent_texts_docs_slip.py`, and any other test whose only failure is this move) read them from `agents/system-prompt.md` instead and check the same text; the order of sections in an agent file loses `## Rules`.
2. The built-in fallback `SYSTEM_PROMPT` stays equal to the shipped `agents/system-prompt.md`, the rules included, as a test already demands.
3. Only the project's root `CLAUDE.md` is carried, as the checkout of the run holds it. Claude Code's switch also stops it loading nested `CLAUDE.md` files on demand; no project of the factory has one, and the operator guide says so.
4. The five-minute cache is a switch of the Claude runtime like its other switches, not a setting: the measurement shows no case where the one-hour cache pays.
5. The route from review to tests counts as a rework round against `review`'s `round_cap`, by the rule that already counts every decision other than a stage's first `next`; a review with any finding outside the tests sends all its findings to `doing`, so no finding is split across two stages (2026-11-08).

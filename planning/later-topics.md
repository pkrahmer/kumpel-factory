# Topics to discuss later

Noted on 2026-11-08 while F0058 ran. Each item is open: nothing is decided until the human and Claude talk it through.

## 1. Acceptances that keep proposing stories (the main topic)

F0058's first acceptance (A0001) proposed S0005 and S0006; when they were done, the second acceptance (A0002) proposed S0007; S0007 will bring a third. Each round costs an acceptance (about $1.50) and its story, and the findings shrink: a real bug (S0005), a guide gap (S0006), then a stale example caused by the human's own `Makefile` change (S0007).

Proposal to discuss: a second or later acceptance judges only the stories added since the last one, and proposes a story only when a criterion of the feature's goal is unmet or something is broken; anything else is a "noticed" item in its report. Until it is decided, the human merges a later acceptance whose proposals are only cosmetic, leaves them in the backlog for later planning, and archives the feature by hand.

## 2. The five-minute prompt cache: make it persistent and documented

On 2026-11-08 the prefix comparison of the 36 measured runs showed that no run reads another run's start beyond Claude Code's own 6,683 tokens: Claude Code puts its cache breakpoint after the role and the run's facts, so the shared work item is never reused across runs. The one-hour cache (written at twice the input price) therefore only costs. As a trial, `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` and `FACTORY_CONTAINER_ENV=CLAUDE_CODE_PROMPT_CACHE_TTL` were added by hand to `factory.local.env` of the instances `vm` and `demo3`.

If the next runs show `ttl: 5m` in their transcripts and the cache writes cost less: make it persistent (the factory sets it for every Claude Code run, or `setup.sh` and the template write it) and document it (the operator guide's agent runtime and settings, `docs/decisions.md`). Open with it: whether reuse across runs is worth a design (the work item as a message of its own, or the API without Claude Code), and the test of whether Claude Code's second system part changes per run.

## 3. Other findings kept for later

- **The credit running out is a "died" stall.** On 2026-11-08 at 14:46 two documenter runs died with "Credit balance is too low"; the pull request said only "died without a result", the factory retried after 15 seconds, then stopped at the attempts cap. It could be a `provider_limit` (or a stop of its own) that names the cause and does not retry at once.
- **The coder's own check.** Whether the coder may run a lighter check than `make check` (tests it touched, lint, types, layers), measured on F0059's numbers; in F0053 to F0058 the factory's check after the coder was red once in 113 coder results.
- **`facts-diff` without `origin/develop`** prints nothing instead of failing; the human's `Makefile` should make it fail, so the block shows `failed:` (A0002).
- **Disk:** both F0058 acceptances saw the pool's free space fall by 0.6 GB that the instance's folders do not explain (stage datasets, snapshots or images).
- **A warning hook for the time left** (Claude Code's PostToolUse `additionalContext`, OpenCode's `tool.execute.after`), and a warm index or LSP service for the agents.

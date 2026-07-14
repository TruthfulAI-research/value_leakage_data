# value_leakage_data

Cached model rollouts and judge outputs for
[Value Leakage: An LLM's Answers Are Silently Shaped by Its Own Values](https://github.com/TruthfulAI-research/value_leakage).
This repository is used as the `data/` submodule of the code repository; the
analysis and plotting scripts there run from these caches without API access.

- `final_data/` — rollout and judge caches for all experiments (Donation Bet, AI Company Questions, Job Offer, Agentic Grading)
- `choosing_activities/results/` — Choosing Activities pipeline results

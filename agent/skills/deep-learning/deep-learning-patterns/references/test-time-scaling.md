# Test-Time Scaling (TTC/TTS) — Referencia Completa

> **Session:** 2026-07-08
> **Full note:** `notes/deep-learning/2026-07-08-test-time-scaling-reasoning.md`

## Taxonomía

### Single-Path Methods
- **CoT** — Chain-of-Thought prompting (Wei et al. 2022)
- **Self-Consistency** — N samples + majority vote (+10-15pp on GSM8K)
- **Self-Correction** — Iterative revision loop

### Multi-Path Search
- **Best-of-N** — Generate N, score with verifier
- **Beam Search** — Verifier-guided, N best partial traces
- **MCTS** — Monte Carlo Tree Search (AlphaZero-style for text)
- **DVTS** — Diverse Verifier Tree Search

### Revision Methods
- **ReST** — Self-Refine with self-generated data
- **Step-by-Step Verification** — Verify each reasoning step

## ORM vs PRM

| | ORM | PRM |
|---|---|---|
| Signal | Final answer only | Each step |
| Density | Low (1/trace) | High (N/trace) |
| Labeling cost | Low | High |
| Best for | BoN, voting | Beam, MCTS |
| Reward hacking | Vulnerable | Robust |

## Key Papers
- arXiv:2408.03314 — Snell et al., "Scaling LLM Test-Time Compute Optimally" (Google DeepMind)
- arXiv:2512.02008 — Agarwal et al., "The Art of Scaling Test-Time Compute" (Microsoft)
- arXiv:2510.08049 — "Survey of Process Reward Models"
- https://testtimescaling.github.io/ — Full survey

## Key Findings (Agarwal 2025)
1. No single strategy universally dominates
2. Reasoning models split into short-horizon (R1, QwQ) and long-horizon (Qwen3, GPT-OSS)
3. Optimal performance scales monotonically with compute budget
4. **Recipe:** Low compute → greedy, medium → beam, high → majority vote

## Practical Resources
- https://github.com/Hritikd/hermes — TTC engine with PRM + MCTS
- https://github.com/zzli2022/Awesome-System2-Reasoning-LLM — System 2 reasoning LLMs
- https://github.com/hijkzzz/Awesome-LLM-Strawberry — LLM techniques collection

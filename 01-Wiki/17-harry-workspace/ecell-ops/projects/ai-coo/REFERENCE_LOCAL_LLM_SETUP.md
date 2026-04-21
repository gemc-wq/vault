# Reference: Local LLM Multi-Mac Setup
> YouTube: https://www.youtube.com/watch?v=SGEaHsul_y4
> Shared by Cem: 2026-02-09

## The Setup (Alex Cheema / Exo Labs)
- **Mac Mini (16GB)** — Orchestrator, running Clawdbot as the controller brain
- **2x Mac Studio M3 Ultra (512GB each)** — Compute nodes running local LLMs
- Connected via **Thunderbolt 5 (RDMA)** for fast inter-machine communication
- Using **Exo Labs** framework to distribute the model across both machines
- Running **Kimi K2.5** locally at ~24 tok/sec across the two machines

## Key Insight
The Mac Mini doesn't run the LLM itself — it's just the orchestrator (Clawdbot).
The heavy Macs are the "muscle" running the actual model inference.
Coding agents and video editing agents run on the local machines.
One controller → multiple workers. Hub and spoke.

## Kimi K2.5 Performance
- Open source, 1T parameters (32B active MoE)
- Scores 90% of what Claude Opus 4.5 can do
- $30/mo subscription vs $200/mo Claude Max
- Can run locally on 512GB+ RAM machines
- Agent Swarm: up to 100 sub-agents, 1,500 tool calls

## Relevance to Ecell
Our setup is conceptually similar but uses API models instead of local:
- Harry (VPS) = orchestrator like the Mac Mini
- Ava (iMac) = worker with free CLI tools
- We use API models (Opus for leads, Flash for sub-agents)
- Cost is comparable without $10K+ hardware investment

## Future Consideration
If Ecell wanted to go fully local/private:
- 2x Mac Studio M3/M4 Ultra 512GB (~$10K each)
- Run Kimi K2.5 locally for zero API costs
- Complete data privacy (nothing leaves the network)
- But: high upfront cost, maintenance, power consumption

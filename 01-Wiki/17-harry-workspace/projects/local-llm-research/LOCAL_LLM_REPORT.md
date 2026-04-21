# Local LLM Feasibility Report: Head Case Designs
**Date:** February 6, 2026
**Prepared by:** Clawdbot (Sub-agent)

---

## 1. Executive Summary: Is It Worth It? (Cost-Benefit Analysis)

For Head Case Designs, transitioning to a **hybrid local/cloud model** is not just about cost—it is about **operational efficiency** and **data sovereignty**.

### Current State
*   **Monthly Cloud Spend:** ~$250 (Claude Opus, Gemini, GPT-5.2).
*   **Annual Projected Spend:** ~$3,000.
*   **Main Pain Points:** Latency for high-frequency tasks, privacy concerns with sales/inventory data, and unpredictable API cost spikes.

### Cost-Benefit Analysis (24-Month Horizon)
| Metric | Cloud-Only (Status Quo) | Local (Mid-Range Option B) |
| :--- | :--- | :--- |
| **Initial Investment** | $0 | ~$3,800 (Mac Mini M4 Pro 96GB) |
| **Ongoing Monthly Cost** | $250 - $400 | $20 - $40 (Electricity + Cloud Backup) |
| **Total 24-Month Cost** | ~$7,200 | ~$4,500 |
| **Break-Even Point** | N/A | **14 - 16 Months** |

### Strategic Advantages
1.  **Zero-Cost Repetitive Tasks:** Classification of 10,000+ support tickets, inventory tagging, and high-frequency RAG embedding generation become effectively "free."
2.  **Privacy:** Sensitive sales data and customer info stay within the internal network.
3.  **Speed (Zero Queue):** No API rate limits or downtime. Local models respond instantly for low-latency tasks (packing verification).

---

## 2. Hardware Options (Minimum to Ideal)

### Option A: Budget (~$1,000–$1,500)
*   **Hardware:** **Mac Mini M4 (Base)** or **Used RTX 3090 Build (Ubuntu)**.
*   **Config:** Mac: 32GB Unified RAM | PC: 24GB VRAM.
*   **LLM Capability:** Runs Llama 3.1 8B (Full) or 70B (High Quantization, e.g., Q2/Q3 - slow).
*   **Performance:** ~10-15 tokens/sec (8B models).
*   **Office Fit:** Extremely quiet, low power (~30-60W).
*   **Verdict:** Good for basic RAG and testing, but will struggle with complex reasoning.

### Option B: Mid-Range (~$2,500–$4,000) — **RECOMMENDED**
*   **Hardware:** **Mac Mini M4 Pro** (Fully Spec'd).
*   **Config:** 96GB Unified Memory, 1TB SSD.
*   **LLM Capability:** **Llama 3 70B (Q4/Q5)** or **Qwen 2.5 72B**. These are "Pro-level" models.
*   **Performance:** ~10-12 tokens/sec on 70B models. Blazing fast (50+ t/s) on 8B-14B models.
*   **Office Fit:** Near silent. Fits under a monitor.
*   **Verdict:** The "sweet spot." Runs high-quality models with enough RAM for long contexts (128k).

### Option C: Serious (~$5,000–$8,000)
*   **Hardware:** **Mac Studio M4 Ultra**.
*   **Config:** 192GB Unified Memory.
*   **LLM Capability:** **DeepSeek R1 / V3 (Q4/Q5)**. Can run massive 400B+ models at low quantization.
*   **Performance:** ~15-20 tokens/sec on 70B models.
*   **Verdict:** For heavy developer use and high-concurrency internal APIs.

### Option D: Power (~$10,000+)
*   **Hardware:** **Dual Mac Studio M4 Ultra Cluster** (via Exo Labs).
*   **Config:** 384GB - 512GB Total Unified Memory.
*   **LLM Capability:** **Kimi K2.5 (1T params)** or **DeepSeek R1 (Full/FP16)**.
*   **Performance:** ~25-30 tokens/sec on world-class reasoning models.
*   **Verdict:** Rivals Claude Opus/GPT-5 in intelligence while remaining 100% local.

---

## 3. Mac vs PC for Local LLMs

| Feature | Apple Silicon (Mac) | NVIDIA RTX (PC) |
| :--- | :--- | :--- |
| **Memory Strategy** | **Unified Memory:** Up to 192GB+ accessible by GPU. | **VRAM:** Limited to 24GB per card (RTX 5090). |
| **Scaling** | Add more Macs via Exo Labs (Thunderbolt 5). | Add more GPUs (Limited by PCIe lanes/Power). |
| **Power/Heat** | High efficiency (Quiet, 100W). | Power hungry (Loud, 600W+). |
| **Software** | **MLX** (Native), llama.cpp, Ollama. | **vLLM**, TensorRT, CUDA (Industry standard). |
| **Cost per Token** | Cheaper for *large* models (High RAM). | Cheaper for *fast* models (High Compute). |

---

## 4. Best Open Models for Business (Feb 2026)

*   **DeepSeek R1 (Reasoning):** The current king of local reasoning. Rivals Opus for coding and logic.
*   **Kimi K2.5 (Multi-Modal/Reasoning):** 1T parameters, MoE architecture. Exceptional at following complex business instructions.
*   **Qwen 2.5 (72B/32B):** Best all-rounder for classification, analysis, and data extraction.
*   **Llama 3.x (Various):** Great ecosystem support; best for RAG and standard chat.
*   **Vision Models:** **Llama 3.2 Vision** or **Qwen-VL** for packing verification (checking images of shipped items).

---

## 5. Architecture: How It Works

1.  **Inference Engine:** Run **Ollama** or **vLLM** on the local machine. It exposes an OpenAI-compatible API.
2.  **Clawdbot Integration:** Update `gateway.config` to add a `custom` provider pointing to the local IP.
3.  **Hybrid Routing (The "Smart" Way):**
    *   *Routing Rule:* If Task = "Classification" or "Summarization" → **Local (Qwen 2.5)**.
    *   *Routing Rule:* If Task = "Strategic Planning" or "High-Stakes Coding" → **Cloud (Claude Opus)**.
4.  **Exo Labs:** If you outgrow one machine, buy a second and link them over Thunderbolt. Exo distributes the model weights across both, acting as a single large virtual GPU.

---

## 6. Final Recommendation

### **The Recommendation: Option B (Mac Mini M4 Pro 96GB)**
For Head Case Designs, a spec'd out Mac Mini is the most professional, cost-effective, and low-maintenance entry point.

**Phase 1: Setup (Month 1)**
*   Purchase Mac Mini M4 Pro (96GB RAM).
*   Install Ollama + DeepSeek R1 (quantized) for reasoning and Llama 3 8B for fast tasks.
*   Offload all RAG embedding generation to the local machine.

**Phase 2: Integration (Month 2-3)**
*   Connect CS Automation (n8n) to the local model for initial ticket sorting.
*   Move inventory data analysis locally (Privacy Win).

**Phase 3: Scale (Year 1+)**
*   If token demand exceeds 20k/day, add a second Mac Mini and use Exo Labs to form a cluster.

**Expected Savings:** ~$2,500/year in API costs while gaining the ability to process 10x more data without fear of the bill.

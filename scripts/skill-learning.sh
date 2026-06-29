#!/bin/bash
# Skill Learning Script - Version corregida
# Instala 1 skill nuevo del hub cada vez que se ejecuta, avanzando el índice
# Usage: bash /hermes-home/scripts/skill-learning.sh

HERMES="/opt/hermes/.venv/bin/hermes"
STATE_FILE="/hermes-home/skills/.skill-learning-state.json"
LOG_FILE="/hermes-home/skills/skill-learning.log"

# Priority order for skill selection (most relevant to David's profile first)
PRIORITY_SKILLS=(
    "duckduckgo-search:official/web/duckduckgo-search"
    "searxng-search:official/web/searxng-search"
    "scrapling:official/web/scrapling"
    "code-wiki:official/software-development/code-wiki"
    "rest-graphql-debug:official/web/rest-graphql-debug"
    "docker-management:official/devops/docker-management"
    "fastmcp:official/mcp/fastmcp"
    "outlines:official/software-development/outlines"
    "instructor:official/software-development/instructor"
    "stocks:official/finance/stocks"
    "qdrant-vector-search:official/mlops/qdrant-vector-search"
    "pinecone:official/mlops/pinecone"
    "chroma:official/mlops/chroma"
    "llava:official/mlops/llava"
    "whisper:official/media/whisper"
    "arxiv:official/research/arxiv"
    "blogwatcher:official/research/blogwatcher"
    "polymarket:official/research/polymarket"
    "huggingface-hub:official/mlops/huggingface-hub"
    "himalaya:official/email/himalaya"
    "airtable:official/productivity/airtable"
    "google-workspace:official/productivity/google-workspace"
    "maps:official/productivity/maps"
    "nano-pdf:official/productivity/nano-pdf"
    "notion:official/productivity/notion"
    "ocr-and-documents:official/productivity/ocr-and-documents"
    "powerpoint:official/productivity/powerpoint"
    "teams-meeting-pipeline:official/productivity/teams-meeting-pipeline"
    "openhue:official/smart-home/openhue"
    "xurl:official/social-media/xurl"
    "hermes-agent-skill-authoring:official/software-development/hermes-agent-skill-authoring"
    "plan:official/software-development/plan"
    "spike:official/software-development/spike"
    "systematic-debugging:official/software-development/systematic-debugging"
    "test-driven-development:official/software-development/test-driven-development"
    "requesting-code-review:official/software-development/requesting-code-review"
    "node-inspect-debugger:official/software-development/node-inspect-debugger"
    "python-debugpy:official/software-development/python-debugpy"
    "kanban-orchestrator:official/devops/kanban-orchestrator"
    "kanban-worker:official/devops/kanban-worker"
    "gif-search:official/media/gif-search"
    "llama-cpp:official/mlops/inference/llama-cpp"
    "vllm:official/mlops/inference/vllm"
    "evaluating-llms-harness:official/mlops/evaluation/lm-evaluation-harness"
    "weights-and-biases:official/mlops/evaluation/weights-and-biases"
    "audiocraft-audio-generation:official/mlops/models/audiocraft"
    "segment-anything-model:official/mlops/models/segment-anything"
    "obsidian:official/note-taking/obsidian"
    "youtube-content:official/media/youtube-content"
    "heartmula:official/media/heartmula"
    "songsee:official/media/songsee"
    "concept-diagrams:official/creative/concept-diagrams"
    "stable-diffusion-image-generation:official/creative/stable-diffusion-image-generation"
    "meme-generation:official/creative/meme-generation"
    "hyperframes:official/creative/hyperframes"
    "qmd:official/software-development/qmd"
    "siyuan:official/productivity/siyuan"
    "sherlock:official/osint/sherlock"
    "osint-investigation:official/research/osint-investigation"
    "domain-intel:official/research/domain-intel"
    "watchers:official/web/watchers"
    "1password:official/security/1password"
    "evm:official/blockchain/evm"
    "solana:official/blockchain/solana"
    "hyperliquid:official/finance/hyperliquid"
    "shopify:official/ecommerce/shopify"
    "shop-app:official/ecommerce/shop-app"
    "telephony:official/communication/telephony"
    "drug-discovery:official/research/drug-discovery"
    "bioinformatics:official/research/bioinformatics"
    "neuroskill-bci:official/computer-vision/neuroskill-bci"
    "slime-rl-training:official/mlops/slime-rl-training"
    "sparse-autoencoder-training:official/mlops/sparse-autoencoder-training"
    "tensorrt-llm:official/mlops/tensorrt-llm"
    "pytorch-fsdp:official/mlops/pytorch-fsdp"
    "pytorch-lightning:official/mlops/pytorch-lightning"
    "unsloth:official/mlops/unsloth"
    "peft-fine-tuning:official/mlops/peft-fine-tuning"
    "fine-tuning-with-transformers:official/mlops/fine-tuning-with-transformers"
    "huggingface-accelerate:official/mlops/huggingface-accelerate"
    "huggingface-tokenizers:official/mlops/huggingface-tokenizers"
    "lambda-labs-gpu-cloud:official/mlops/lambda-labs-gpu-cloud"
    "modal-serverless-gpu:official/mlops/modal-serverless-gpu"
    "nemo-curator:official/mlops/nemo-curator"
    "simpo-training:official/mlops/simpo-training"
    "optimizing-attention:official/mlops/optimizing-attention"
    "hermes-s6-container-runtime:official/devops/hermes-s6-container-runtime"
    "here.now:official/productivity/here-now"
    "blackbox:official/autonomous-ai-agents/blackbox"
    "antigravity-cli:official/autonomous-ai-agents/antigravity-cli"
    "grok:official/autonomous-ai-agents/grok"
    "parallel-cli:official/autonomous-ai-agents/parallel-cli"
    "mcporter:official/mcp/mcporter"
    "inference-sh-cli:official/mlops/inference-sh-cli"
    "kanban-video-orchestrator:official/devops/kanban-video-orchestrator"
    "openclaw-migration:official/migration/openclaw-migration"
    "blender-mcp:official/creative/blender-mcp"
    "3-statement-model:official/finance/3-statement-model"
    "dcf-model:official/finance/dcf-model"
    "lbo-model:official/finance/lbo-model"
    "merger-model:official/finance/merger-model"
    "excel-author:official/productivity/excel-author"
    "pptx-author:official/productivity/pptx-author"
    "fitness-nutrition:official/health/fitness-nutrition"
    "memento-flashcards:official/productivity/memento-flashcards"
    "one-three-one-rule:official/finance/one-three-one-rule"
    "guidance:official/software-development/guidance"
    "faiss:official/mlops/faiss"
    "pinggy-tunnel:official/devops/pinggy-tunnel"
    "page-agent:official/web/page-agent"
    "oss-forensics:official/research/oss-forensics"
    "adversarial-ux-test:official/dogfood/adversarial-ux-test"
    "agentmail:official/email/agentmail"
    "comps-analysis:official/finance/comps-analysis"
    "darwinian-evolver:official/autonomous-ai-agents/darwinian-evolver"
    "distributed-llm-pretraining:official/mlops/distributed-llm-pretraining"
    "clip:official/computer-vision/clip"
    "baoyu-article-illustrations:official/creative/baoyu-article-illustrations"
)

TOTAL=${#PRIORITY_SKILLS[@]}

# Load state using python3 (robust JSON handling)
load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        python3 -c "
import json, sys
try:
    with open('$STATE_FILE') as f:
        data = json.load(f)
    print(json.dumps(data))
except:
    print('{}')
" 2>/dev/null
    else
        echo '{"current_index": 0, "learned": [], "skipped": [], "last_error": null}'
    fi
}

# Save state (write atomically)
save_state() {
    local tmpfile="${STATE_FILE}.tmp.$$"
    echo "$1" > "$tmpfile"
    mv "$tmpfile" "$STATE_FILE"
}

# Main logic
main() {
    local state
    state=$(load_state)
    
    # Get current index
    local idx
    idx=$(echo "$state" | python3 -c "import sys,json; print(json.load(sys.stdin).get('current_index', 0))" 2>/dev/null)
    if [[ -z "$idx" || "$idx" == "None" ]]; then
        idx=0
    fi
    
    # Check if we've gone through all priority skills
    if [[ $idx -ge $TOTAL ]]; then
        echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] COMPLETED: All $TOTAL skills learned. Cycle finished." >> "$LOG_FILE"
        echo "DONE: All $TOTAL skills completed. Set to pause."
        # Mark as done
        python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
data['current_index'] = $TOTAL
data['completed'] = True
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null
        exit 0
    fi
    
    local skill_entry="${PRIORITY_SKILLS[$idx]}"
    local skill_name="${skill_entry%%:*}"
    local skill_id="${skill_entry##*:}"
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Next skill: $skill_name (index: $idx/$TOTAL)" >> "$LOG_FILE"
    
    # Install the skill
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Installing: $skill_name" >> "$LOG_FILE"
    local install_output
    install_output=$($HERMES skills install "$skill_id" 2>&1)
    local install_exit=$?
    
    if [[ $install_exit -ne 0 ]]; then
        echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] INSTALL FAILED for $skill_name: $install_output" >> "$LOG_FILE"
        echo "FAIL: $skill_name - $install_output"
        # Save error state and advance to avoid infinite loop
        python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
data['current_index'] = $((idx + 1))
data['last_error'] = 'install_failed'
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null
        exit 1
    fi
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Installed: $skill_name" >> "$LOG_FILE"
    
    # Update state - ALWAYS advance index
    python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
if 'learned' not in data:
    data['learned'] = []
if '$skill_name' not in data['learned']:
    data['learned'].append('$skill_name')
data['current_index'] = $((idx + 1))
data['last_error'] = None
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null
    
    echo "LEARNED: $skill_name (index: $((idx + 1))/$TOTAL)"
}

main "$@"

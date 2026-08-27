#!/bin/bash
# Diagnose stalled skill-learning cron jobs
# Usage: bash agent/skills/hub-skill-discovery/scripts/diagnose-stalled-skill.sh
#
# Checks:
# 1. Is the skill-learning state current_index stuck?
# 2. Are there skills in quarantine?
# 3. Has the same skill been reinstalled >3 times?
# 4. Provides fix commands.

STATE_FILE="agent/skills/.skill-learning-state.json"
LOG_FILE="agent/skills/skill-learning.log"
QUARANTINE_DIR="agent/skills/.hub/quarantine"

echo "=== Stalled Skill Diagnosis ==="
echo ""

# Check state file
if [[ ! -f "$STATE_FILE" ]]; then
    echo "❌ No state file found at $STATE_FILE"
    exit 1
fi

echo "📊 Current state:"
python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
print(f'  current_index: {data.get(\"current_index\", \"?\")}')
print(f'  learned: {data.get(\"learned\", [])}')
print(f'  skipped: {data.get(\"skipped\", [])}')
print(f'  last_error: {data.get(\"last_error\", \"none\")}')
"
echo ""

# Check quarantine
echo "📦 Quarantine contents:"
if [[ -d "$QUARANTINE_DIR" ]] && [[ "$(ls -A "$QUARANTINE_DIR" 2>/dev/null)" ]]; then
    for q in "$QUARANTINE_DIR"/*; do
        echo "  ⚠️  $(basename "$q")"
    done
else
    echo "  (empty)"
fi
echo ""

# Check for repeated installations in log
if [[ -f "$LOG_FILE" ]]; then
    echo "🔄 Repeated skill installations (last 48h):"
    python3 -c "
from collections import Counter
from datetime import datetime, timedelta
import re

with open('$LOG_FILE') as f:
    lines = f.readlines()

# Find 'Installing:' lines with timestamps
pattern = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC)\] Installing: (.+)')
recent_cutoff = datetime.utcnow() - timedelta(hours=48)
install_times = []

for line in lines:
    m = pattern.match(line.strip())
    if m:
        ts_str, skill = m.group(1), m.group(2)
        ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S UTC')
        if ts >= recent_cutoff:
            install_times.append((ts, skill))

if install_times:
    counts = Counter(s for _, s in install_times)
    for skill, count in counts.most_common():
        if count > 1:
            print(f'  ⚠️  {skill}: {count} times in last 48h')
            if count > 3:
                print(f'     🚨 STALLED — likely stuck in loop!')
else:
    print('  (none detected)')
"
fi
echo ""

# Fix suggestions
echo "🔧 Fix suggestions:"
echo "  1. If quarantine has items: move them or skip in state"
echo "  2. Advance index: edit current_index in $STATE_FILE"
echo "  3. To skip current: python3 -c \"import json; d=json.load(open('$STATE_FILE')); d['skipped'].append('SKILL_NAME'); d['current_index']+=1; json.dump(d,open('$STATE_FILE','w'),indent=2)\""

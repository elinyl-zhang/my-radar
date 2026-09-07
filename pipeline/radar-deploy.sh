#!/bin/bash
# radar-deploy.sh — My Radar 确定性部署层
#
# 职责：把 daily-feed.json 组装进 HTML 并部署到桌面。
# 这一层不调用任何 LLM，只包含确定性操作（校验 / 组装 / 回滚），
# 因此运行时间在 1-2 秒，不存在超时风险。
#
# 被两处调用：
#   1. launchd 每天早上 07:00（不依赖任何 app 在运行）
#   2. WorkBuddy automation 在生成完新 feed 之后
#
# 幂等：重复执行不会破坏任何东西。

set -u

PYTHON="${PYTHON:-/usr/bin/python3}"

# repo root = the directory above pipeline/
RADAR_HOME="${RADAR_HOME:-$(cd "$(dirname "$0")/.." && pwd)}"

PIPELINE="$RADAR_HOME/pipeline/radar-pipeline.py"
FEED="$RADAR_HOME/feed.json"
LOGDIR="$RADAR_HOME/logs"

mkdir -p "$LOGDIR"
LOG="$LOGDIR/radar-deploy.log"

TS=$(date '+%Y-%m-%d %H:%M:%S')
TODAY=$(date '+%Y-%m-%d')

# 读 feed 的日期（读不到就记为 ?）
FEED_DATE=$("$PYTHON" -c "import json,sys
try:
    print(json.load(open('$FEED')).get('date','?'))
except Exception:
    print('?')" 2>/dev/null)

if [ "$FEED_DATE" = "$TODAY" ]; then
  FRESHNESS="FRESH"
elif [ "$FEED_DATE" = "?" ]; then
  FRESHNESS="UNREADABLE"
else
  FRESHNESS="STALE($FEED_DATE)"
fi

{
  echo "[$TS] ── deploy start ──"
  echo "[$TS] feed.date=$FEED_DATE  today=$TODAY  →  $FRESHNESS"
} >> "$LOG"

# 前置检查：模板和管道脚本在不在
if [ ! -f "$PIPELINE" ]; then
  echo "[$TS] ABORT: 管道脚本不存在 $PIPELINE" >> "$LOG"
  echo "" >> "$LOG"
  exit 1
fi

if [ ! -f "$FEED" ]; then
  echo "[$TS] ABORT: feed 不存在 $FEED" >> "$LOG"
  echo "" >> "$LOG"
  exit 1
fi

# 跑管道（校验 → 备份 → 组装 → 校验输出 → 失败回滚）
"$PYTHON" "$PIPELINE" >> "$LOG" 2>&1
RC=$?

echo "[$TS] pipeline exit=$RC  freshness=$FRESHNESS" >> "$LOG"
echo "" >> "$LOG"

exit $RC

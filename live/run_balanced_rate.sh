#!/bin/bash
# run_balanced_rate.sh — publish balanced's signal for the family (read-only; writes only the regime/hurdle file).
# Skips cleanly if the shared data keys are absent. Manual: BB_DRYRUN=1 bash live/run_balanced_rate.sh
set -uo pipefail
REPO="/Users/malcolmx/blaquebaux-balanced"; ENVFILE="$HOME/.config/blaquebaux/alpaca.env"
LOGDIR="$REPO/logs"; mkdir -p "$LOGDIR"; LOG="$LOGDIR/balanced_rate_$(TZ=America/New_York date +%Y%m%d).log"
exec >> "$LOG" 2>&1
echo "======== $(TZ=America/New_York date '+%F %T %Z') balanced rate publish ========"
[ -f "$ENVFILE" ] && { set -a; source "$ENVFILE"; set +a; } || { echo "no $ENVFILE — skipping"; exit 0; }
[ -z "${ALPACA_KEY_ID:-}" ] && { echo "no ALPACA keys — skipping"; exit 0; }
/usr/bin/python3 "$REPO/live/balanced_rate_emitter.py"; RC=$?
echo "======== done rc=$RC $(TZ=America/New_York date '+%T %Z') ========"; exit $RC

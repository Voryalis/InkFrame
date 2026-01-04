#!/bin/sh
# InkFrame: random image rotation every 15 minutes, time-of-day buckets

BASE="/mnt/us/inkframe/images"
INTERVAL_SEC=900   # 15 minutes
LOG="/mnt/us/inkframe/inkframe.log"

mkdir -p "$(dirname "$LOG")"
echo "InkFrame starting at $(date)" >> "$LOG"

# Stop Kindle UI so it doesn't draw over the screen (dedicated frame mode)
if command -v initctl >/dev/null 2>&1; then
  initctl stop framework >/dev/null 2>&1
else
  stop framework >/dev/null 2>&1
fi

bucket_for_hour() {
  H="$1"  # 0..23
  if [ "$H" -ge 6 ] && [ "$H" -le 11 ]; then
    echo "morning"
  elif [ "$H" -ge 12 ] && [ "$H" -le 18 ]; then
    echo "day"
  else
    echo "night"
  fi
}

pick_random_file() {
  DIR="$1"
  COUNT=$(find "$DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) 2>/dev/null | wc -l)
  [ "$COUNT" -gt 0 ] || return 1

  IDX=$(od -An -N2 -tu2 /dev/urandom 2>/dev/null | tr -d ' ')
  IDX=$(( (IDX % COUNT) + 1 ))

  find "$DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) 2>/dev/null \
    | sed -n "${IDX}p"
}

while :; do
  HOUR=$(date +%H | sed 's/^0//')
  [ -z "$HOUR" ] && HOUR=0

  BUCKET=$(bucket_for_hour "$HOUR")
  DIR="$BASE/$BUCKET"

  FILE=$(pick_random_file "$DIR") || FILE=""

  # Fallback: if bucket folder empty/missing, pick from BASE directly
  if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Bucket '$BUCKET' empty; falling back to $BASE" >> "$LOG"
    FILE=$(pick_random_file "$BASE") || FILE=""
  fi

  if [ -n "$FILE" ] && [ -f "$FILE" ]; then
    echo "[$(date)] bucket=$BUCKET display=$FILE" >> "$LOG"
    eips -c
    eips -g "$FILE"
  else
    echo "[$(date)] No images found in $BASE or bucket folders" >> "$LOG"
  fi

  sleep "$INTERVAL_SEC"
done

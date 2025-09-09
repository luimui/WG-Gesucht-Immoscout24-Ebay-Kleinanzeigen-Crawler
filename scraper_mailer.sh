#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRAPER_DIR="$SCRIPT_DIR/ebay_kleinanzeigen"
TMP_FILE="$SCRAPER_DIR/body.tmp"
LOG_FILE="$SCRIPT_DIR/scraper_mailer.log"


while true; do
	sleep 5
	cd "$SCRAPER_DIR" || { echo "Failed to cd to $SCRAPER_DIR" | tee -a "$LOG_FILE"; continue; }
	python3 scraper.py > "$TMP_FILE"
	# Only send mail if there are new ads (body contains URLs)
	if grep -q "https://www.ebay-kleinanzeigen.de" "$TMP_FILE"; then
		count=$(grep -c "https://www.ebay-kleinanzeigen.de" "$TMP_FILE")
		subject="EBAY-KA $(date +"%F %T") | ${count} new apartments (350-950 EUR)"
		python3 "$SCRIPT_DIR/send_mail.py" "$subject" < "$TMP_FILE"
		printf "%s\n" "$(date +"%F %T")" | tee -a "$LOG_FILE"
		cat "$TMP_FILE" | tee -a "$LOG_FILE"
	fi
	rm -f "$TMP_FILE"
	cd "$SCRIPT_DIR"
done


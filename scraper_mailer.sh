#!/bin/bash
while sleep 5; do 

cd wg_gesucht && python scraper.py > body.tmp && cat body.tmp | ifne mail -s "WG_GESUCHT $(date) New Apartment" example@mail.com | cat body.tmp | ifne  printf "$(date +"%T")\n" && cat body.tmp && cd .. && 

cd ebay_kleinanzeigen && python scraper.py > body.tmp && cat body.tmp | ifne mail -s "EBAY-KA $(date) New Apartment" example@mail.com | cat body.tmp | ifne  printf "$(date +"%T")\n" && cat body.tmp && cd .. &&

cd immoscout24 && python scraper.py > body.tmp && cat body.tmp | ifne mail -s "IMMOSCOUT24 $(date) New Apartment" example@mail.com | cat body.tmp | ifne  printf "$(date +"%T")\n" && cat body.tmp && cd ..;

done


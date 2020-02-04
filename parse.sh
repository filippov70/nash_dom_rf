#!/usr/bin/env bash

region_ids="1551 1545"
target_url="https://наш.дом.рф/erogs-graphql"
export PATH=$PATH:/home/filippov/software/firefox # путь к geckodriver
##for r_id in ${region_ids} ; do
#curl -d "@request_t.json" -X POST -H "Content-Type: application/json" -o houses.json ${target_url}
./parse_json.py
##done


# https://erzrf.ru/novostroyki
target_url="https://erzrf.ru/erz-rest/api/v1/gk/list-map?region=moskva&regionKey=143443001&costType=1&sortType=cmxrating"

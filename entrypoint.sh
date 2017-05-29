#!/bin/bash

[ -e config.ini ] && rm config.ini

config=$(<config_template.ini);
config="${config//\%slack-api-key\%/$SLACK_KEY}";
config="${config//\%telegram-api-key\%/$TELEGRAM_KEY}";
printf '%s\n' "$config" >config.ini


exec "$@"

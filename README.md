# nem-slack-telegram

__1. config.ini__  
To get this bridge between slack and telegram going you need to adapt a few things.
You need to make a copy of config_template.ini and rename that copy to config.ini.
Insert your API-keys into config.ini.

Under docker it's autocreated using ENVironment variables:

    docker run -e "SLACK_KEY=foo" -e "TELEGRAM_KEY=bar" -e  -d --name slack-telegram-bot --restart=always slack-telegram-bot

__2. bridge.py__
In bridge.py you there is a variable called SLACK_CHANNEL_MATCHING.
Change the channel to your own channels. The keys are slack channels, the values are telegram channels.

__3. Docker__
+ Build docker: docker build -t slack-telegram-bot ./
+ Run docker: docker run -e "SLACK_KEY=foo" -e "TELEGRAM_KEY=bar" -e  -d --name slack-telegram-bot --restart=always slack-telegram-bot

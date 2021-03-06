'''
Created on 26.09.2015

@author: root
'''
import ConfigParser
import logging
import logging.config
import Queue
import threading
import time

from slack_coms import SlackManager
from telegram_coms import TelegramManager

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(pathname)s:%(funcName)s:%(lineno)d | %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },

    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
logging.config.dictConfig(LOGGING)

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

SLACK_TOKEN = Config.get('Token', 'Slack')
TELEGRAM_TOKEN = Config.get('Token', 'Telegram')


SLACK_PASS_BOTS = [u'B4ZFJAJCW']
SLACK_CHANNEL_MATCHING = {
    'C5K4S3JKE': -1001106499126,
}
TELEGRAM_CHANNEL_MATCHING = {tel_channel: slack_channel for slack_channel,
                             tel_channel in SLACK_CHANNEL_MATCHING.items()}


SLACK_EMO_MATCHING = {':stuck_out_tongue:': ':P',
                      ':smile:': ':D',
                      ':simple_smile:': ':)',
                      ':wink:': ';)', }

slack = SlackManager(SLACK_TOKEN, TELEGRAM_CHANNEL_MATCHING,
                     SLACK_EMO_MATCHING, SLACK_PASS_BOTS)
telegram = TelegramManager(TELEGRAM_TOKEN, SLACK_CHANNEL_MATCHING)

'''Queues are used to pass information between Threads. Duh!'''
slack_output_queue = Queue.Queue()
telegram_output_queue = Queue.Queue()


'''All threads are being created and started.'''
slack_listen_thread = threading.Thread(name='slack_listener',
                                       target=slack.listen_to_slack,
                                       args=(slack_output_queue,))
slack_listen_thread.setDaemon(True)
slack_listen_thread.start()

telegram_listen_thread = threading.Thread(name='telegram_listener',
                                          target=telegram.listen_to_telegram,
                                          args=(telegram_output_queue,))
telegram_listen_thread.setDaemon(True)
telegram_listen_thread.start()

slack_forward_thread = threading.Thread(name='slack_forwarder',
                                        target=slack.forward_to_slack,
                                        args=(telegram_output_queue, ))

slack_forward_thread.setDaemon(True)
slack_forward_thread.start()

telegram_forward_thread = threading.Thread(name='telegram_forwarder',
                                           target=telegram.forward_to_telegram,
                                           args=(slack_output_queue,))

telegram_forward_thread.setDaemon(True)
telegram_forward_thread.start()

if __name__ == '__main__':
    while True:
        try:
            message = 'Running Threads: ' + ', '.join(thread.name for
                                                      thread in
                                                      threading.enumerate())
            logging.info(message)
            # Wait a day before reposting the message
            time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.error(str(e))

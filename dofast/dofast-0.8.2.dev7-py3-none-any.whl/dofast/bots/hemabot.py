#!/usr/bin/env python
"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import random
from threading import local

import codefast as cf
from codefast.axe import axe
from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

import dofast
from dofast import api
from dofast.pipe import author


class Psycho:
    def __init__(self):
        cf.info('start Psycho TG bot.')
        self.bot_name = 'hemahema'
        self.text = ''

    def alarm(self, context: CallbackContext) -> None:
        """Send the alarm message."""
        job = context.job
        context.bot.send_message(job.context, text=self.text)

    def remove_job_if_exists(self, name: str, context: CallbackContext) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    def deepl(self, update: Update, context: CallbackContext) -> None:
        '''deepl trans'''
        text = ' '.join(context.args)
        result = api.deepl.translate(text)['translations'].pop()['text']
        update.message.reply_text(result)

    def set_timer(self, update: Update, context: CallbackContext) -> None:
        """Add a job to the queue."""
        chat_id = update.message.chat_id
        try:
            # args[0] should contain the time for the timer in seconds
            due = int(context.args[0])
            if due < 0:
                update.message.reply_text('Sorry we can not go back to future!')
                return

            job_removed = self.remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(self.alarm,
                                       due,
                                       context=chat_id,
                                       name=str(chat_id))

            text = 'Timer successfully set!'
            if job_removed:
                text += ' Old one was removed.'
            update.message.reply_text(text)

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set <seconds>')

    def unset(self, update: Update, context: CallbackContext) -> None:
        """Remove the job if the user changed their mind."""
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
        update.message.reply_text(text)

    def text_handler(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        text = update.message.text
        self.text = text
        cf.io.write(text, '/tmp/wechat.txt')
        # Back up message to cloud.
        dofast.api.bucket.upload('/tmp/wechat.txt')

        if api.textparser.match(['weather', '天气'], text):
            api.weather.draw_weather_image()
            update.message.reply_photo(open('/tmp/weather.png', 'rb'))

        elif api.textparser.match(['avatar', '头像'], text):
            api.avatar.random()
            update.message.reply_photo(open('/tmp/pyavatar.png', 'rb'))
            update.message.reply_text('Here is your new avatar, enjoy!')
            return

        elif api.textparser.is_parcel_arrived(text):
            chat_id = update.message.chat_id
            due_time = axe.today() + 'T' + '22:45'
            due = axe.diff(axe.now(), due_time, seconds_only=True)
            update.message.reply_text(
                'Msg received, alert at {} in {} seconds.'.format(
                    due_time, due))
            if due < 0:
                update.message.reply_text('Sorry we can not go back to future!')
                return

            context.job_queue.run_once(self.alarm,
                                       due,
                                       context=chat_id,
                                       name=str(chat_id))

        else:
            result = api.deepl.translate(text)['translations'].pop()['text']
            update.message.reply_text(result)

    def file_handler(self, update: Update, context: CallbackContext) -> None:
        ''' save phone to cloud
        # https://stackoverflow.com/questions/50388435/how-save-photo-in-telegram-python-bot
        '''
        if update.message.document:
            # uncompressed photo
            file_id = update.message.document.file_id
            file_type = update.message.document.mime_type.split('/')[-1]

        elif update.message.photo:
            ## compressed photo
            file_id = update.message.photo[-1].file_id
            file_type = 'jpeg'

        else:
            update.message.reply_text(
                'No photo nor ducument detected from {}'.format(
                    str(update.message)))
            return

        obj = context.bot.get_file(file_id)
        localfile = '.'.join([str(random.randint(111, 999)), file_type])
        obj.download(localfile)
        dofast.api.bucket.upload(localfile)
        cf.io.rm(localfile)
        update.message.reply_text(
            f"File {localfile} retrieved and uploaded to cloud.")

    def main() -> None:
        """Run bot
        update.message methods: https://docs.pyrogram.org/api/bound-methods/Message.reply_text
        """
        psy = Psycho()
        token = author.get(psy.bot_name)
        updater = Updater(token)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("set", psy.set_timer))
        dispatcher.add_handler(CommandHandler(("deepl", 'dpl'), psy.deepl))
        dispatcher.add_handler(CommandHandler("unset", psy.unset))
        dispatcher.add_handler(MessageHandler(Filters.text, psy.text_handler))
        dispatcher.add_handler(
            MessageHandler(Filters.document | Filters.photo, psy.file_handler))

        # Start the Bot
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    Psycho.main()

import matplotlib
import matplotlib.pyplot as plt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, Updater

import xperibot.utils as utils
matplotlib.use('Agg')


class ExpBot:
    def __init__(self, token, allowed_users):
        self.updater = Updater(token=token)

        self.dispatcher = self.updater.dispatcher
        self.allowed_users = allowed_users
        self.dispatcher.add_handler(
            CommandHandler('stop', self.stop, filters=Filters.user(username=allowed_users)))
        self.dispatcher.add_handler(CommandHandler(
            'start', self.start, run_async=True))

        self.dispatcher.add_handler(
            CommandHandler('raw_scalars', self.get_scalars))
        self.dispatcher.add_handler(
            CommandHandler('draw_scalars', self.get_scalars))
        self.dispatcher.add_handler(CallbackQueryHandler(self.get_scalars))

        self.bot = None
        self.id_chat = None

        self.scalar_dict = {}

        self.current_action = None
        self.selected_scalars = []

        self.current_experiment = None
        self.loop_len = None
        self.report_status = None

    def add_scalar(self, name, x, iteration):
        v = self.scalar_dict.setdefault(name, [])
        v.append((x, iteration))

    def get_scalars_keyboard(self):
        button_list = [InlineKeyboardButton(
            x, callback_data=x) for x in self.scalar_dict if x not in self.selected_scalars]
        keyboard = utils.accept_build_menu(button_list, n_cols=4)
        return InlineKeyboardMarkup(keyboard)

    def get_scalars(self, update, context):
        chat_id = update.effective_chat.id
        if self.current_action is None:
            self.current_action = update.message.text[1:]  # Deleting first '/'
            update.message.reply_text(
                'Scalars selection:', reply_markup=self.get_scalars_keyboard())
        else:
            query = update.callback_query
            query.answer()
            data = query.data
            if data == 'accept':
                if self.current_action == 'raw_scalars':
                    for scalar in self.selected_scalars:
                        value, iteration = self.scalar_dict[scalar][-1]
                        context.bot.send_message(
                            chat_id=chat_id, text="{} {}: {}".format(iteration, scalar, value))
                if self.current_action == 'draw_scalars':
                    fig, ax = plt.subplots(nrows=1, ncols=1)
                    for scalar in self.selected_scalars:
                        y, x = list(zip(*self.scalar_dict[scalar]))
                        ax.plot(x, y, label=scalar)
                    plt.legend()
                    fig.savefig("tmp.png", format='png')
                    plt.close(fig)
                    context.bot.send_photo(
                        chat_id=chat_id, photo=open("tmp.png", 'rb'))
                query.edit_message_text(text="Done")
                self.current_action = None
                self.selected_scalars = []
            elif data == 'cancel':
                self.current_action = None
                query.edit_message_text(text="Cancelled")
            else:
                self.selected_scalars.append(data)
                query.edit_message_text(text="Selected {}".format(
                    self.selected_scalars), reply_markup=self.get_scalars_keyboard())

    # UTILS FUNCS
    def start(self, update, context):
        self.bot = context.bot
        self.id_chat = update.effective_chat.id

    def send_message(self, message):
        self.bot.send_message(chat_id=self.id_chat, text=message)

    # EXPERIMENTS CONTROL
    def in_experiment(self, name):
        if self.id_chat is None or self.bot is None:
            print("Waiting for 'start' command")
            while self.id_chat is None or self.bot is None:
                pass
        self.current_experiment = name
        self.send_message(f"Starting experiment {name}")

    def loop(self, loop, report_status_every=10):
        self.loop_len = len(loop)
        self.report_status = report_status_every
        return loop

    def update_loop(self, iteration):
        if (iteration + 1) % self.report_status == 0:
            scalars_string = "\n".join(
                [f"{key}: {value[-1][0]:.2f}" for key, value in self.scalar_dict.items()])
            self.send_message(
                f"{iteration}/{self.loop_len} in {self.current_experiment}\n"+scalars_string)

    def out_experiment(self):
        self.send_message(f"Finished experiment {self.current_experiment}")

    # BOT CONTROL

    def start_bot(self):
        self.updater.start_polling()

    def idle_bot(self):
        self.updater.idle()

    def stop(self, update, context):
        self.updater.stop()

    #
    def __enter__(self):
        self.start_bot()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.idle_bot()


class Experiment:
    def __init__(self, bot) -> None:
        self.bot = bot

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.idle_bot()

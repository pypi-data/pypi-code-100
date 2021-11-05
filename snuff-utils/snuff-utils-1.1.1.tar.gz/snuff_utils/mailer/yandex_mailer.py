from .config import YANDEX_SMTP_SERVER
from .mailer import Mailer


class YandexMailer(Mailer):
    """
    Класс, реализующий библиотеку для отправки электронной почты с помощью яндекс
    """
    smtp_server = YANDEX_SMTP_SERVER

""" Модуль содержит основной класс для работы с AR (Gravity One) """

from qdk.main import QDK


class ARQDK(QDK):
    """ Основной класс для взаимодействия с AR Gravity One """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_status(self):
        """
        Извлечь статус AR.

        :return:
        """
        return self.execute_method('get_status', get_response=True)

    def start_car_protocol(self, info):
        """
        Начать заезд.

        :param info: Словарь с необходимой информацией.
        :return:
        """
        return self.execute_method('start_weight_round', info=info,
                                   get_response=True)

    def add_comment(self, record_id, comment):
        """
        Добавить комментарий к заезду.

        :param record_id: id записи.
        :param comment: Комментарий.
        :return:
        """
        return self.execute_method('add_comment', record_id=record_id,
                                   comment=comment, get_response=True)

    def operate_gate_manual_control(self, operation, gate_name):
        """
        Работа со шлагбаумами.

        :param operation: Название операции (close|open):
        :param gate_name: Имя шлагбаума (entry/exit)
        :return:
        """
        return self.execute_method('operate_gate_manual_control',
                                   operation=operation, gate_name=gate_name,
                                   get_response=True)

    def change_opened_record(self, record_id, auto_id, car_number, carrier,
                             trash_cat_id, trash_type_id, comment,
                             polygon=None):
        """
        Изменить открытую запись.

        :param record_id: id зписи.
        :param auto_id: id авто.
        :param car_number: гос. номер авто.
        :param carrier: id перевозчика.
        :param trash_cat_id: id категории груза.
        :param trash_type_id: id вида груза.
        :param comment: комментарий весовщика.
        :param polygon: id полигона.
        :return:
        """
        return self.execute_method('change_opened_record', record_id=record_id,
                                   auto_id=auto_id, car_number=car_number,
                                   carrier=carrier, trash_cat_id=trash_cat_id,
                                   trash_type_id=trash_type_id,
                                   comment=comment,
                                   polygon=polygon, get_response=True)

    def close_opened_record(self, record_id, time_out=None, alert='РЗ'):
        """
        Закрыть открытую запись.

        :param record_id: id записи.
        :param time_out: время выезда.
        :param alert: Алерт закрытия.
        :return:
        """
        return self.execute_method('close_opened_record', record_id=record_id,
                                   time_out=time_out, alert=alert,
                                   get_response=True)

    def get_unfinished_records(self):
        """
        Получить все незаконченные заезды (заезды без тары).

        :return:
        """
        return self.execute_method('get_unfinished_records', get_response=True)

    def get_health_monitor(self):
        """
        Получить состояние монитора здоровья.

        :return:
        """
        return self.execute_method('get_health_monitor', get_response=True)

    def try_auth_user(self, username, password):
        """
        Попытка аутентификации юзера.

        :param username: Логин пользователя.
        :param password: Пароль пользователя.
        :return:
        """
        return self.execute_method('try_auth_user', username=username,
                                   password=password, get_response=True)

    def capture_cm_launched(self):
        """
        Зафиксировать запуск СМ.

        :return:
        """
        return self.execute_method('capture_cm_launched', get_response=True)

    def capture_cm_terminated(self):
        """
        Зафиксировать завершение СМ.

        :return:
        """
        return self.execute_method('capture_cm_terminated', get_response=True)

    def get_history(self, time_start, time_end, what_time='time_in',
                    trash_cat=None, trash_type=None, carrier=None,
                    auto_id=None, polygon_object_id=None, alerts=None):
        """
        Получить историю заездов.

        :return:
        """
        return self.execute_method('get_history', time_start=time_start,
                                   time_end=time_end, what_time=what_time,
                                   trash_cat=trash_cat, trash_type=trash_type,
                                   carrier=carrier, auto_id=auto_id,
                                   polygon_object_id=polygon_object_id,
                                   alerts=alerts, get_response=True)

    def get_table_info(self, table_name, only_active=True):
        """
        Получить содержимое таблицы.

        :param table_name: Имя таблицы.
        :param only_active: Только активные записи?
        :return:
        """
        return self.execute_method('get_table_info', tablename=table_name,
                                   get_response=True)

    def get_last_event(self, auto_id):
        """
        Получить данные о последнем заезде авто.

        :param auto_id: ID авто.
        :return:
        """
        return self.execute_method('get_last_event', auto_id=auto_id,
                                   get_response=True)

    def restart_unit(self):
        return self.execute_method('restart_unit', get_response=True)

    def catch_orup_decline(self):
        return self.execute_method('capture_orup_decline', get_response=True)

    def catch_orup_accept(self):
        return self.execute_method('capture_orup_accept', get_response=True)

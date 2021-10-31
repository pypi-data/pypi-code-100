from pymeet.core.registry import Registry

from pymeet.core.game.server.message import GameActionMessage


class GameServer:
    @staticmethod
    def request_connection(client_id: str, ip_address: str, name: str):
        reg = Registry()
        reg.game.push_joining_notification(
            requester_name=name,
            ip_address=ip_address,
            on_accepted=lambda _: reg.message_server.accept_connection(client_id),
            on_declined=lambda _: reg.message_server.decline_connection(client_id),
        )

    def update(self):
        self._process_remote_messages()
        self._process_local_messages()
        self._update_characters()

    def _update_characters(self):
        reg = Registry()
        reg.character_repository.update_all()

    def _process_remote_messages(self):
        reg = Registry()
        messages = reg.remote_message_queue.pop_all()
        for message in messages:
            if not isinstance(message, GameActionMessage):
                continue
            ...

    def _process_local_messages(self):
        reg = Registry()
        messages = reg.local_message_queue.pop_all()
        for message in messages:
            if not isinstance(message, GameActionMessage):
                continue

            message.action.apply()

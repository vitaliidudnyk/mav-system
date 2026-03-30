from insmav.streams.shared.base_handler import BaseHandler
from insmav.streams.rpc.pending_commands import PendingCommands


class AckHandler(BaseHandler):
    def __init__(self, pending_commands: PendingCommands):
        self._pending_commands = pending_commands

    @property
    def message_type(self) -> str:
        return "COMMAND_ACK"

    def handle(self, message) -> None:
        self._pending_commands.resolve(message.command, message)
from src.insmav.handlers.base_handler import BaseHandler
from src.insmav.rpc.pending_commands import PendingCommands


class AckHandler(BaseHandler):
    def __init__(self, pending_commands: PendingCommands):
        self._pending_commands = pending_commands

    def handle(self, message) -> None:
        if message.get_type() != "COMMAND_ACK":
            return

        self._pending_commands.resolve(message.command, message)
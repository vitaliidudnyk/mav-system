from venv import logger

from src.insmav.rpc.pending_commands import PendingCommands


class ReliableRpcSender:
    def __init__(
        self,
        mavlink_sender,
        pending_commands: PendingCommands,
        ack_timeout: float = 1.0,
        max_retries: int = 3,
    ):
        self._mavlink_sender = mavlink_sender
        self._pending_commands = pending_commands
        self._ack_timeout = ack_timeout
        self._max_retries = max_retries

    def send(self, message) -> None:
        if not self._requires_ack(message):
            self._mavlink_sender.send(message)
            return

        command = message.command
        original_confirmation = getattr(message, "confirmation", 0)

        self._pending_commands.register(command)

        try:
            for attempt in range(self._max_retries + 1):
                message.confirmation = original_confirmation + attempt
                self._mavlink_sender.send(message)

                ack = self._pending_commands.wait_for_ack(
                    command=command,
                    timeout=self._ack_timeout,
                )

                if ack is not None:
                    return

            logger.warning(
                f"COMMAND_ACK was not received for command {command} "
                f"after {self._max_retries + 1} attempts"
            )
            return
        finally:
            message.confirmation = original_confirmation
            self._pending_commands.clear(command)

    def _requires_ack(self, message) -> bool:
        message_type = message.get_type()

        return message_type in {
            "COMMAND_LONG",
            "COMMAND_INT",
        }
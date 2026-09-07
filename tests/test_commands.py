import unittest

from src.app_config import AppConfig
from src.core.chat_message import ChatMessage
from src.core.commands import CommandOutcome, evaluate_command


def make_config(**overrides) -> AppConfig:
    cfg = AppConfig()
    for key, value in overrides.items():
        setattr(cfg, key, value)
    return cfg


class EvaluateCommandTests(unittest.TestCase):
    def test_regular_message_is_not_a_command(self):
        cfg = make_config()
        msg = ChatMessage(username="viewer", text="hello chat")
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.NOT_A_COMMAND)

    def test_mod_can_skip(self):
        cfg = make_config()
        msg = ChatMessage(username="mod1", text="!skip", is_mod=True)
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)

    def test_broadcaster_can_skip(self):
        cfg = make_config()
        msg = ChatMessage(username="streamer", text="!skip", is_broadcaster=True)
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)

    def test_regular_viewer_cannot_skip_by_default(self):
        cfg = make_config()
        msg = ChatMessage(username="viewer", text="!skip")
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_DENIED)

    def test_mod_only_flag_disabled_allows_anyone(self):
        cfg = make_config(mod_only_skip=False)
        msg = ChatMessage(username="viewer", text="!skip")
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)

    def test_command_is_case_insensitive(self):
        cfg = make_config()
        msg = ChatMessage(username="mod1", text="!SKIP", is_mod=True)
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)

    def test_unknown_command_is_ignored(self):
        cfg = make_config()
        msg = ChatMessage(username="viewer", text="!discord")
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.UNKNOWN_COMMAND)

    def test_custom_prefix(self):
        cfg = make_config(command_prefix=".")
        msg = ChatMessage(username="mod1", text=".skip", is_mod=True)
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)

    def test_custom_skip_command_name(self):
        cfg = make_config(skip_command="next")
        msg = ChatMessage(username="mod1", text="!next", is_mod=True)
        self.assertEqual(evaluate_command(msg, cfg), CommandOutcome.SKIP_REQUESTED)


if __name__ == "__main__":
    unittest.main()

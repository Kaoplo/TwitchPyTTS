import unittest

from src.twitch.irc_parse import (
    split_lines,
    parse_line,
    badges_from_tags,
    make_anonymous_nick,
)


class SplitLinesTests(unittest.TestCase):
    def test_single_complete_line(self):
        lines, remainder = split_lines("PING :tmi.twitch.tv\r\n")
        self.assertEqual(lines, ["PING :tmi.twitch.tv"])
        self.assertEqual(remainder, "")

    def test_multiple_lines_in_one_chunk(self):
        # This is the bug the old implementation had: a single recv() can
        # contain several PRIVMSGs, and only the first was ever processed.
        chunk = (
            ":a!a@a.tmi.twitch.tv PRIVMSG #ch :hello\r\n"
            ":b!b@b.tmi.twitch.tv PRIVMSG #ch :world\r\n"
        )
        lines, remainder = split_lines(chunk)
        self.assertEqual(len(lines), 2)
        self.assertEqual(remainder, "")

    def test_partial_line_is_kept_as_remainder(self):
        lines, remainder = split_lines(":a!a@a PRIVMSG #ch :hel")
        self.assertEqual(lines, [])
        self.assertEqual(remainder, ":a!a@a PRIVMSG #ch :hel")

    def test_remainder_is_stitched_with_next_chunk(self):
        first_lines, remainder = split_lines(":a!a@a PRIVMSG #ch :hel")
        second_lines, remainder2 = split_lines(remainder + "lo\r\n")
        self.assertEqual(first_lines, [])
        self.assertEqual(second_lines, [":a!a@a PRIVMSG #ch :hello"])
        self.assertEqual(remainder2, "")


class ParseLineTests(unittest.TestCase):
    def test_plain_privmsg(self):
        line = parse_line(":user123!user123@user123.tmi.twitch.tv PRIVMSG #channel :hello world")
        self.assertEqual(line.command, "PRIVMSG")
        self.assertEqual(line.username, "user123")
        self.assertEqual(line.params, ["#channel"])
        self.assertEqual(line.trailing, "hello world")

    def test_tagged_privmsg_with_badges(self):
        raw = (
            "@badges=moderator/1,subscriber/12;display-name=Mod;id=abc-123 "
            ":mod!mod@mod.tmi.twitch.tv PRIVMSG #channel :stop"
        )
        line = parse_line(raw)
        self.assertEqual(line.tags["id"], "abc-123")
        self.assertEqual(line.username, "mod")
        is_mod, is_broadcaster = badges_from_tags(line.tags)
        self.assertTrue(is_mod)
        self.assertFalse(is_broadcaster)

    def test_broadcaster_badge_counts_as_mod(self):
        raw = "@badges=broadcaster/1 :streamer!s@s.tmi.twitch.tv PRIVMSG #channel :hi"
        line = parse_line(raw)
        is_mod, is_broadcaster = badges_from_tags(line.tags)
        self.assertTrue(is_mod)
        self.assertTrue(is_broadcaster)

    def test_message_with_colon_in_body(self):
        line = parse_line(":u!u@u PRIVMSG #channel :time is 10:30 : go")
        self.assertEqual(line.trailing, "time is 10:30 : go")

    def test_ping(self):
        line = parse_line("PING :tmi.twitch.tv")
        self.assertEqual(line.command, "PING")
        self.assertEqual(line.trailing, "tmi.twitch.tv")

    def test_empty_line_returns_none(self):
        self.assertIsNone(parse_line(""))


class NickTests(unittest.TestCase):
    def test_anonymous_nick_format(self):
        self.assertEqual(make_anonymous_nick(123456), "justinfan123456")


if __name__ == "__main__":
    unittest.main()

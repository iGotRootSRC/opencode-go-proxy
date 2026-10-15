"""Conversation affinity must survive turns across all supported API surfaces."""

import unittest

from opencode_go_proxy.opencode_session import resolve_opencode_session


class SessionAffinityTests(unittest.TestCase):
    def test_equivalent_opening_representations_keep_affinity(self):
        expected = resolve_opencode_session({}, {"input": "Debug app A"})
        for opening in (
            {"role": "user", "content": "Debug app A"},
            {"type": "message", "role": "user", "content": "Debug app A"},
            {
                "role": "user",
                "content": [{"type": "input_text", "text": "Debug app A"}],
            },
            {"role": "user", "content": [{"type": "text", "text": "Debug app A"}]},
        ):
            self.assertEqual(
                expected, resolve_opencode_session({}, {"input": [opening]})
            )

    def test_followup_keeps_initial_affinity(self):
        for field in ("input", "messages"):
            with self.subTest(field=field):
                opening = {"role": "user", "content": "Debug app A"}
                first = {field: [opening]}
                followup = {
                    field: [
                        opening,
                        {"role": "assistant", "content": "What error?"},
                        {"role": "user", "content": "It crashes"},
                    ]
                }
                self.assertEqual(
                    resolve_opencode_session({}, first),
                    resolve_opencode_session({}, followup),
                )

    def test_distinct_openings_have_distinct_affinity(self):
        for field in ("input", "messages"):
            with self.subTest(field=field):
                first = {field: [{"role": "user", "content": "Debug app A"}]}
                other = {field: [{"role": "user", "content": "Debug app B"}]}
                self.assertNotEqual(
                    resolve_opencode_session({}, first),
                    resolve_opencode_session({}, other),
                )

    def test_explicit_session_overrides_history(self):
        for field in ("input", "messages"):
            self.assertEqual(
                resolve_opencode_session(
                    {"x-opencode-session": "thread-1"}, {field: []}
                ),
                "thread-1",
            )

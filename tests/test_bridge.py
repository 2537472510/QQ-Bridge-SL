import unittest

from qq_dsh_bridge import BridgeMessage, QQDSHBridge


class QQDSHBridgeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bridge = QQDSHBridge()

    def test_from_qq_event_to_dsh_payload(self) -> None:
        message = self.bridge.from_qq_event({"user_id": 123, "group_id": 456, "message": "hello"})
        self.assertEqual(message, BridgeMessage(platform="qq", user_id="123", content="hello", channel_id="456"))

        payload = self.bridge.to_dsh_payload(message)
        self.assertEqual(payload, {"source": "qq", "sender": "123", "content": "hello", "channel": "456"})

    def test_from_dsh_event_to_qq_payload(self) -> None:
        message = self.bridge.from_dsh_event({"sender": "alice", "channel": "room-1", "content": "hi"})
        self.assertEqual(message, BridgeMessage(platform="dsh", user_id="alice", content="hi", channel_id="room-1"))

        payload = self.bridge.to_qq_payload(message, target_group_id="7788")
        self.assertEqual(
            payload,
            {"message_type": "group", "group_id": "7788", "message": "[dsh] alice: hi"},
        )

    def test_empty_messages_raise(self) -> None:
        with self.assertRaises(ValueError):
            self.bridge.from_qq_event({"user_id": 1, "message": "  "})

        with self.assertRaises(ValueError):
            self.bridge.from_dsh_event({"sender": "a", "content": ""})


if __name__ == "__main__":
    unittest.main()

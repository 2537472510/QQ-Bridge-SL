from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BridgeMessage:
    platform: str
    user_id: str
    content: str
    channel_id: str | None = None


class QQDSHBridge:
    """Minimal payload bridge between QQ events and DSH events."""

    def from_qq_event(self, event: dict[str, Any]) -> BridgeMessage:
        content = str(event.get("message") or event.get("raw_message") or "").strip()
        if not content:
            raise ValueError("QQ event has no message content")

        return BridgeMessage(
            platform="qq",
            user_id=str(event.get("user_id", "unknown")),
            content=content,
            channel_id=(str(event["group_id"]) if "group_id" in event else None),
        )

    def to_dsh_payload(self, message: BridgeMessage) -> dict[str, str]:
        payload = {
            "source": message.platform,
            "sender": message.user_id,
            "content": message.content,
        }
        if message.channel_id:
            payload["channel"] = message.channel_id
        return payload

    def from_dsh_event(self, event: dict[str, Any]) -> BridgeMessage:
        content = str(event.get("content") or "").strip()
        if not content:
            raise ValueError("DSH event has no message content")

        return BridgeMessage(
            platform="dsh",
            user_id=str(event.get("sender") or "unknown"),
            content=content,
            channel_id=(str(event["channel"]) if "channel" in event else None),
        )

    def to_qq_payload(self, message: BridgeMessage, *, target_group_id: str) -> dict[str, str]:
        return {
            "message_type": "group",
            "group_id": str(target_group_id),
            "message": f"[{message.platform}] {message.user_id}: {message.content}",
        }

import datetime
import json
from pathlib import Path

from opencode_go_proxy import meter


def test_unrepresentable_local_day_does_not_break_usage_summary():
    path = Path(meter.usage_events_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime(2026, 10, 15, tzinfo=datetime.UTC)
    events = [
        {"at": "0001-01-01T00:00:00+01:00", "totalTokens": 500},
        {"at": now.isoformat(), "totalTokens": 7},
    ]
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n")
    summary = meter.usage_summary(now)
    assert summary["todayTokens"] == 7
    assert summary["todayTurns"] == 1

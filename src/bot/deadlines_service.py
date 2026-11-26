from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _to_aware(dt):
    """Если у времени нет часового пояса, считаем его UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def format_deadlines(deadlines, now=None, tz_name="UTC"):
    """Собирает текст ответа на команду /deadlines.

    deadlines - список словарей вида:
        {"title": "Курсовая", "due": datetime(...), "done": False}
    """
    tz = ZoneInfo(tz_name)
    now = _to_aware(now or datetime.now(timezone.utc))

    active = [d for d in deadlines if not d.get("done")]
    if not active:
        return "Активных дедлайнов нет."

    active.sort(key=lambda d: _to_aware(d["due"]))

    lines = ["Ваши дедлайны:"]
    for number, item in enumerate(active, start=1):
        due = _to_aware(item["due"])
        local = due.astimezone(tz)
        line = f"{number}. {item['title']} - {local:%d.%m.%Y %H:%M}"
        if due < now:
            line += " (просрочен)"
        lines.append(line)
    return "\n".join(lines)

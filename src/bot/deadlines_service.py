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

def parse_timezone(text):
    """Возвращает название часового пояса или None, если оно неверное.

    Пример: "Asia/Yekaterinburg"
    """
    name = text.strip()
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None
    return name


def parse_reminder_time(text):
    """Из "09:30" делает время. Если формат неверный, возвращает None."""
    try:
        return datetime.strptime(text.strip(), "%H:%M").time()
    except ValueError:
        return None

_timezones = {}
_remind_times = {}


def save_timezone(user_id, name):
    _timezones[user_id] = name


def save_remind_time(user_id, t):
    _remind_times[user_id] = t

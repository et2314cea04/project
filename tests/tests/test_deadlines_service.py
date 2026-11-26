from datetime import datetime, timezone

from src.bot.deadlines_service import format_deadlines  # поправьте под ваш стиль

NOW = datetime(2026, 12, 1, 12, 0, tzinfo=timezone.utc)


def test_empty_list():
    assert format_deadlines([], now=NOW) == "Активных дедлайнов нет."


def test_done_deadline_is_hidden():
    items = [{"title": "Сделано", "due": NOW, "done": True}]
    assert format_deadlines(items, now=NOW) == "Активных дедлайнов нет."


def test_sorted_and_overdue_marked():
    items = [
        {"title": "Поздний", "due": datetime(2026, 12, 10, 9, 0, tzinfo=timezone.utc)},
        {"title": "Прошлый", "due": datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)},
    ]
    text = format_deadlines(items, now=NOW)
    assert text.index("Прошлый") < text.index("Поздний")
    assert "(просрочен)" in text

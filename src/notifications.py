from datetime import datetime, timedelta, timezone, time, tzinfo
from database.models import User
from database.operations import get_users
from setup import bot

notification_message = """Вы давно не тренировались
Это не займет много времени
/create_test - создайте тест
/take_test - пройдите уже созданный тест
/train - режим тренировки"""

am_10 = time(10, 0)
pm_10 = time(22, 0)

async def notify_users():
    now = datetime.now().time()
    if not (am_10 <= now <= pm_10): return
    users = await get_users()
    for user in users:
        diff = datetime.now(timezone.utc) - user.last_activity.replace(tzinfo=timezone.utc)
        if diff > timedelta(minutes=1):
            await bot.send_message(user.id, notification_message)

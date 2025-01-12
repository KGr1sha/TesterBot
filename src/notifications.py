from datetime import datetime, timedelta, timezone, time 
from database.operations import get_users, update_user_activity
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
        if diff > timedelta(hours=24):
            await bot.send_message(user.id, notification_message)
            await update_user_activity(user.id) # so that notifications are sent once a day

#TODO: отнятие от баланса
from datetime import datetime, timedelta
import calendar


async def calculateLimitTillNextMonth(balance):
    # Получаем сегодняшнюю дату
    Today = datetime.utcnow().date()

    # Определяем следующий месяц
    year = Today.year
    month = Today.month + 1

    # Если следующий месяц — январь, увеличиваем год
    if month > 12:
        month = 1
        year += 1

    # Создаём дату для первого числа следующего месяца
    NextMonthFirstDay = datetime(year, month, 1).date()
    DaysTillNextMonth = (NextMonthFirstDay - Today).days

    everydayLimit = balance / DaysTillNextMonth

    return everydayLimit

async def minus(balance, value):
    return balance - value

async def plus(balance, value):
    return balance + value

from datetime import datetime, date, timedelta


def string_to_date(date_string:str):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def date_to_string(date):
    return date.strftime("%Y.%m.%d")


def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()

    print(f"\nUser list from bday function: {users}")

    for user in users.values():

        print(f"\nUser object: {user}\n")
        print(f"User Birthday property: {user.birthday}\n")

        birthday_this_year = user.birthday.value.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = user.birthday.replace(year = today.year + 1)
        """
        Додайте на цьому місці перевірку, чи не буде 
        припадати день народження вже наступного року.
        """
        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)
            """ 
            Додайте перенесення дати привітання на наступний робочий день,
            якщо день народження припадає на вихідний. 
            """
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": user.name, "congratulation_date": congratulation_date_str})
    return upcoming_birthdays

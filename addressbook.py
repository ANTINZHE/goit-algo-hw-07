from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    """ Базовий клас для полів запису """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """ Клас для зберігання імені контакту """
    def __init__(self, value):
        cleaned = value.replace(" ", "")
        if not cleaned.isalpha():
            raise ValueError("Name can only contain letters")
        super().__init__(value)


class Phone(Field):
    """ Клас для зберігання номера телефону """
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    """ Клас для зберігання інформації про контакт """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """ Метод додавання номеру телефона """
        self.phones.append(Phone(phone))

    def add_birthday(self, date_str):
        """ Метод додавання дня народження """
        self.birthday = Birthday(date_str)

    def remove_phone(self, phone):
        """ Метод видалення номеру телефона"""
        phone = self.find_phone(phone)
        if phone:
            self.phones.remove(phone)
            return
        raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        """ Метод редагування номеру телефона """
        phone = self.find_phone(old_phone)
        if phone:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
            return
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        """ Метод пошуку за номером телефона"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{bday}"


class AddressBook(UserDict):
    """ Клас для зберігання та управління записами """
    def add_record(self, record):
        """ Додавання запису до self.data """
        self.data[record.name.value] = record

    def find(self, name):
        """ Метод знаходження запису за іменем """
        record = self.data.get(name)
        if record:
            return record
        return None

    def delete(self, name):
        """ Метод видалення запису """
        if name in self.data:
            return self.data.pop(name)
        raise KeyError("Record not found")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = date.today()

        for record in self.values():
            if record.birthday is None:
                continue

            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)

            # Якщо ДН уже було цього року, переносимо на наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta = (birthday_this_year - today).days
            if 0 <= delta <= 7:
                congratulation_date = birthday_this_year

                # Якщо це субота або неділя → переносимо на понеділок
                if congratulation_date.weekday() in (5, 6):
                    days_to_monday = 7 - congratulation_date.weekday()
                    congratulation_date = congratulation_date + timedelta(days=days_to_monday)

                upcoming_birthdays.append(
                    f"{record.name.value}: {congratulation_date.strftime('%d.%m.%Y')}"
                )

        return upcoming_birthdays
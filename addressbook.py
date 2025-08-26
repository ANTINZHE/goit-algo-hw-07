from collections import UserDict
from datetime import datetime

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
        pass

# # Створення нової адресної книги
# book = AddressBook()
#
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
#
# # Додавання запису John до адресної книги
# book.add_record(john_record)
#
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
#
# # Виведення всіх записів у книз
#
# print(book)
#
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
#
# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
#
# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555
#
# # Видалення запису Jane
# book.delete("Jane")
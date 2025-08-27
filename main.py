from addressbook import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Record does not exist"
    return inner

@input_error
def parse_input(user_input):
    """ Функція розбиття введеного рядку """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    """ Функція додавання контакту """
    name, phone, *_ = args
    record = book.find(name)
    massage = "Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        massage = "Contact added"
    record.add_phone(phone)
    return massage

@input_error
def add_birthday(args, book):
    name, date_str = args
    record = book.find(name)
    record.add_birthday(date_str)
    return "Birthday added"

@input_error
def change_contact(args, book):
    """ Функція зміни контакту """
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact update"

@input_error
def show_phone(args, book):
    """ Функція відображення телефону """
    name = args[0] # Якщо не ввести args, то виведе помилку IndexError
    record = book.find(name)
    return f"{', '.join(p.value for p in record.phones)}"

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record.birthday is None:
        return f"Birthday not set for {name}"
    return f"Birthday for {name}: {record.birthday}"

@input_error
def show_all(book):
    """ Функція відображення усіх контактів """
    return book

@input_error
def birthdays(book):
    records = book.get_upcoming_birthdays()
    if not records:
        return "No upcoming birthdays"
    return "\n".join(records)

def main():
    """ Головна функція """
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Використав match, так як це зрозуміліше ніж if elif else :)
        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "all":
                print(show_all(book))
            case "birthdays":
                print(birthdays(book))
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()
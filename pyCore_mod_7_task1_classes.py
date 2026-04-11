from collections import UserDict
from datetime import datetime, date, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        self._value = value

class Birthday(Field):
    def __init__(self, value:str):
        try:
            value = re.sub(r"(\d{2}).(\d{2}).(\d{4})", r"\1-\2-\3", value) # validate input
            value = datetime.strptime(value, "%d-%m-%Y").date() # convert string to date            
            self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone_value:str):
        for p in self.phones:
            if phone_value == p.value:
                return p #phone object
        else:
            return None
    
    def add_phone(self, phone_value:Phone): #add phone to list
        if not self.find_phone(phone_value):
            self.phones.append(Phone(phone_value))
        else:
            raise ValueError("Such phone already exists")

    def remove_phone(self, phone_value:str):
        phone_obj = self.find_phone(phone_value)
        if phone_obj:
                self.phones.remove(phone_obj)
        else: 
            raise ValueError("Phone Not Found")
    
    def edit_phone(self, phone_value:str, phone_new:str):
        phone_obj = self.find_phone(phone_value)
        if phone_obj:
            phone_obj.value = phone_new
        else:
            raise ValueError("No such phone exists")

    def add_birthday(self, birthday_value:str):
        self.birthday = Birthday(birthday_value)

    def __str__(self):
        return f"Contact name: {self.name.value},\nBirthday: {self.birthday}\nPhones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name:str):
        self.data.pop(name, None)            

    def find(self, name:str):
        return self.data.get(name)
    
    def _string_to_date(self, date_string:str):
        return datetime.strptime(date_string, "%Y.%m.%d").date()

    def _date_to_string(self, date):
        return date.strftime("%Y.%m.%d")

    def _find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def _adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self._find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for contact in self.data.values():
            #rewrite birth year w current year
            birthday_this_year = contact.birthday.value.replace(year=today.year)

            # check if birthday already was this year
            if birthday_this_year < today: 
                # if so add year
                birthday_this_year = contact.birthday.replace(year = today.year + 1) 

            #if birthday is within 7 days from now
            if 0 <= (birthday_this_year - today).days <= days:

                # adjust congratulation date for weekends
                birthday_this_year = self._adjust_for_weekend(birthday_this_year) 

                #convert congrat date to string
                congratulation_date_str = self._date_to_string(birthday_this_year)

                #write contact names and congrat dates into array of dicts
                upcoming_birthdays.append({"name": contact.name, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "Empty"
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    def inner(*args, **kwargs):
        try: 
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide a name and a phone number."
        except KeyError:
            return "Please provide a valid contact name."
        except IndexError:
            return "Please provide a name."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone 
    return "Contact added"

@input_error
def change_contact(args, contacts):
    name, phone = args
    contacts[name]  #check if contact with such name exists
    contacts.update({name : phone})
    return f"Contact {name} updated with {phone} as new phone"

@input_error
def print_phone(args, contacts):
    name = args[0]
    return contacts[name]

@input_error    
def print_all_contacts(contacts):
    if len(contacts) == 0:
        return "No saved contacts"
    else:
        contacts_output = ""
        for name, phone in contacts.items():
            contacts_output += f"Contact Name: {name}, Phone Number: {phone}\n"
        return contacts_output


def main():


    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(print_phone(args, contacts))
        elif command == "all":
            print(print_all_contacts(contacts))
        else:
            print("Invalid command")   
    # record1 = Record("Viktor")
    # record2 = Record("Vasyl")

    # record1.add_birthday("11.04.2006")
    # record2.add_birthday("16.04.2007")

    # book = AddressBook()

    # book.add_record(record1)
    # book.add_record(record2)

    # print(book.get_upcoming_birthdays())

if __name__ == "__main__":
    main()
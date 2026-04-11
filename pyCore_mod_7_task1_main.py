from pyCore_mod_7_task1_classes import Record, AddressBook 

def input_error(func):
    def inner(*args, **kwargs):
        try: 
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input!"
        except KeyError:
            return "Please provide a valid contact name."
        except IndexError:
            return "Please provide a name."
    return inner

@input_error
def parse_input(user_input):
    # differentiate a command from arguments
    cmd, *args = user_input.split() 
    # make command lowercase to prevent errors
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book:AddressBook):
    name, phone, *_ = args
    record = book.find(name) #get the Record object
    message = "Contact updated"
    if not record: #if the object is empty
        record = Record(name) #create a new record
        book.add_record(record) #add it to addressbook
        message = "Contact added"
    if phone: 
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book:AddressBook):
    name, phone, phone_new, *_ = args
    record = book.find(name) #find the contact to be updated
    message = f"Contact {name} updated with phone {phone}" 
    if record: #if found update phone
        record.edit_phone(phone, phone_new)
    else: 
        message = "Error, phone not updated"
    return message

@input_error
def print_phone(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        # a string w phone values of a record separated by commas
        return f"{', '.join(phone.value for phone in record.phones)}" 
    return f"No phones found for record {name}"

@input_error    
def print_all_contacts(book:AddressBook):
    return book #book str method used for printing

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = f"Contact {name} already has a birthday on {record.return_birthday()}"
    if record.birthday is None:
        record.add_birthday(birthday)
        message = f"Birthday {birthday} added for contact {name}"
    return message
    
@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return record.return_birthday()

@input_error
def birthdays(book:AddressBook):
    # get a list of dictionaries with contact names and congratulation dates
    birthday_list_raw = book.get_upcoming_birthdays() 
    if birthday_list_raw:
        # a string to store names and dates in pretty format
        birthdays_refined = str() 
        for record_dict in birthday_list_raw:
            # get name and date values directly from dictionary
            birthdays_refined += f"Name: {record_dict['name']}, Congratulation Date: {record_dict['congratulation_date']}\n"
        return birthdays_refined
    return f"No contacts with birthdays within the next 7 days"


def main():
    book = AddressBook()
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
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":  
            print(print_phone(args, book))
        elif command == "all":
            print(print_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
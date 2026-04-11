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

if __name__ == "__main__":
    main()
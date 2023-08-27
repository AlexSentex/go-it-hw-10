from collections import UserDict
import time


class AddressBook(UserDict):
    '''AddressBook that contains names and numbers'''

    def __init__(self) -> None:
        
        self.data = {}

    def add_record(self, record):
        key = record.name.value
        self.data[key] = record


class Record:
    def __init__(self, name, phone=None) -> None:
        self.name = name
        self.phones = []
        if phone:
            if phone not in self.phones:
                self.phones.append(phone)

    def edit(self, phone_to_edit, new_phone):
        pass

class Field:
    pass


class Name(Field):
    '''Contains name'''
    def __init__(self, name) -> None:
        self.value = name


class Phone(Field):
    def __init__(self, phone) -> None:
        self.value = phone
        

class UsernameError(LookupError):
    '''Username not found!'''
class CommandError(LookupError):
    '''Undefined command'''
    
def input_error(handler: tuple) -> str:
    '''Return input error'''
    errors = {
        1: 'Enter valid command!',
        2: 'Username not found',
        3: 'Enter valid username and(or) phone (phone must contain only digits)',
        4: 'Number not found'
    }
    def trying(command: str, args) -> str:
        try:
            answer = handler(command, args)
        except UsernameError:
            return errors[2]
        except ValueError:
            return errors[4]
        except IndexError:
            return errors[3]
        except CommandError:
            return errors[1]
        except KeyError:
            return errors[2]
        return answer
    return trying

@input_error
def handler(command: str, args) -> str:
    '''Handle commands'''
    global ab

    def greet():
        return 'Hello!\nHow can I help you?'


    def add(name: str, phone='') -> str:
        '''Add user number into database'''
        if phone.isnumeric():
            phone = Phone(phone)

            if name in ab.keys():
                ab[name].phones.append(phone)
                return 'Done'
                
            name = Name(name)
            rec = Record(name, phone)
            ab[rec.name.value] = rec
            return 'Done'
        
        name = Name(name)
        rec = Record(name)
        ab[rec.name.value] = rec

        return 'Done'


    def change(name, old_number, new_number) -> str:
        '''Change user number'''

        if name not in ab.keys():
            raise UsernameError
        
        for phone in ab[name].phones:
            if phone.value == old_number:
                phone.value = new_number
                return 'Done'
        
        raise ValueError

    def show(user_input: tuple[str]) -> str:
        '''Show User phone.\n
        If key: 'all' - show all contacts'''

        if user_input[0] == 'all':
            title = '|{:^15}|{:^15}|\n'.format('Username', 'Phone')
            for username, rec in ab.items():
                if rec.phones:
                    title += '|{:^15}|{:^15}|\n'.format(
                                                        username.title(),
                                                        rec.phones[0].value
                                                        )
                    if len(rec.phones) == 1:
                        continue
                    for num in rec.phones[1:]:
                        title += '|{:^15}|{:^15}|\n'.format('', num.value)
                else:
                    title += '|{:^15}|{:^15}|\n'.format(username, ' ')
            return title
        
        phones = ''
        for phone in ab[user_input[0]].phones:
            phones += phone.value + '\n'

        return f'{user_input[0].title()}: {phones}'
    
    if command == 'hello':
        return greet()
    elif command == 'add':
        if len(args) > 1:
            return add(args[0], args[1])
        return add(args[0])
    elif command == 'change':
        return change(args[0], args[1], args[2])
    elif command == 'phone':
        return show(args)
    elif command == 'show':
        return show(args)
    raise CommandError
    
    

def parser(raw_input: str) -> str|tuple[str]:
    
    if raw_input == 'good bye' or\
       raw_input == 'close' or\
       raw_input == 'exit' or\
       raw_input == 'quit':
        print('Good bye!')
        time.sleep(3)
        return 'break'
    
    user_input = raw_input.split(' ')

    return tuple(user_input)

def main() -> None:
    """Main cycle"""
    while True:
        command = parser(input().lower())
        if command == 'break':
            break
        print(handler(command[0], command[1:]))


if __name__ == "__main__":
    ab = AddressBook()
    main()

from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
    
    def __str__(self):
        return str(self._value)

class Name(Field): 
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self._phone_valid()

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._phone_valid()

    def _phone_valid(self):
        if self._value is not None:
            if len(self._value) != 10 or not self._value.isdigit():
                raise ValueError("Incorrect number: phone must contain 10 digit!")

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self._bday_valid()
    
    def _bday_valid(self):
        if self.value is None:
            raise ValueError("No date of birth, should be YYYY-MM-DD")
        else:
            try:
                datetime.strptime(self.value, '%Y-%m-%d')
            except ValueError:
                #print("Date of birth should be YYYY-MM-DD")
                raise ValueError("Wrong format, date of birth should be YYYY-MM-DD")
        
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._bday_valid()
    
    def days_to_birthday(self):
        today = datetime.now()
        bday_date = datetime.strptime(self.value, '%Y-%m-%d')
        bday_upgreat = datetime(today.year, bday_date.month, bday_date.day)
        if today > bday_upgreat:
            bday_upgreat = datetime(today.year + 1, bday_date.month, bday_date.day)
        days_to_next_bday = (bday_upgreat - today).days
        return days_to_next_bday

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone._phone_valid()                 
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for element in self.phones:
            if element.value == phone_number:
                self.phones.remove(element)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                new_phone_check = Phone(new_phone)
                new_phone_check._phone_valid()
                phone.value = new_phone
                return       
        raise ValueError(f'{old_phone} not exist')

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"

class AddressBook(UserDict):
    def __iter__(self, pages_count):
        count = 0
        pages_now = []
        for record in self:
            pages_now.append(record)
            count += 1
            if count == pages_count:
                yield pages_now
                pages_now = []
                count = 0
            if pages_now:
                yield pages_now

    def add_record(self, record): 
        self.data[record.name.value] = record

    def find(self, name):
        result = self.data.get(name)
        return result
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

if __name__ == '__main__':
    book = AddressBook()

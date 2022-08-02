from collections import namedtuple

Person = namedtuple("Person", 
                        ['email','first_name', 'last_name', 'age'])

data={
    1: Person("johndoe@gmail.com", "John", "Doe", 23),
    2: Person("joe@gmail.com", "Joe", "Doe", 19),
    3: Person("harsh12@gmail.com", "Harsh", "Mishra", 19),
    4: Person("vaibhav@gmail.com", "Vaibhav", "Doe", 45)
}

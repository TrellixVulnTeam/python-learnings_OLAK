def p_decorate(func):
    def func_wrapper(self):
        return "<p>{0}</p>".format(func(self))

    return func_wrapper


class Person():
    def __init__(self):
        self.name = "Rajesh"
        self.family = "Venkataraman"

    @p_decorate
    def get_fullname(self):
        return self.name + " " + self.family


my_person = Person()
print(my_person.get_fullname())

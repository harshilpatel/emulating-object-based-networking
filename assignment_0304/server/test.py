
class A:
    def __init__(self):
        self.value = "a"

    def print_value(self):
        print self.value

    def get_value(self, a, b):
        return a+b
    
    def __getattr__(self, name):
        print name

a = A()
# a.print_value()
# print getattr(a, 'value')
print getattr(a, 'get_value')(1,3)
# a.print_output
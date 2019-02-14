

class A:
    def __getattr__(self, attr):
        upper_func = lambda *args, **kwargs: args[0].upper()
        return upper_func

a = A()
print a.upper("abc")
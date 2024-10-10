class A:
    def test(self):
        print("a")

class B:
    def show(self,object):
        object.test()

a = A()
b = B()
b.show(a)

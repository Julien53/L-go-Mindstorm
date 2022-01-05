import time

class test:
    def test(msg):
        print(msg)

def function3(msg):
    print(msg)

def function2(msg):
    print(msg)

def function1(msg):
    print(msg)


tab = {
    0: function3,
    1: function2,
    2: function1,
    3: time.sleep,
    4: test.test,

    10: 100,
    11: 200,
    12: 300,
    13: 1,
    14:345


}

print(tab[2].__name__ + "(" + str(tab[12]) +")")

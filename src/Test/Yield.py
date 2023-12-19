class TYield():
    def Generator1(self):
        for i in range(10):
            yield i

    def Generator2(self):
        for i in ['one', 'two', 'three']:
            yield i



Yield = TYield()
for x in Yield.Generator1():
    print(x)

for x in Yield.Generator2():
    print(x)

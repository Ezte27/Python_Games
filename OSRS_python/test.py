a = ['a', 'e', 'i', 'o', 'u', '1', '2', '3', '4', '5']
b = "hohohohoho"
c = a.pop(len(a)//2 - 1)
print(a)
a.insert(len(a)//2, c)

print(a)
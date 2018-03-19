import hashlib

hasher = hashlib.md5()
with open('hi.txt', 'rb') as file:
    buf = file.read()
    hasher.update(buf)
print("Genaretd Hash Code for file is:",hasher.hexdigest())
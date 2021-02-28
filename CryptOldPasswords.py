password = 'yh3!V+a1G#'
chars = '+-*!&$#?=@</>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
key = ''


key_index = 0
new_password = ''
for i in key:
    for j in range(len(chars)):
        if i == chars[j]:
            key_index += j
key_index /= len(key)
key_index = int(key_index)
for i in password:  # first symbol in password
    for j in range(len(chars)):
        password_index = 0
        if i == chars[j]:
            password_index = j + key_index
            if password_index >= len(chars):
                password_index -= len(chars)
            new_password += chars[password_index]
print(new_password)

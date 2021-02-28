import random
import sqlite3

chars = '+-*!&$#?=@</>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
# connect to db
database = sqlite3.connect('passwords.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (service TEXT, login TEXT, password TEXT)""")


def generate_password():
    """
    create password given length
    """
    global chars
    password = ''
    length = input('Длина пароля ')
    try:
        len = int(length)
    except ValueError:
        print('Вы ввели не число\n')
        return
    for _ in range(len):
        password += random.choice(chars)
    return password


def crypt_password(password, key):
    """
    crypt password with key, that given from user
    """
    global chars
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
    return new_password


def decrypt_password(password, key):
    """
    decrypt password with key, that given from user
    """
    global chars
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
                password_index = j - key_index
                if password_index < 0:
                    password_index += len(chars)
                new_password += chars[password_index]
    return new_password


def get_user_data(func):
    """
    get service and login from user
    """

    def wrapper():
        """
        decorate function
        """
        global cursor
        cursor.execute("""SELECT service FROM passwords""")
        services = cursor.fetchall()
        # if not writings in db
        if not services:
            print("Нет ни одной уч. записи\n")
            return
        else:
            change = input('Вывести уч. записи y/n? ')
            if change == 'y':
                services = set(services)
                for i in services:
                    print(i[0])
            elif change == 'n':
                pass
            else:
                print('Неверная команда!')
                return
        service = input('От чего пароль? ')
        cursor.execute("""SELECT login FROM passwords WHERE service = ?""", (service,))
        logins = cursor.fetchall()
        # if not exists this login in db
        if not logins:
            print('Нет такой уч. записи\n')
            return
        print('Уч. записи в этом сервисе:')
        for i in logins:
            print(i[0])
        login = input('Логин ')
        # TODO не выводить запрос на ключ при удалении записи
        # key = None
        key = input('Ключ шифрования ')
        data = {'service': service, 'login': login, 'key': key}
        cursor.execute("""SELECT service FROM passwords WHERE service = ? AND login = ?""",
                       (data['service'], data['login']))
        if cursor.fetchone() is None:
            print('Нет такой уч. записи\n')
            return
        # run current function
        func(data)

    return wrapper


@get_user_data
def read_writing(data):
    global cursor
    cursor.execute("""SELECT password FROM passwords WHERE service = ? AND login = ? """,
                   (data['service'], data['login']))
    password = cursor.fetchone()
    decrypted_password = decrypt_password(password[0], data['key'])
    print(f'Пароль {decrypted_password}')
    database.commit()


def append_writing():
    global cursor
    service = input('От чего пароль? ')
    login = input('Логин ')
    key = input('Ключ шифрования ')
    if service is None and login is None:
        print('Введите корректные данные\n')
        return
    cursor.execute("""SELECT password FROM passwords WHERE service = ? AND login = ?""", (service, login))
    if not cursor.fetchone() is None:
        print('Такая уч. запись уже существует\n')
    else:
        password = generate_password()
        try:
            encrypted_password = crypt_password(password, key)
        except TypeError:
            return
        cursor.execute("""INSERT INTO passwords(service, login, password) VALUES(?, ?, ?) """,
                       (service, login, encrypted_password))
        print(f'Пароль для {service} - {password}')
    database.commit()


@get_user_data
def rewrite_writing(data):
    global cursor
    change = input('Что поменять?(serv/log/pass) ')
    if change == 'serv':
        new_service = input('Новое название сервиса ')
        cursor.execute("""UPDATE passwords SET service = ? WHERE service = ? AND login = ? """,
                       (new_service, data['service'], data['login']))
        print(f'Новое название сервиса - {new_service}')
    elif change == 'log':
        new_login = input('Новый логин ')
        cursor.execute("""UPDATE passwords SET login = ? WHERE service = ? AND login = ? """,
                       (new_login, data['service'], data['login']))
        print(f'Новый логин - {new_login}')
    elif change == 'pass':
        ans = input('Вы уверены y/n? ')
        if ans == 'y':
            password = generate_password()
            try:
                encrypted_password = crypt_password(password, data['key'])
            except TypeError:
                return
            cursor.execute("""UPDATE passwords SET password = ? WHERE service = ? AND login = ? """,
                           (encrypted_password, data['service'], data['login']))
            print(f'Новый пароль - {password}')
        elif ans == 'n':
            print('Отмена ')
            return
        else:
            print('Неверная команда!')
            return
    else:
        print('Неверная команда ')
        return
    database.commit()


@get_user_data
def delete_writing(data):
    global cursor
    ans = input('Вы уверены y/n? ')
    if ans == 'y':
        cursor.execute("""DELETE FROM passwords WHERE service = ? AND login = ?""",
                       (data['service'], data['login']))
        print('Запись удалена!')
    elif ans == 'n':
        print('Отмена ')
        return
    else:
        print('Неверная команда!')
    database.commit()


if __name__ == '__main__':
    while True:
        mode = input(
            'Что вы хотите сделать? (r-посмотреть пароль, w-сгенерировать пароль, rw-поменять пароль, '
            'd-удалить пароль, q-выйти) ')
        if mode == 'w':
            append_writing()
        elif mode == 'r':
            read_writing()
        elif mode == 'rw':
            rewrite_writing()
        elif mode == 'd':
            delete_writing()
        elif mode == 'q':
            break
        else:
            print('Неверная команда ')

    cursor.close()

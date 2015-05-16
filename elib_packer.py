import getpass
import packer as p


packer = p.Packer()

print('Входим в библиотеку МИСиС')
username = input("логин--> ")
password = getpass.getpass("пароль--> ")
book_id = input("id книги--> ")
print('входим...')

try:
    packer.login(username, password)
    print('собираем pdf (относительно долгий процесс)...')
    packer.save_book(book_id)
    print('готово!')

except p.Packer_LoginError:
    print('Неправильный логин / пароль')

except p.Packer_BaseError:
    print('Неизвестная ошибка.')

finally:
    print('выходим...')
    packer.logout()

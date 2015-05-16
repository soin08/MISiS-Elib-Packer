import argparse
import packer as p

parser = argparse.ArgumentParser(description='Вход в библиотеку МИСиС')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('book_id')
args = parser.parse_args()

packer = p.Packer()

try:
    print('входим...')
    packer.login(args.username, args.password)
    print('собираем pdf (относительно долгий процесс)...')
    packer.save_book(args.book_id)

except p.Packer_LoginError:
    print('Неправильный логин / пароль')

except p.Packer_BaseError:
    print('Неизвестная ошибка.')

finally:
    print('выходим...')
    packer.logout()

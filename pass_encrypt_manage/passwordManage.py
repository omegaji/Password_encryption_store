from hashlib import sha256

def get_hexdigest(salt, plaintext):
    return sha256((salt + plaintext).encode('utf-8')).hexdigest()

SECRET_KEY = 's3cr3t'

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))

ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')

def password(plaintext, service, length=10):
    raw_hexdigest = make_password(plaintext, service)


    num = int(raw_hexdigest, 16)

    num_chars = len(ALPHABET)


    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(ALPHABET[idx])

    return ''.join(chars)

from peewee import *
import sqlite3
sqlite3.connect('accounts.db')

db = SqliteDatabase('accounts.db')

class Service(Model):
    name = CharField()
    length = IntegerField(default=8)
    symbols = BooleanField(default=True)
    alphabet = CharField(default='')

    class Meta:
        database = db

    def get_alphabet(self):
        if self.alphabet:
            return self.alphabet
        alpha = ('abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '0123456789')
        if self.symbols:
            alpha += '!@#$%^&*()-_'
        return alpha

    def password(self, plaintext):
        return password(plaintext, self.name, self.length)

    @classmethod
    def search(cls, q):
        return cls.select().where(cls.name ** ('%%%s%%' % q))
db.connect()
db.create_tables([Service], safe=True)
take_input=input("here enter your social site name for which you want to remember password\n")

new_pass=Service.create(name=take_input,length=8, symbols=True,alphabet=password('take_input','s3cr3t'))
new_pass.password('s3cr3t')
new_pass.alphabet=new_pass.password('s3cr3t')
print(new_pass.password('s3cr3t'))

curs=db.execute(Service.search('sd'))
for cur in curs:

    print(cur[4
    ])

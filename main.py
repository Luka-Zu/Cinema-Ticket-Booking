import sqlite3
import string
from random import random, randint

from fpdf import FPDF

class User:
    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        fee = seat.get_price()
        if card.validate(fee):
            if seat.is_free():
                card.pay(fee)
                print("SUCCESS")
                ticket = Ticket(self, fee, seat.get_seat())
                ticket.to_pdf()
            seat.occupy()





class Seat:
    database = "cinema.db"

    def __init__(self, seat_id):
        self.__seat_id = seat_id
        connection_with_database = sqlite3.connect(database=self.database)
        cursor = connection_with_database.cursor()
        cursor.execute(f"""
        SELECT  * FROM "Seat" WHERE seat_id = '{self.__seat_id}'
        """)
        result = cursor.fetchall()[0]

        self.__price = result[2]
        self.__is_available = (result[1] == 0)

        connection_with_database.close()

    def get_seat(self):
        return self.__seat_id
    def get_price(self):
        return self.__price

    def is_free(self):
        return self.__is_available

    def occupy(self):
        if self.is_free():
            connection_with_database = sqlite3.connect(database=self.database)
            connection_with_database.execute(f"""
                        UPDATE "Seat" SET "taken"=1 WHERE seat_id='{self.__seat_id}'    
                        """)
            self.__is_available = False
            connection_with_database.commit()
            connection_with_database.close()
            return True
        else:
            print("Seat is already occupied! ")
            return False


class Card:
    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.__holder = holder
        self.__cvc = cvc
        self.__number = number
        self.__type = type

    def validate(self, price):
        connection_with_database = sqlite3.connect(self.database)
        cursor = connection_with_database.cursor()
        cursor.execute(f"""
        SELECT * FROM "Card" WHERE number={self.__number}
        """)
        data = cursor.fetchall()[0]
        # print(data)
        actual_type = data[0]
        actual_cvc = data[2]
        actual_holder = data[3]
        amount = data[4]
        is_valid = True

        if actual_type != self.__type:
            is_valid = False
            print("Enter correct type for card")
        if actual_cvc != self.__cvc:
            is_valid = False
            print("Enter correct cvc")
        if actual_holder != self.__holder:
            is_valid = False
            print("Enter correct holder name")
        if amount <= price:
            is_valid = False
            print("Not enough money on account")
        connection_with_database.close()
        return is_valid

    def pay(self, price):
        connection_with_database = sqlite3.connect(self.database)
        cursor = connection_with_database.cursor()
        cursor.execute(f"""
                SELECT * FROM "Card" WHERE number={self.__number}
                """)
        amount = cursor.fetchall()[0][4]
        new_amount = amount - price
        connection_with_database.execute(f"""
                                UPDATE "Card" SET "balance"={new_amount} WHERE number='{self.__number}'    
                                """)
        connection_with_database.commit()
        connection_with_database.close()

class Ticket:

    def __init__(self, user, price, seat_number):
        self.seat_number = seat_number
        self.price = price
        self.user = user

    def to_pdf(self):

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family='Times', style='B', size=24)
        pdf.cell(w=0, h=80, txt='Your Digital Ticket', border=1, ln=1, align="C")

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Name: ', border=1)
        pdf.set_font(family='Times', style='', size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt='', border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Ticket ID: ', border=1)
        pdf.set_font(family='Times', style='', size=12)
        pdf.cell(w=0, h=25, txt=str(randint(1, 1000)), border=1, ln=1)
        pdf.cell(w=0, h=5, txt='', border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Price: ', border=1)
        pdf.set_font(family='Times', style='', size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt='', border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Seat Number: ', border=1)
        pdf.set_font(family='Times', style='', size=12)
        pdf.cell(w=0, h=25, txt=str(self.seat_number), border=1, ln=1)
        pdf.cell(w=0, h=5, txt='', border=0, ln=1)

        pdf.output('Ticket.pdf')


a = Seat('B3')

print(a.get_price())
print(a.is_free())

b = Card("Master Card", 23456789, '234', "Marry Smith")
print(b.validate(100))

u = User("jemali")
u.buy(a,b)
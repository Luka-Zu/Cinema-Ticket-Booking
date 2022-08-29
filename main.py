import sqlite3


class User:
    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        pass


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
        self.holder = holder
        self.cvc = cvc
        self.number = number
        self.type = type

    def validate(self, price):
        connection_with_database = sqlite3.connect(self.database)
        cursor = connection_with_database.cursor()
        cursor.execute(f"""
        SELECT * FROM "Card" WHERE number={self.number}
        """)
        data = cursor.fetchall()[0]
        print(data)
        actual_type = data[0]
        actual_cvc = data[2]
        actual_holder = data[3]
        amount = data[4]
        is_valid = True

        if actual_type != self.type:
            is_valid = False
            print("Enter correct type for card")
        if actual_cvc != self.cvc:
            is_valid = False
            print("Enter correct cvc")
        if actual_holder != self.holder:
            is_valid = False
            print("Enter correct holder name")
        if amount <= price:
            is_valid = False
            print("Not enough money on account")
        return is_valid
class Ticket:

    def __init__(self, user, price, seat_number):
        self.seat_number = seat_number
        self.price = price
        self.user = user

    def to_pdf(self):
        pass


#
# a = Seat('A1')
#
# print(a.get_price())
# print(a.is_free())
# print(a.occupy())

# b = Card("Master Card", 23456789, '234', "Marry Smith")
# print(b.validate(100))

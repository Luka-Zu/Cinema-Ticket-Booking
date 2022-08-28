# User:
# name
# buy(seat, card)

class User:
    pass


# Seat:
# database
# seat_id
# price
# is_free()
# occupy()

class Seat:
    pass



# Card:
# database
# type
# number
# cvc
# holder
# validate(price)

class Card:
    pass


# Ticket:
# id
# user
# price
# seat
# to_pdf(path)

class Ticket:
    pass
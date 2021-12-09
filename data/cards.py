import numpy as np

class Card():
    def __init__(self, name, wiki_name=None, tags=[]):
        self.name = name
        self.tags = tags
        self.wiki_name = self.name if wiki_name is None else wiki_name

    def __eq__(self, other):
        if type(other) is Card:
            return self.name == other.name
        else:
            return self.name == other

    def __str__(self):
        return self.name

class CardSet():
    def __init__(self, name, cards):
        self.name  = name
        self.cards = cards

rat = Card('rat')
tiger = Card('tiger')
rabbit = Card('rabbit')
dragon = Card('dragon')
snake = Card('snake')
sheep = Card('sheep')
monkey = Card('monkey')
chicken = Card('chicken')
pig = Card('pig')
animal_cards = CardSet('animals', [rat, tiger, rabbit, dragon,
                       snake, sheep, monkey, chicken, pig])

broccoli = Card('broccoli')
cabbage = Card('cabbage')
radish = Card('radish')
carrot = Card('carrot')
lettuce = Card('lettuce')
cauliflower = Card('cauliflower')
tomato = Card('tomato')
cucumber = Card('cucumber')
spinach = Card('spinach')
vegetable_cards = CardSet('vegetables', [broccoli, cabbage, radish,
                          carrot, lettuce, cauliflower, tomato,
                          cucumber, spinach])

earth = Card('earth')
water = Card('water')
fire = Card('fire')
air = Card('air')
zuko = Card('zuko')
appa = Card('appa', wiki_name='Appa_(character)')
aang = Card('aang')
katara = Card('katara', wiki_name='katara_(Avatar:_The_Last_Airbender)')
azula = Card('azula')

avatar_cards = CardSet('atla', [earth, water, fire, air, zuko,
                                appa, aang, katara, azula])

all_card_sets = [animal_cards, vegetable_cards, avatar_cards]

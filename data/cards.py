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

animal_cards = CardSet(
    "animals",
    [
        Card("rat"),
        Card("tiger"),
        Card("rabbit"),
        Card("dragon"),
        Card("snake"),
        Card("sheep"),
        Card("monkey"),
        Card("chicken"),
        Card("pig")
    ]
)

vegetable_cards = CardSet(
    "vegetables",
    [
        Card("broccoli"),
        Card("cabbage"),
        Card("radish"),
        Card("carrot"),
        Card("lettuce"),
        Card("cauliflower"),
        Card("tomato"),
        Card("cucumber"),
        Card("spinach"),
    ]
)

avatar_cards = CardSet(
    "atla",
    [
        Card("earth"),
        Card("water"),
        Card("fire"),
        Card("air"),
        Card("zuko"),
        Card("appa", wiki_name="Appa_(character)"),
        Card("aang"),
        Card("katara", wiki_name="katara_(Avatar:_The_Last_Airbender)"),
        Card("azula"),
    ],
)

all_card_sets = [
    animal_cards,
    vegetable_cards,
    avatar_cards
]

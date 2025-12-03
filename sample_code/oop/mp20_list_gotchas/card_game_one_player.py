from dealer import get_card
from player import Player

eric = Player('Eric')
eric.show_cards()

for _ in range(5):
    new_card = get_card()
    eric.hand.append(new_card)

eric.show_cards()

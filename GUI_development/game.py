import random
from strategy import probabilistic_bidding

# Define card values (dictionary for easy reference)
card_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "jack": 11,
    "queen": 12,
    "king": 13,
    "ace": 14
}

class Card:
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

  def get_value(self):
    return card_values[self.value]

class Player:
  def __init__(self, name):
    self.name = name
    self.deck = []  # Add deck attribute to store player's unique cards
    self.points = 0

  def draw_card(self):
    if len(self.deck) > 0:
        self.deck.pop()  # Draw from player's deck
    else:
      print(f"{self.name}'s deck is empty!")

  def bid(self):
    # Implement bidding strategy here (e.g., random choice, AI logic)
    chosen_card = random.choice(self.deck)
    #print(f"{self.name} bids: {chosen_card.value}")
    return chosen_card

  def update_points(self, round_points):
    self.points += round_points

class Banker:
  def __init__(self):
    self.diamond_deck = [Card("Diamonds", value) for value in card_values.keys()]
    random.shuffle(self.diamond_deck)  # Shuffle diamonds before dealing

  def generate_diamond_card(self):
    if len(self.diamond_deck) > 0:
      revealed_diamond = self.diamond_deck.pop()  # Draw and remove a diamond
      return revealed_diamond
    else:
      # Handle situation where all diamonds are used (game ends after this round)
      return None

class AI_player:
  def __init__(self, name = "AI Player" ):
    self.name = name
    self.deck = []  # Add deck attribute to store player's unique cards
    self.points = 0
    self.remaining_diamonds = []

    self.other_player_cards = dict()

  def draw_card(self):
    if len(self.deck) > 0:
        self.deck.pop()  # Draw from player's deck
    else:
      print(f"{self.name}'s deck is empty!")

  def observe(self, all_cards, other_players_cards, banker_cards ):

    def observe_other_players( all_cards : list , other_players_cards : dict ) -> None:
        for player, cards in other_players_cards.items():
            self.other_player_cards [ player ] = set(all_cards) - set(self.other_player_cards.get ( player, set() ) | set([cards]))

    observe_other_players( all_cards, other_players_cards )
    self.remaining_diamonds = banker_cards

  def bid(self):
    if self.other_player_cards is not None:
        chosen_card = probabilistic_bidding( self.deck , self.remaining_diamonds,
                                    [ cards for cards in self.other_player_cards.values()] )
        #print([ len(cards) for cards in self.other_player_cards.values()])
    else:
        chosen_card = random.choice(self.deck)

    #print(f"{self.name} bids: {chosen_card.value}")
    return chosen_card

  def update_points(self, round_points):
    self.points += round_points

all_cards = [Card(suit, value) for suit in ["Spades", "Hearts", "Clubs"] for value in card_values.keys()]
random.shuffle(all_cards)

def initialize_game(ai_player, num_players):
  # Create players, remove diamonds from deck, and distribute unique decks
  players = [Player(f"Player {i+1}") for i in range(num_players)]

  for index, player in enumerate(players + [ ai_player ]):
    #print(index)
    player.deck = all_cards [ index * 13 : (index + 1) * 13 ]

  return players

def get_card_name( card : Card ) -> str:
  return card.suit + "_" + str(card.value)

def play_round(players, banker, ai_player):
  # Bidding phase
  players_and_bids = { player.name : player.bid() for player in players }
  ai_player.observe( all_cards, players_and_bids, banker.diamond_deck )
  ai_card = ai_player.bid()

  # Reveal phase and calculate points
  revealed_diamond_card = banker.generate_diamond_card()
  round_winner_card_value = max( [ bidded_card.get_value() for bidded_card in players_and_bids.values() ] + [ai_card.get_value()])
  round_points = revealed_diamond_card.get_value()

  # Handle ties or multiple winners
  winning_players = [player for player in players if players_and_bids [ player.name ].get_value() == round_winner_card_value]
  if ai_card.get_value() == round_winner_card_value: winning_players.append(ai_player)

  if len(winning_players) > 1:
    round_points /= len(winning_players)  # Split points for ties

  # Update player points
  for player in winning_players:
    player.update_points(round_points)

  # Print round results
  player_and_cards = { player : get_card_name(players_and_bids[player]) for player in players_and_bids }
  player_and_cards.update({ ai_player.name : get_card_name(ai_card)})
  player_and_cards.update({ "Banker" : get_card_name(revealed_diamond_card) })
  
  winners = [player.name for player in winning_players]
 
  return player_and_cards, winners, str(round_points)

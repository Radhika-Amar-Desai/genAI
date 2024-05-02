def calculate_diamond_probability( remaining_diamonds):
  """
  This function calculates the probability of each diamond value being revealed.

  Args:
      revealed_diamonds: List of revealed diamond values (integers).

  Returns:
      Dictionary: Probabilities for each diamond value (2-14).
  """

  diamond_probs_of_remaining_cards = { card : remaining_diamonds.count(card) / (len(remaining_diamonds))\
                                      for card in remaining_diamonds }
  return diamond_probs_of_remaining_cards

from functools import reduce

def probability_of_winning(individual_player_cards , card_to_win):
  """
  This function calculates the probability of a card winning the trick.

  Args:
      individual_player_cards: Dictionary where keys are players and values are lists of their remaining cards (excluding diamonds).
      card_to_win: Integer value of the card that needs to win.

  Returns:
      Float: Probability of the card winning the trick.
  """

  all_cards = reduce ( lambda x,y : x | y, [ player_cards for player_cards in individual_player_cards ] )

  favorable_cards = sum([card.get_value() < card_to_win.get_value() for card in all_cards])

  # Total possible combinations (product of remaining cards for each player)
  total_combinations = reduce( lambda x, y : x * y, [ len(player_cards) for player_cards in individual_player_cards ] )

  return favorable_cards / total_combinations

def probabilistic_bidding(hand, remaining_diamonds, other_players_cards):
  """
  This function chooses the card to bid based on expected points.

  Args:
      hand: List of card values (integers) in your hand.
      revealed_diamonds: List of revealed diamond values (integers).

  Returns:
      Integer: The card value to bid (from your hand).
  """
  expected_points = calculate_expected_points(hand, remaining_diamonds, other_players_cards)
  best_card = max(expected_points, key=expected_points.get)
  return best_card

def calculate_expected_points(hand, remaining_diamonds, other_player_cards):
  """
  This function calculates the expected points for bidding each card in your hand.

  Args:
      hand: List of card values (integers) in your hand.
      _: Placeholder argument for revealed_diamonds (not used).

  Returns:
      Dictionary: Expected points for bidding each card in your hand.
  """

  def get_expected_points_for_card ( card_in_hand, remaining_diamonds_prob ):

    expected_points_with_diamond_prob = sum( card.get_value() * prob for card, prob in remaining_diamonds_prob.items()) / len ( remaining_diamonds_prob )
    expected_points_with_winning_prob = expected_points_with_diamond_prob * probability_of_winning ( other_player_cards, card_in_hand )

    return expected_points_with_winning_prob

  remaining_diamonds_prob = calculate_diamond_probability ( remaining_diamonds )

  expected_points = { card_in_hand : get_expected_points_for_card ( card_in_hand, remaining_diamonds_prob ) for card_in_hand in hand}

  return expected_points

def probabilistic_bidding(hand, remaining_diamonds, other_players_cards):
  """
  This function chooses the card to bid based on expected points.

  Args:
      hand: List of card values (integers) in your hand.
      revealed_diamonds: List of revealed diamond values (integers).

  Returns:
      Integer: The card value to bid (from your hand).
  """
  expected_points = calculate_expected_points(hand, remaining_diamonds, other_players_cards)
  best_card = max(expected_points, key=expected_points.get)
  return best_card


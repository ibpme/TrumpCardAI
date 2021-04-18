# AB = Auction Bid
# LP = Leading Player
# DP = Defending Player
from trump import Player, Bid, SuitsEnum, Deck, PASS
from logic import compare_cards, playable_bid
import random
import time


def random_AB(highest_bid=PASS) -> Bid:
    """Use random exponential and beta distribution to make Auction Bids given the highest current bid in the auction

    Parameters
    ----------
    highest_bid : , optional
        Highest current bid in the auction, by default PASS

    Returns
    -------
    Bid
        The choosen random Bid
    """
    valid_bid = playable_bid(highest_bid=highest_bid)

    # Use Random Exponential Distribution to make card bids
    num_from_exp_dist = random.expovariate(1)
    bid_value_choice = min([0, 1, 2, 3, 4, 5, 6],
                           key=lambda x: abs(x-num_from_exp_dist))
    # Find the closest value from random beta distribution for suits
    num_from_beta_dist = random.betavariate(2, 2)*4
    bid_suit_choice = min([0, 1, 2, 3, 4],
                          key=lambda x: abs(x-num_from_beta_dist))+1
    if Bid(bid_value_choice, SuitsEnum(bid_suit_choice)) not in valid_bid:
        return PASS
    return Bid(bid_value_choice, SuitsEnum(bid_suit_choice))


def random_LP(player: Player, trump_played=False, trump_suit=None):
    return random.choice(player.playable_lead_cards(trump_played=trump_played, trump_suit=trump_suit))


def random_DP(player: Player, suit: SuitsEnum):
    return random.choice(player.playable_cards(suit))


def monte_carlo_LP(player: Player, cards_played: list, trump_played=False, trump_suit=None, iteration=100):
    """Return the best card played from a MonteCarlo Simulation by iterating over a sample of possilble card outcomes and distribution

    Parameters
    ----------
    player : Player
    cards_played : list
    trump_played : bool, optional, by default False
    trump_suit : [type], optional, by default None
    iteration : int, number of monte carlo simulations optional, by default 100

    Returns
    -------
    Card
        Best card from the monte carlo iteration
    """

    # TODO : Create a callback function for the opponents DP AI

    # Get all cards that have not been played
    random_deck = Deck()
    cards_not_played = list(set(random_deck.cards) -
                            set(player.cards+cards_played))
    # Create dummy players as sample
    # print(len(set(set(random_deck.cards) - set(player.cards+cards_played))))
    dummy_players = []
    for _ in range(3):
        dummy_players.append(Player())

    # Simulate the best score from canidates cards
    card_candidates = player.playable_lead_cards(
        trump_played=trump_played, trump_suit=trump_suit)
    card_rank = list()
    for card in card_candidates:
        score = 0
        for i in range(iteration):
            # Simulate cards being played and get the score for the card played by the leading player
            cards = []
            for dum_player in dummy_players:
                # Simulate random card distribution
                card_not_played_copy = cards_not_played.copy()
                random_cards = random.sample(card_not_played_copy, int(
                    len(cards_not_played)/len(dummy_players)))
                for random_card in random_cards:
                    card_not_played_copy.remove(random_card)
                dum_player.set_cards(random_cards)
                # Simulate random card being played by player
                play_random_card = random.choice(
                    dum_player.playable_cards(card.suit))
                cards.append(dum_player.play(play_random_card))
            cards.append(card)

            # TODO : Check if winning cards belongs to Teammate to add to points
            winning_card = compare_cards(
                cards, suit_call=card.suit, trump_suit=trump_suit)

            # If the leading player wins the card update the score
            if winning_card.owner == player:
                score += 1
            else:
                continue
        card_rank.append({
            "card": card,
            "score": score
        })
    # Sort the list and return the card with the highest score
    card_rank.sort(key=lambda x: x["score"], reverse=True)
    return card_rank[0]['card']

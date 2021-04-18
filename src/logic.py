from trump import PASS, SuitsEnum, Card, Bid


def compare_cards(cards: list, suit_call: SuitsEnum, trump_suit=None) -> Card:
    """Compare a list of cards and returns the winning card

        Parameters
        ----------
        cards : list
            list of Card
        suit_call : SuitEnum
            The suit that is called by the lead player
        trump_suit : SuitEnum | None
            Trump suit

        Returns
        -------
        Card
            Winning Card
        """
    cards_match_suit = None
    # Check if there is a trump suit in play
    if trump_suit:
        # Check if there is a trump card in cards
        cards_match_suit = list(filter(
            lambda card: card.suit == trump_suit, cards))

    # If there is no trump suit or no trump card found in cards select winner from matching suit call
    if len(cards_match_suit) == 0:
        cards_match_suit = list(filter(
            lambda card: card.suit == suit_call, cards))
        # Determine the winner of a trump card suit or a suit_call suit by its value
    highest_card_value = 0
    highest_card = None
    for card in cards_match_suit:
        if card.card_value > highest_card_value:
            highest_card = card
            highest_card_value = card.card_value
    return highest_card


def playable_bid(highest_bid: Bid) -> list:
    """Get a list of legal Bids that can be made given a highest current bid in the auction

    Parameters
    ----------
    highest_bid : Bid
        Highest current bid in the auction

    Returns
    -------
    list
        List of legal bids
    """
    bid_list = [PASS]
    for i in range(1, 7):
        for j in range(1, 6):
            if Bid(i, SuitsEnum(j)) <= highest_bid:
                continue
            bid_list.append(Bid(i, SuitsEnum(j)))
    return bid_list


def check_pass(bid_history: list) -> bool:
    """Check if 3 consecutive PASS has been made given a bid history

    Parameters
    ----------
    bid_history : list

    Returns
    -------
    bool
    """
    last_three = bid_history[-3:]
    if len(last_three) < 3:
        return False
    if all(map(lambda x: x["bid"] == PASS, last_three)):
        return True
    return False


def void_players(players: list) -> list:
    """List of void players

    Parameters
    ----------
    players : list
        List of players to iterate

    Returns
    -------
    list
        list of void players
    """
    void_players_list = []
    for player in players:
        if player.isVoid():
            void_players_list.append(player)
    return void_players_list

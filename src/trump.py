from enum import IntEnum
import random


class PipsEnum(IntEnum):
    """Pip/Symbol/Numerals Value Enumeration"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class SuitsEnum(IntEnum):
    """Suits Enumeration

    *Note : Also used by Bid object to refer to the value of the Bid PASS and NOTRUMP

    """
    PASS = 0
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4
    NOTRUMP = 5

    @classmethod
    def suits_only(cls, return_type=set):
        return return_type([cls.CLUBS, cls.DIAMONDS, cls.HEARTS, cls.SPADES])


class Card:

    def __init__(self, suit_enum: SuitsEnum, pip_enum: PipsEnum, owner=None):
        """A card representation of a suit and its value

        Parameters
        ----------
        suit_enum : SuitsEnum\n
        pip_enum : PipsEnum\n
        owner : Player | None, optional, by default None
        """
        if suit_enum not in SuitsEnum.suits_only():
            raise ValueError("Card Object only takes SuitEnum values of 1-4")
        self._suit = suit_enum
        self._pip = pip_enum
        self._owner = owner

    # def __eq__(self, other):
    #     if self._suit == other._suit and self._pip == other._pip:
    #         return True
    #     else:
    #         return super().__eq__(other)

    def __hash__(self):
        return hash((self._suit, self._pip))

    @property
    def suit(self) -> SuitsEnum:
        return self._suit

    @property
    def suit_name(self) -> str:
        return str(self._suit.name)

    @property
    def suit_value(self) -> int:
        return self._suit.value

    @property
    def pip(self) -> PipsEnum:
        return self._pip

    @property
    def card_value(self) -> int:
        return self._pip.value

    @property
    def card_name(self) -> str:
        return self._pip.name

    @property
    def owner(self):
        """Player object for the owner of the card

        Returns
        -------
        Player
            Player | None object of the owner of the card
        """
        return self._owner

    def set_owner(self, owner):
        """Set the card's owner

        Parameters
        ----------
        owner : Player | None
            A player object to which the card belongs to
            None if the card is still in deck or not in players hands
        """
        self._owner = owner

    def __repr__(self):
        """Card Representation

        Returns
        -------
        str
            e.g "JACK-SPADES"
        """
        return f"{self.card_name}-{self.suit_name}"


class Deck:

    def __init__(self, shuffle=False):
        """Create a deck filled with 52 playing cards

        Parameters
        ----------
        shuffle : bool, optional
            shuffle the card by initialization, by default False
        """
        self._cards = []
        self.build_cards()
        if shuffle:
            self.shuffle()

    def build_cards(self):
        """Generate a full deck of cards to the deck"""
        for suit in SuitsEnum.suits_only():
            for pip in PipsEnum:
                self._cards.append(Card(suit, pip))

    @property
    def cards(self):
        return self._cards

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self._cards)

    def sort(self, sort_by="all", reverse=False):
        """Sort the deck by value and its suits"""

        if sort_by == "values":
            self._cards.sort(
                key=lambda card: card.card_value, reverse=reverse)
        elif sort_by == "suits":
            self._cards.sort(
                key=lambda card: card.suit_value, reverse=reverse)
        elif sort_by == "all":
            self._cards.sort(
                key=lambda card: card.card_value, reverse=reverse)
            self._cards.sort(
                key=lambda card: card.suit_value, reverse=reverse)
        else:
            raise ValueError("sort_by argument is values/suits/all")

    def draw(self, num=None) -> Card:
        """Draw a card and removes it from the deck

        Returns
        -------
        Card
            object
        """
        return self._cards.pop()

    def remove_cards(self, cards: list):
        for card in cards:
            self._cards.remove(card)


class Bid:

    def __init__(self, value: int, suit):
        """A bid class with a value and a suit

        *Note Bid(0,SuitsEnum(0)) is considered a PASS

        Parameters
        ----------
        value : int
            integer value for the bid\n
        suit : SuitEnum
            SuitEnum(0) is a PASS bid and SuitEnum(5) is NOTRUMP
        """

        if suit == SuitsEnum(0) and value != 0:
            raise ValueError("PASS must be the bid Bid(0,SuitsEnum(0))")

        if value == 0 and suit != SuitsEnum(0):
            # print("Automatic insertion of PASS: Bid(0,SuitsEnum(0))")
            # print(value, suit)
            self._suit = SuitsEnum(0)
        else:
            self._suit = suit

        self._value = value

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return self.value < other
        if self.value < other.value:
            return True
        if self.value == other.value and self.suit < other.suit:
            return True
        return False

    def __le__(self, other):
        if not isinstance(other, type(self)):
            return self.value <= other
        if self.value < other.value:
            return True
        if self.value == other.value and self.suit < other.suit:
            return True
        if self == other:
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return self.value == other
        if self.value == other.value and self.suit == other.suit:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return self.value != other
        if self.value != other.value or self.suit != other.suit:
            return True
        return False

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return self.value > other
        if self.value > other.value:
            return True
        if self.value == other.value and self.suit > other.suit:
            return True
        return False

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            return self.value >= other
        if self.value > other.value:
            return True
        if self.value == other.value and self.suit > other.suit:
            return True
        if self == other:
            return True
        return False

    def num_of_tricks_to_win(self) -> int:
        """Number of tricks to be won by the bid

        Returns
        -------
        int
            integer value of the number of tricks
        """
        return int(self.value + 6)

    @property
    def suit(self):
        return self._suit

    @property
    def value(self) -> int:
        return self._value

    def __repr__(self):
        return f"{self.value}-{self.suit.name}"


PASS = Bid(0, SuitsEnum(0))


class Player:

    def __init__(self):
        """Player Representation\n

        Containing basic player functionality for the game
        Note : Player desicions should not be implemented here
        """
        self._cards = []
        self._bid_history = []
        self._current_bid = None
        self._teammate = None
        self._team = None
        self._next_player = None
        self._prev_player = None

    @property
    def cards(self):
        return self._cards

    def set_cards(self, cards: list):
        self._cards = cards

    @property
    def teammate(self):
        return self._teammate

    def set_teammate(self, player):
        """Set a player object as a teammate

        Parameters
        ----------
        player : Player
        """
        self._teammate = player

    @property
    def team(self):
        return self._team

    def set_team(self, team):
        """Set Team object as the team of the player

        Parameters
        ----------
        team : Team
        """
        self._team = team

    def prev_player(self):
        """Get the previous player from the current player

        Returns
        -------
        Player
        """
        return self._prev_player

    def next_player(self):
        """Get the next player from the current player

        Returns
        -------
        Player
        """
        return self._next_player

    def set_prev_player(self, player):
        """Set the previous player from the current player

        Parameters
        ----------
        player : Player
        """
        self._prev_player = player

    def set_next_player(self, player):
        """Set the next player from the current player

        Parameters
        ----------
        player : Player
        """
        self._next_player = player

    @property
    def current_bid(self):
        return self._current_bid

    @property
    def bid_history(self):
        return self._bid_history

    def auction_bid(self, bid: Bid):
        """Bid in the auction phase ,add to bid_history and set the current player bid individualy

        Parameters
        ----------
        bid : Bid

        Returns
        -------
        Bid
        """
        self._current_bid = bid
        self._bid_history.append(bid)
        return bid

    def build_hand_from_deck(self, deck: Deck, num_of_cards=13):
        if not isinstance(deck, Deck):
            raise ValueError("Takes argument of type Deck")

        for _ in range(num_of_cards):
            # This changes deck object
            card = deck.draw()
            card.set_owner(self)
            self._cards.append(card)

    def sort_cards(self, sort_by="all", reverse=False):
        """Sort the deck by value and its suits"""
        if sort_by == "values":
            self.cards.sort(
                key=lambda card: card.card_value, reverse=reverse)
        elif sort_by == "suits":
            self.cards.sort(
                key=lambda card: card.suit_value, reverse=reverse)
        elif sort_by == "all":
            self.cards.sort(
                key=lambda card: card.card_value, reverse=reverse)
            self.cards.sort(
                key=lambda card: card.suit_value, reverse=reverse)
        else:
            raise ValueError("sort_by argument is values/suits/all")

    def available_suits(self) -> set:
        """Check the availabe remaining Suits in Player.cards

        Returns
        -------
        set
            A set of available suits
        """

        return set(map(lambda card: card.suit, self._cards))

    def unavailable_suits(self) -> str:
        """Check the unavailabe Suits in Player.cards

        Returns
        -------
        str
            A set of unavailabe suits
        """
        unavailable_suits = SuitsEnum.suits_only() - self.available_suits()
        if unavailable_suits:
            return unavailable_suits
        else:
            return None

    def all_cards_of_suit(self, suit: SuitsEnum):
        """Get all the cards in a specified suit

        Parameters
        ----------
        suit : SuitsEnum

        Returns
        -------
        list
            list of cards
        """
        cards = []
        for card in self._cards:
            if card.suit == suit:
                cards.append(card)
        return cards

    def isVoid(self) -> bool:
        """Player has no card of some Suit

        Returns
        -------
        bool
        """
        if self.unavailable_suits():
            return True
        return False

    def play(self, card):
        """Player draws a card,plays a hand and remove it from Player.Cards"""
        self._cards.remove(card)
        return card

    def playable_cards(self, suit: SuitsEnum) -> list:
        """List of the cards that fits the rules given a suit in a defending position

        Parameters
        ----------
        suit : SuitEnum

        Returns
        -------
        list
        """
        if suit not in self.available_suits():
            # print("No more card of suit {}".format(suit.name))
            return self._cards
        else:
            cards_same_suit = list(filter(
                lambda card: card.suit == suit, self._cards))
            return cards_same_suit

    def playable_lead_cards(self, trump_played=False, trump_suit=None):
        # TODO : Possible Error scenario Trump-Card not yet played but only trump suit remains
        """List of the cards that fits the rules given a suit in a leading position


        Parameters
        ----------
        trump_played : bool, optional
            specify if trump has been played, by default False
        trump_suit : [type], optional
            specify the trump-suit by default None , when None it assumes a NoTrump

        Returns
        -------
        list
        """
        if trump_played:
            return self._cards
        else:
            cards_no_trump_suit = list(filter(
                lambda card: card.suit != trump_suit, self._cards))
            if len(cards_no_trump_suit) == 0:
                try:
                    raise Exception(
                        "Possible Error scenario Trump-Card not yet played but only trump suit remains")
                except:
                    print(
                        "Possible Error scenario Trump-Card not yet played but only trump suit remains")
                    return self._cards
            return cards_no_trump_suit

    def reset(self):
        self._cards = []
        self._bid_history = []
        self._current_bid = None


class Team:

    def __init__(self, player1, player2):
        """A team representation containing players

        Parameters
        ----------
        player1 : Player
        player2 : Player
        """
        self._players = [player1, player2]
        self._tricks_won = []
        self.points = 0
        player1.set_team(self)
        player2.set_team(self)
        player1.set_teammate(player2)
        player2.set_teammate(player1)

    @property
    def tricks_won(self) -> list:
        return self._tricks_won

    @property
    def players(self) -> list:
        return self._players

    def add_tricks_won(self, cards: list):
        self._tricks_won += [cards]

    def reset(self):
        self._tricks_won = []
        self.points = 0

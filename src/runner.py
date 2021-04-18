from trump import Card, Deck, Player, SuitsEnum, Team, Bid, PASS
import trump_ai
import logic


def generate_players():
    """Generate players and instanciate  into an array 

    Returns
    -------
    list
        list of players (Player Object)
    """
    players = []
    previous_player = None
    first_player = None
    # Create a two way cyclic list for the players
    for i in range(4):
        # Create player instance and append to player list
        current_player = Player()
        players.append(current_player)

        # Forward cycle
        if i == 0:
            first_player = current_player
        current_player.set_prev_player(previous_player)
        previous_player = current_player
    first_player.set_prev_player(current_player)
    # Backwards cycle
    for _ in range(4):
        previous_player = current_player.prev_player()
        previous_player.set_next_player(current_player)
        current_player = previous_player

    return players


def generate_teams(players):
    """Generate teams and instanciate into array

    Parameters
    ----------
    players : list of players (len(4))
        player length is 4

    Returns
    -------
    list
        iist of teams (Team Object)
    """
    teams = []
    # Create 2 teams for the game
    player = players[0]
    partner = player.next_player().next_player()
    team = Team(player, partner)
    teams.append(team)
    player = player.next_player()
    partner = player.next_player().next_player()
    team = Team(player, partner)
    teams.append(team)
    return teams


def reset(players, teams):
    for player in players:
        player.reset()
    for team in teams:
        team.reset()


PLAYERS = generate_players()
TEAMS = generate_teams(PLAYERS)
PLAYER_WATCH = PLAYERS[0]
TOTAL_SCORE = 0
NUM_OF_ROUNDS = 25

for x in range(NUM_OF_ROUNDS):

    DECK = Deck(shuffle=True)
    CARDS_PLAYED = []
    TRUMP_SUIT = None
    TRUMP_CARD_PLAYED = False
    BID_HISTORY = []
    HIGHEST_BID = PASS
    CONTRACT = None
    DECLARER = None

    # Build hand for each player
    for player in PLAYERS:
        player.build_hand_from_deck(DECK)
        # Check if the player is void then TRUMP CARD CAN BE PLAYED IMMEDIETLY
        # if player.isVoid():
        #     TRUMP_CARD_PLAYED = True
    # Start Auction
    while True:
        player = player.next_player()
        player_bid = trump_ai.random_AB(highest_bid=HIGHEST_BID)
        # Player make the auction bid
        player.auction_bid(player_bid)
        # Recheck if Bid is valid
        if player_bid > HIGHEST_BID or player_bid == PASS:
            # Add bid to bid history
            bid_dict = {"player": player, "bid": player_bid}
            BID_HISTORY.append(bid_dict)

            if player_bid != PASS:
                HIGHEST_BID = player_bid
        else:
            raise ValueError("Not a valid bid !")

        if logic.check_pass(BID_HISTORY):
            break
    if HIGHEST_BID == PASS:
        # raise TypeError("All PASS")
        NUM_OF_ROUNDS -= 1
        continue

    # Get the Player Declarer from BID HISTORY last BID
    DECLARER = BID_HISTORY[-1]["player"]
    CONTRACT = HIGHEST_BID
    TRUMP_SUIT = CONTRACT.suit

    # Start the game
    player = DECLARER
    for i in range(13):

        # Leading player chooses card
        cards = []
        if PLAYER_WATCH == player or PLAYER_WATCH.teammate == player:
            card = trump_ai.monte_carlo_LP(
                player, CARDS_PLAYED, trump_played=TRUMP_CARD_PLAYED, trump_suit=TRUMP_SUIT)
        else:
            card = trump_ai.random_LP(
                player, trump_played=TRUMP_CARD_PLAYED, trump_suit=TRUMP_SUIT)
        suit_call = card.suit
        cards.append(player.play(card))

        # Simulatate turn for defending players
        for _ in range(3):
            player = player.next_player()
            card = trump_ai.random_DP(player, suit_call)
            cards.append(player.play(card))

        # Determine winner
        wining_card = logic.compare_cards(
            cards, suit_call, trump_suit=TRUMP_SUIT)
        # If a trump suit won , then a trump suit is played
        if wining_card.suit == TRUMP_SUIT:
            if TRUMP_SUIT != SuitsEnum(0) or TRUMP_SUIT != SuitsEnum(5):
                TRUMP_CARD_PLAYED = True

        # Give points to winning team
        player_winner = wining_card.owner
        team_winner: Team = player_winner.team
        team_winner.points += 1

        player = player_winner

        # Add cards played to history of game and tricks won to winner
        CARDS_PLAYED += cards
        team_winner.add_tricks_won(cards)

    print("Game {}:".format(x), "Trump :{} ".format(TRUMP_SUIT.name), end=" ")
    if len(PLAYER_WATCH.team.tricks_won) > len(PLAYER_WATCH.next_player().team.tricks_won):
        TOTAL_SCORE += 1
        print("Won")
    else:
        print("Lost")

    reset(PLAYERS, TEAMS)


print("Win Rate: {:.2f} %".format(TOTAL_SCORE*100/NUM_OF_ROUNDS))

import random
# Vi skapar fyra klasser som kommunicerar med varandra

# Class card prints out rank and suit
class Card:
    def __init__(self, suit:str, rank:str) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank['rank']} of {self.suit}"
    
# Class Deck makes a deck of cards
class Deck:
    def __init__(self): 
        self.cards = [] # Create an empty list 
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"] # Four suits
        # A dictionary with a rank and corresponding value (key:value) 
        ranks = [
                {"rank": "A", "value": 14},
                {"rank": "2", "value": 2},
                {"rank": "3", "value": 3},
                {"rank": "4", "value": 4},
                {"rank": "5", "value": 5},
                {"rank": "6", "value": 6},
                {"rank": "7", "value": 7},
                {"rank": "8", "value": 8},
                {"rank": "9", "value": 9},
                {"rank": "10", "value": 10},
                {"rank": "J", "value": 10},
                {"rank": "Q", "value": 10},
                {"rank": "K", "value": 10},
                ]
        # A for loop to insert every possible hand(move) in self.card list
        for suit in suits:
            for rank in ranks:  
                self.cards.append(Card(suit, rank))

    # A method to shuffle a deck
    def shuffle(self) -> None:
        random.shuffle(self.cards)

    # A method to deal 
    def deal(self, number: int):
        cards_dealt = [] # An empty list to store cards dealt
        for x in range(number): # a loop to deal numbers amount of times
            if len(self.cards) > 0: 
                card = self.cards.pop() # Pop the last deck
                cards_dealt.append(card) # store it in cards_dealt
        return cards_dealt # return the list cards_dealt

# A class that handles the dealing of the cards
class Hand:
    def __init__(self, dealer: bool=False):
        self.cards = [] # This list will store the players hand and dealers hand
        self.value = 0 # The total value of player and dealer 
        self.dealer = dealer

    # This method adds a card to a hand
    def add_card(self, card_list) -> None:
        self.cards.extend(card_list) # Appends the new card to card_list

    # This method calculates the value. 
    def calculate_value(self) -> None:
        self.value = 0
        has_ess:bool = False
        
        # this for loop iterates over each card.
        for card in self.cards:
            card_value = int(card.rank["value"]) # calculates the new value
            self.value += card_value   # Adds the new value to the total value
            if card.rank["rank"] == "A": # If the card you got is an A, has_ess is true
                has_ess = True

        # if the total value of hand is over 21, A turns to the value of 1 instead of 14
        if has_ess and self.value > 21:
            self.value = self.value - 13

        #This method recalculates and returns the new value
    def get_value(self) -> int:
        self.calculate_value()
        return self.value
    
    # This method checks if it's blackjack. This applies if the new value is exactly 21.
    def is_blackjack(self):
        return self.get_value() == 21

    # This method displays the current hand
    def display(self, show_all_dealer_cards=False) -> None:
        print(f"{'Dealers' if self.dealer else "Your"} hand:") # This prints either dealers or your hand depending on if self.dealer is true or false
        for index, card in enumerate(self.cards): # This loops through every card in your hand (self.card)
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack(): # This prints hidden for the dealer if all conditions are met.
                print("Hidden")
            else:
                print(card)

        if not self.dealer: # Prints players hand if false.
            print("Value:", self.get_value())
        else:
            if show_all_dealer_cards:
                print("Value:", self.get_value())
        print()

# This class is the game running
class Game:
    def play(self) -> None: # This method runs the game

            deck = Deck() # Initalize a new deck object
            deck.shuffle() # Shuffles this deck

            player_hand = Hand() # Initialize Hand to the player. Player has an empty list(hand)
            dealer_hand = Hand(dealer=True) # Initialize Hand to the dealer. Dealer has an empty list(hand)

            # A loop that deals 1 card each for player and dealer.
            for i in range(1):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

                # Welcome sign!
                print("*" * 30)
                print("Welcome to a game of Blackjack!")
                print("*" * 30)

                # Displays current hand for player and dealer
                player_hand.display()
                dealer_hand.display()

                choice: str = ""

                # This loop runs while value is under 21. It wants and input from user
                while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                    choice = input("Choose 'Hit' or 'Stand': ").lower()
                    print()
                    while choice not in ["h", "s", "hit", "stand"]:
                        choice = input("Please enter 'hit' or 'stand' or (h/s)").lower()
                        print()
                    if choice in ["hit", "h"]: # If hit, adds a new card and displays
                        player_hand.add_card(deck.deal(1))
                        player_hand.display()

                if self.check_winner(player_hand, dealer_hand): # Checks if player or dealer has won yet.
                    continue

                player_hand_value = player_hand.get_value() # Recalculates the total value of player
                dealer_hand_value = dealer_hand.get_value() # Recalculates the total value of dealer

                # This loop checks if dealers hand is under 21. If under 21, adds a new card.
                while dealer_hand_value < 21:
                    dealer_hand.add_card(deck.deal(1))
                    dealer_hand_value = dealer_hand.get_value()
                    

                dealer_hand.display(show_all_dealer_cards=True) # This reveals the dealers cards (value)

                if self.check_winner(player_hand, dealer_hand): # Check if there's a winner again
                    continue
                
                # Prints final result and values of player and dealer hands.
                print("Final Results:")
                print("Your hand:", player_hand_value)
                print("Dealers hand:", dealer_hand_value)

                # Check if there's a winner again. True argument is passed to game_over to finish the game
                self.check_winner(player_hand, dealer_hand, True)

            print("")
            print("Thanks for playing!")
         
    # This method checks for every possible outcome.
    def check_winner(self, player_hand, dealer_hand, game_over:bool = False):
        if not game_over:
            if player_hand.get_value() > 21: # Checks if player hand is over 21
                print("You have lost!")
                return True # This makes game_over = True
            
            elif dealer_hand.get_value() > 21: # Checks if dealer hand is over 21
                print("Dealer lost. You won!")
                return True
            
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack(): # Checks if player and dealer has both blackjack
                print("Both players have blackjack. That means you lose!")
                return True

            elif player_hand.is_blackjack(): # Checks if player has blackjack
                print("You have blackjack. You win!")
                return True

            elif dealer_hand.is_blackjack(): # Checks if dealer has blackhack
                print("Dealer has blackjack. You lost!")
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value(): # Checks if player hand is bigger than dealer hand
                print("You win!")
            elif player_hand.get_value() == dealer_hand.get_value(): # Checks if player hand and dealer hand is the same
                print("It's a Tie! That means you have lost!")
            else:
                print("Dealer win!")
                print("Dealer: GG EZ NOOB! 8D")
                print("")
                return True

        return False

# Calls the class Game to the variabel g
g = Game()

# This runs the method play within the class Game
g.play()
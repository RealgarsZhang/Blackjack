import constant
import random

DEBUG = False

class Game(object):

########################################################
#              Private methods                          #
########################################################

    def __init__(self,num_players):
        self.__cards = []
        self.__next_card = 0
        self.__reset_cards()
        self.__players = [self.Player(i) for i in range(num_players)]
        self.__dealer_hand = [None,None] # 1st is hole card

    def __compute_raw_val(self, hand):  # computes the facial value of a hand.
        A_cnt = 0
        tmp = 0
        for card in hand:
            if card.isdigit():
                tmp += int(card)
            elif card == 'A':
                A_cnt += 1
            else:
                tmp += 10

        if A_cnt == 0:
            return tmp
        else:
            A_list = [A_cnt + tmp, 11 + (A_cnt - 1) + tmp]

        if A_list[1] <= 21:
            return A_list[1]
        else:
            return A_list[0]

    def __compute_val(self, hand, splitted=False): # computes the value of a hand. -1 for bust. 22 for blackjack.
        if not splitted and len(hand) == 2 and sorted(hand) in [['A','J'],['A','Q'],['A','K'],['10','A']]:
            return 22 # blackjack
        raw_val = self.__compute_raw_val(hand)
        if raw_val <=21:
            return raw_val
        else:
            return -1

    # different hit, double, split rule can be added by modifying following six methods.
    def __hittable(self,player,hand_idx):
        if hand_idx not in player.no_more_cards \
                and self.__compute_val(player.hands[hand_idx],player.splitted)>=0:#not doubled, splitted ace, or bust
            return True
        else:
            return False

    def __doublable(self,player,hand_idx):
        bet = player.bets[hand_idx]
        return bet<=player.fund and hand_idx not in player.no_more_cards

    def __splittable(self,player,hand_idx):
        hand = player.hands[hand_idx]
        if len(player.hands)<constant.MAX_SPLIT and \
                player.bets[hand_idx]<= player.fund and \
                len(hand)==2 and \
                self.__compute_raw_val([hand[0]]) == self.__compute_raw_val([hand[1]]):
            return True
        else:
            return False

    def __handle_hit(self,player,hand_idx):
        player.hands[hand_idx].append(self.__get_next_card())

    def __handle_double(self,player,hand_idx):
        player.fund -= player.bets[hand_idx]
        player.bets[hand_idx] *=2
        player.hands[hand_idx].append(self.__get_next_card())
        player.no_more_cards.add(hand_idx)

    def __handle_split(self,player,hand_idx):
        player.splitted = True
        player.fund -= player.bets[hand_idx]
        player.bets.append(player.bets[hand_idx])
        hand = player.hands[hand_idx][:]
        player.hands[hand_idx] = [hand[0],self.__get_next_card()]
        player.hands.append([hand[1],self.__get_next_card()])
        if hand[0] == 'A':
            player.no_more_cards.add(hand_idx)
            player.no_more_cards.add(len(player.hands)-1)

    def __get_next_card(self): # Pick a card at random. For simplicity, assume enough cards.
        if self.__next_card >= len(self.__cards):
            return None
        else:
            return_val = self.__cards[self.__next_card] #defer the increment
            self.__next_card += 1
            return return_val

    def __print_hands(self, hands):
        for i in range(len(hands)):
            print("Latest hand "+ str(i)+ ": "+" ".join(hands[i]))

    def __reset_cards(self):
        self.__cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4 * constant.NUM_DECKS
        random.shuffle(self.__cards)
        if DEBUG:
            self.__cards = ['A','Q','A','Q','A','A','9','5','A','A','A','A','A']+self.__cards
        self.__next_card = 0

    def __reset_players(self): # don't reset fund or pid!
        for p in self.__players:
            p.splitted = False
            p.hands = []
            p.bets = []
            p.ingame = False
            p.no_more_cards = set()

    def __reset_dealer(self):
        self.__dealer_hand = [None,None]

########################################################
#              Public methods                          #
########################################################

    def Reset(self):
        self.__reset_cards()
        self.__reset_players()
        self.__reset_dealer()

    def Get_bets(self): # Ask for bets from players. 0 bet means not participating.
        exist_player = False
        for p in self.__players:
            if p.fund <=0:
                print("Player %d: You have lost all money. You can't bet." %p.pid)
            else:
                while True:
                    bet = input("Player %d: Please take a bet:" %p.pid)
                    if bet.isdigit():
                        if bet == '0':
                            print("Player %d: You decide not to participate." % p.pid)
                            print()
                            break
                        elif int(bet)>p.fund:
                            print("Player %d: You don't have enough fund. Your fund is: %d. Try again."% (p.pid,p.fund))
                        else:
                            print("Player %d: Your bet is %s. Good luck."% (p.pid,bet))
                            p.fund -= int(bet)
                            p.bets.append(int(bet))
                            p.ingame = True
                            exist_player = True
                            print()
                            break
                    else:
                        print("Player %d: Invalid input. Try again." % p.pid)

        return exist_player

    def Two_cards_distri(self): # At the start, give two cards to everyone.
        self.__dealer_hand[0] = self.__get_next_card()
        self.__dealer_hand[1] = self.__get_next_card()
        print ("The dealer's current hand is: (\"*\" means hole card)")
        print (self.__dealer_hand[0]," *")
        print ()
        print("Now distribute two cards to each player.")
        print()
        for p in self.__players:
            if p.ingame:
                p.hands.append([self.__get_next_card(),self.__get_next_card()])
                print("Player %d: Your hand is the following:" % p.pid)
                print(" ".join(p.hands[0]))
                print()

    def Offer_insurance(self):
        pass

    def Peek_for_blackjack(self):
        if self.__compute_val(self.__dealer_hand,False) == 22:
            print("The dealer has a blackjack. His hand is: ")
            print(" ".join(self.__dealer_hand))
            return True
        else:
            return False

    def Resolve_insurance(self):
        pass

    def Finalize(self): # Computes winning and losing.
        dealer_val = self.__compute_val(self.__dealer_hand,False)

        for p in self.__players:

            if p.ingame == False:
                continue

            num_hands = len(p.hands)
            for i in range(num_hands):
                player_val = self.__compute_val(p.hands[i],p.splitted)
                if player_val == dealer_val:
                    print("Player %d: You get push in your hand %d: "%(p.pid,i)+" ".join(p.hands[i]))
                    p.fund += p.bets[i]
                elif player_val>dealer_val:
                    if player_val == 22:
                        print("Player %d: Blackjack! You win %d in your hand %d: "\
                              % (p.pid,p.bets[i]*(constant.BLACKJACK_PAY-1), i)+" ".join(p.hands[i]))
                        p.fund += p.bets[i]*constant.BLACKJACK_PAY
                    else:
                        print("Player %d: You win %d in your hand %d: "\
                              % (p.pid, p.bets[i]*(constant.NORMAL_PAY-1), i)+" ".join(p.hands[i]))
                        p.fund += p.bets[i]*constant.NORMAL_PAY
                else:
                    print("Player %d: You lose %d in your hand %d: " \
                          % (p.pid,p.bets[i], i)+" ".join(p.hands[i]))
            print("Player %d: Your fund left is %d" % (p.pid,p.fund))
            print()

    def Players_move(self):
        for p in self.__players:

            if p.ingame == False:
                continue
            print("Now is the turn of player %d."%p.pid)
            self.Print_player(p.pid)
            i = 0
            while i<len(p.hands):

                #build choices
                valid_choices = ['ST']
                print_str = "ST: Stand\n"
                if self.__hittable(p, i):
                    print_str += "H: Hit\n"
                    valid_choices.append('H')
                if self.__doublable(p, i):
                    print_str += "D: Double\n"
                    valid_choices.append('D')
                if self.__splittable(p, i):
                    print_str += "SP: Split\n"
                    valid_choices.append('SP')
                # surrender can be inserted here

                print('For your hand %d: ' % i + " ".join(p.hands[i]) + \
                      ", with bet %d, you have following options:" %p.bets[i])
                print(print_str)

                # get user choice
                while True:
                    choice = input("Please choose from"+str(valid_choices))
                    if choice not in valid_choices:
                        print("Invalid input. Try again.\n")
                    else:
                        break

                # checks already done! Choice is indeed valid.
                # handle choices
                if choice == 'ST':
                    print("You choose to stand for hand %d."%p.pid)
                    self.Print_player(p.pid)
                    #print()
                    i+=1
                elif choice == 'H':
                    self.__handle_hit(p,i)
                    print("Hit successful. The new hand is")
                    print(" ".join(p.hands[i]))
                    self.Print_player(p.pid)
                    #print()

                elif choice == 'D':
                    self.__handle_double(p,i)
                    print("Double successful.")
                    self.Print_player(p.pid)
                    #print()

                else:
                    self.__handle_split(p,i)
                    print("Split successful.")
                    self.Print_player(p.pid)
                    #print()

    def Dealer_hit17(self): # Hit soft 17 after players' moves
        print("Dealer's two cards are:")
        print(" ".join(self.__dealer_hand))
        print()
        while 0<=self.__compute_val(self.__dealer_hand,False)<17: # pick until soft 17.
            self.__dealer_hand.append(self.__get_next_card())
        print("After hitting 17, dealer's hand is:")
        print(" ".join(self.__dealer_hand))

    def Print_player(self,pid):
        print("Player %d, your fund left is %d. Following are your current hand(s) and bet(s):"%(pid, self.__players[pid].fund))
        print()
        for i in range(len(self.__players[pid].hands)):
            hand = self.__players[pid].hands[i]
            bet = self.__players[pid].bets[i]
            print ('Hand %d: ' %i)
            print (" ".join(hand))
            print ('Bet %d: ' %i)
            print (bet)
            print ()

    class Player(object):

        def __init__(self,pid):
            self.splitted = False # if splitted, then no blackjack. Reset when reset Game
            self.fund = constant.INITIAL_FUND # initial fund, initialized to be 1000. Don't reset
            self.hands = [] # self.hands[i]: str list contains cards in the hand. Reset when reset Game.
            self.bets = [] # bets for each hand. Reset when reset Game
            self.pid = pid # don't reset
            self.ingame = False # reset
            self.no_more_cards = set() # reset. hand idx which should get no more cards(for splitted ace and doubled hand)
            # can add more states for surrender and insurance


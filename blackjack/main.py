from Game import Game
import constant


if __name__ == "__main__":

    print("Welcome to Blackjack!")

    num = input("Please input the number of players, no more than %d."%constant.MAX_PLAYER)
    while not num.isdigit() or int(num)==0 or int(num)>constant.MAX_PLAYER:
        num = input("Invalid input! Please try again")

    g = Game(int(num))
    end = False

    print("Your initial funds are all %d."%constant.INITIAL_FUND)
    while not end:
        g.Reset()
        _ = input("Press ENTER to input bets. ")
        print()
        exist_player = g.Get_bets()
        if exist_player:
            _ = input("Press ENTER to start two card phase. ")
            print()
            g.Two_cards_distri()
            _ = input("Press ENTER to continue")
            print()
            blackjack_found = g.Peek_for_blackjack()
            if blackjack_found:
                _ = input("Press ENTER to see summary.")
                print()
                g.Finalize()
            else:
                _ = input("Press ENTER to start players' move.")
                print()
                g.Players_move()
                _ = input("Press ENTER to start hit 17' move.")
                print()
                g.Dealer_hit17()
                _ = input("Press ENTER to see summary.")
                print()
                g.Finalize()
        else:
            print("Unfortunately, no one wants to play.")

        cont = input("Do you want to play one more time?[Y/N]")
        while cont not in ('Y','N'):
            cont = input("Invalid input. Please answer Y or N.")
        if cont == 'N':
            end = True
            print("Game over. Thank you for playing!")





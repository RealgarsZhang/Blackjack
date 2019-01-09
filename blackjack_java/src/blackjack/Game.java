package blackjack;

import java.util.Scanner;

public class Game {

    private Player[] players;

    public Game(int player_num, double fund){
        players = new Player[player_num];
        for(int i =0; i<player_num; i++) {
            players[i] = new Player(fund);
        }
    }


    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Please input the number of players:");
        int player_num = scanner.nextInt();
        // Todo: Check valid
        System.out.println("Please enter initial fund:");
        double fund = scanner.nextDouble();

        Game g = new Game(player_num,fund);





    }
}

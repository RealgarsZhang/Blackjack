package blackjack;

import java.util.ArrayList;

public class Player {
    private ArrayList<ArrayList<String>> hands = new ArrayList<>();
    private ArrayList<Double> bets = new ArrayList<>();
    private double fund;
    private final int max_hands = 4;

    public Player(double fund){
        this.fund = fund;
    }

    public ArrayList<ArrayList<String>> getHands() {
        return hands;
    }

    public void setHands(ArrayList<ArrayList<String>> hands) {
        this.hands = hands;
    }

    public ArrayList<Double> getBets() {
        return bets;
    }

    public void setBets(ArrayList<Double> bets) {
        this.bets = bets;
    }

    public double getFund() {
        return fund;
    }

    public void setFund(double fund) {
        this.fund = fund;
    }

    public boolean addHand(ArrayList<String> new_hand){
        if (hands.size()>=max_hands){
            System.out.println("Max num of hands reached.");
            return false;
        }
        hands.add(new ArrayList<>(new_hand));
        return true;
    }

    public boolean addBet(double new_bet){
        if (bets.size()>=max_hands){
            System.out.println("Max num of hands reached.");
            return false;
        }
        bets.add(new_bet);
        return true;
    }

    public double changeFund(double delta_fund){
        if (fund+delta_fund<0){
            System.out.println("Not enough fund. You spend all you have.");
            double tmp = fund;
            fund = 0.0;
            return -tmp;
        }else{
            fund += delta_fund;
            return delta_fund;
        }
    }

}

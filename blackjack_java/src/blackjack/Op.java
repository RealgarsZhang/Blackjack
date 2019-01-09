package blackjack;

public class Op {
    protected String opName = "Op";

    public boolean doable(Player player){
        return true;
    }

    public boolean execute(Player player){
        return true;
    }
}

class Stand extends Op{
    public Stand(String opName){
        this.opName = opName;
    }

    @Override//For polymorphism, don't use static
    public boolean doable(Player player) {
        return super.doable(player);
    }

    @Override
    public boolean execute(Player player) {
        return super.execute(player);
    }
}

class Split extends Op{
    public Split(String opName){
        this.opName = opName;
    }
    @Override
    public boolean doable(Player player){
        if (player.getHands().size()>=4){
            System.out.println("Maximum hands reached. Unable to split");
            return false;
        }
        //Exist pair? which to split?
    }
}

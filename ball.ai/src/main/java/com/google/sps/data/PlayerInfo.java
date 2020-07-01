package main.java.com.google.sps.data;

public class PlayerInfo {
    private String first_name, last_name;
    private int points,rebounds,steals;

    public PlayerInfo(String first_name, String last_name, int points, int rebounds, int steals){
        this.first_name = first_name;
        this.last_name = last_name;
        this.points = points;
        this.rebounds = rebounds;
        this.steals = steals;
    }
}
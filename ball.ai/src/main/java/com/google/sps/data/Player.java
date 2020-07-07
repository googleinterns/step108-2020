package com.google.sps.data;

public class Player {
    private String name;
    private int points,rebounds,steals;

    public Player(String name, int points, int rebounds, int steals){
        this.name = name;
        this.points = points;
        this.rebounds = rebounds;
        this.steals = steals;
    }
}
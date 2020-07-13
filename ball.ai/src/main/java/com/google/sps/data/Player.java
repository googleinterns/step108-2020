package com.google.sps.data;

public class Player {
    private String name;
    private int points,rebounds,steals,year;

    public Player(String name, int points, int rebounds, int steals , int year){
        this.name = name;
        this.points = points;
        this.rebounds = rebounds;
        this.steals = steals;
        this.year= year;
    }
}
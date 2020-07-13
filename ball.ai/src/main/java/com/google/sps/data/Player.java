package com.google.sps.data;

public class Player {
    private String name;
    private double points,rebounds,steals;
    private int year;

    public Player(String name, double points, double rebounds, double steals , int year){
        this.name = name;
        this.points = points;
        this.rebounds = rebounds;
        this.steals = steals;
        this.year= year;
    }
}
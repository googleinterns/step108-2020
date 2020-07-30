package com.google.sps.data;

public class Player {
    private String name;
    private double points, assists, rebounds, steals, blocks;
    private int year;

    public Player(String name, double points, double assists, double rebounds, double steals , int year, double blocks){
        this.name = name;
        this.points = points;
        this.assists = assists;
        this.rebounds = rebounds;
        this.steals = steals;
        this.blocks = blocks;
        this.year = year;
    }
}
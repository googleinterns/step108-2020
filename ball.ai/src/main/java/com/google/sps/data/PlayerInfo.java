package com.google.sps.data;

import java.util.List;
import java.util.ArrayList;

public class PlayerInfo {
    private String name;
    private int player_id;
    private List<Integer> seasonsPlayed = new ArrayList<Integer>();
    private List<String> positionsPlayed = new ArrayList<String>();

    public PlayerInfo(String name, int player_id, int year, List<String> positionsPlayed){
        this.name = name;
        this.player_id = player_id;
        addYear(year);
        this.positionsPlayed = positionsPlayed;
    }
    
    public void addYear(int year){
        seasonsPlayed.add(year);
    }
}
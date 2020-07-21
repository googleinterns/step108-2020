package com.google.sps.data;

import java.util.List;
import java.util.ArrayList;

public class PlayerInfo {
    private String name;
    private int player_id;
    private List<Integer> seasonsPlayed = new ArrayList<Integer>();

    public PlayerInfo(String name, int player_id, int year){
        this.name = name;
        this.player_id = player_id;
        addYear(year);
    }
    
    public void addYear(int year){
        seasonsPlayed.add(year);
    }
}
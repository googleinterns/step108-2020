package com.google.sps.data;

import com.google.sps.data.Team;
import java.util.ArrayList;

public class Schedule {
    private int year;
    private ArrayList<Integer[]> games = null;
    private ArrayList<Team> teams = null;

    public Schedule(int year, ArrayList<Team> teams) {
        this.year = year;
        this.teams = teams;
    }

    public void addGame(Integer[] game) {
        if (this.games == null) {
            this.games = new ArrayList<>();
        }
        this.games.add(game);
    }

    public void addGames(ArrayList<Integer[]> games) {
        this.games = games;
    }

    public void addTeam(Team team) {
        if (this.teams == null) {
            this.teams = new ArrayList<>();
        }
        this.teams.add(team);
    }

    public void addTeams(ArrayList<Team> teams) {
        this.teams = teams;
    }
}
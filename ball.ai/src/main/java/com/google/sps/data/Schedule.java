package com.google.sps.data;

import com.google.sps.data.Team;
import com.google.sps.data.Game;
import java.util.List;
import java.util.ArrayList;

public class Schedule {
    public int year;
    public List<Game> games = null;
    public List<Team> teams = null;

    public Schedule(int year) {
        this.year = year;
    }

    public void addGame(Game game) {
        if (this.games == null) {
            this.games = new ArrayList<>();
        }
        this.games.add(game);
    }

    public void addGames(List<Game> games) {
        this.games = games;
    }

    public void addTeam(Team team) {
        if (this.teams == null) {
            this.teams = new ArrayList<>();
        }
        this.teams.add(team);
    }

    public void addTeams(List<Team> teams) {
        this.teams = teams;
    }
}
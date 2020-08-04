package com.google.sps.data;

import java.util.ArrayList;
import java.util.List;

public class Schedule {
  public int year;
  public List<Game> games = null;
  public List<Team> teams = null;

  public Schedule() {}

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
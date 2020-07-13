package com.google.sps.data;

import java.lang.reflect.Field;
import java.util.List;

public class Team {
  public String team_name, team_nickname, team_abbrev, team_id, division_id, conference;

  public Team(String city, String name, String abbrv, String id, String division, String conference) {
    this.team_name = city;
    this.team_nickname = name;
    this.team_abbrev = abbrv;
    this.team_id = id;
    this.division_id = division;
    this.conference = conference;
  }

  public Team() throws IllegalAccessException {
    for (Field field : this.getClass().getFields()) {
      field.set(this, null);
    }
  }

  public static List<Team> fromCSV() {
    CSVToObj csv = new CSVToObj();
    return csv.fromFile("resources/teams.csv", Team.class);
  }
}
package com.google.sps.data;

public class Team {
    private String name, abbrv, division, conference;

    public Team(String name, String abbrv, String division, String conference) {
        this.name = name;
        this.abbrv = abbrv;
        this.division = division;
        this.conference = conference;
    }
}
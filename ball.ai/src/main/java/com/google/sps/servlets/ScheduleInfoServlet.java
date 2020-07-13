package com.google.sps.servlets;

import com.google.sps.data.Team;
import com.google.sps.data.Game;
import com.google.sps.data.Schedule;
import com.google.sps.data.CSVToObj;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.*;

import com.google.gson.Gson;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/scheduleInfo")
public class ScheduleInfoServlet extends HttpServlet {

    // Reads in csv file of teams and converts it to json
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        int year = Integer.parseInt(request.getParameter("year"));
        CSVToObj csv = new CSVToObj();
        List<Game> games = csv.fromFile(String.format("resources/past_schedules/%d.csv", year), Game.class);
        List<Team> teams = Team.fromCSV();
        if (games != null && teams != null) {
            Schedule schedule = new Schedule(year);
            schedule.addGames(games);
            schedule.addTeams(teams);
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(schedule));
        } else {
            response.setContentType("application/json;");
            response.getWriter().println("false");
        }
    }
}
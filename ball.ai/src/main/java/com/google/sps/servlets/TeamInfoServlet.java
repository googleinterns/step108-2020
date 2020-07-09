package com.google.sps.servlets;

import com.google.sps.data.Team;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
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

@WebServlet("/teamInfo")
public class TeamInfoServlet extends HttpServlet {

    // Reads in csv file of teams and converts it to json
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader("resources/teams.csv"));
            CSVParser records = CSVFormat.DEFAULT
                .withFirstRecordAsHeader()
                .parse(br);
            List<Team> teams = new ArrayList<>();
            for (CSVRecord record : records){
                String name = record.get("team_name").concat(
                    record.get("team_nickname"));
                String abbrv = record.get("team_abbrev");
                String division = record.get("division_id");
                String conference = record.get("conference");

                Team team = new Team(name, abbrv, division, conference);
                teams.add(team);
            }
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(teams));
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (br != null){
                    br.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}
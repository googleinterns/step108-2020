package com.google.sps.servlets;

import com.google.sps.data.CSVToObj;
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
        List<Team> teams = Team.fromCSV();
        if (teams != null) {
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(teams));
        } else {
            // Invalid year specified
            response.setContentType("application/json;");
            response.getWriter().println("false");
        }
    }
}
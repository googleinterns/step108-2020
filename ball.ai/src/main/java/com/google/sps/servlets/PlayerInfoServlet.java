package com.google.sps.servlets;

import com.google.sps.data.Player;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import java.util.Map;
import java.util.HashMap;
import java.lang.Double;

import com.google.gson.Gson;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/playerInfo")
public class PlayerInfoServlet extends HttpServlet {

    /**
     * reads in csv file of players and converts it to json
     */
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader("resources/player-seasons_per_game.csv"));
            CSVParser records = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(br);
            Map<String, Player> team = new HashMap<>();
            for (CSVRecord record: records) {
                String name = record.get("PLAYER_NAME");
                double points = Double.parseDouble(record.get("PTS"));
                double assists = Double.parseDouble(record.get("AST"));
                double rebounds = Double.parseDouble(record.get("REB"));
                double steals = Double.parseDouble(record.get("STL"));
                double blocks = Double.parseDouble(record.get("BLK"));
                int year = Integer.parseInt(record.get("SEASON"));
                String id = name + year;
                team.putIfAbsent(id, new Player(name, points, assists, rebounds, steals, year, blocks));
            }
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(team));
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if(br != null){
                    br.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        
    }
}
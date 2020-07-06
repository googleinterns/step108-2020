package com.google.sps.servlets;

import com.google.sps.data.Player;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import java.util.ArrayList;
import java.util.List;
import com.google.gson.Gson;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/playerInfo")
public class PlayerInfoServlet extends HttpServlet {


    //reads in csv file of players and converts it to json
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        BufferedReader br = null;
        try{
            br = new BufferedReader(new FileReader("players.csv"));
            CSVParser records = CSVFormat.DEFAULT
                .withFirstRecordAsHeader()
                .parse(br);
            List<Player> team = new ArrayList<>();
            for (CSVRecord record: records){
                String first_name = record.get("first_name");
                String last_name = record.get("last_name");
                int points = Integer.parseInt(record.get("points"));
                int rebounds = Integer.parseInt(record.get("rebounds"));
                int steals = Integer.parseInt(record.get("steals"));

                Player player = new Player(first_name, last_name, points, rebounds, steals);
                team.add(player);
            }
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(team));
        } catch (IOException e){
            e.printStackTrace();
        } finally {
            try{
                if(br != null){
                    br.close();
                }
            }catch (IOException ex){
                ex.printStackTrace();
            }
        }
        
    }
}
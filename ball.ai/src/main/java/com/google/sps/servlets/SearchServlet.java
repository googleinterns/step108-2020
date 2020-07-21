package com.google.sps.servlets;

import com.google.sps.data.PlayerInfo;
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
import java.lang.Double;

import com.google.gson.Gson;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/search")

public class SearchServlet extends HttpServlet {


    //reads in csv file of players and converts it to json
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        BufferedReader br = null;
        try{
            br = new BufferedReader(new FileReader("resources/player-seasons_per_game.csv"));
            CSVParser records = CSVFormat.DEFAULT
                .withFirstRecordAsHeader()
                .parse(br);
            Map<String, PlayerInfo> listPlayers = new HashMap<>();
            for (CSVRecord record: records){
                String name = record.get("PLAYER_NAME");
                int year = Integer.parseInt(record.get("SEASON"));
                int player_id = Integer.parseInt(record.get("PLAYER_ID"));
                
                if(listPlayers.containsKey(name)){
                    listPlayers.get(name).addYear(year);
                }else{
                    listPlayers.putIfAbsent(name, new PlayerInfo(name,player_id,year));
                }
            }
            Gson gson = new Gson();
            response.setContentType("application/json;");
            response.getWriter().println(gson.toJson(listPlayers));
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
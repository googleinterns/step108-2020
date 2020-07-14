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
import java.util.Map;
import java.util.HashMap;
import java.util.*;
import java.lang.Double;

import com.google.gson.Gson;

import com.google.appengine.api.datastore.FetchOptions;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.SortDirection;
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
            Map<String, List<Integer>> listPlayers = new HashMap<>();
            for (CSVRecord record: records){
                String name = record.get("PLAYER_NAME");
                int year = Integer.parseInt(record.get("SEASON"));
                
                if(listPlayers.containsKey(name)){
                    listPlayers.get(name).add(year);
                }else{
                    listPlayers.putIfAbsent(name, new ArrayList<Integer>(Arrays.asList(year)));
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
package com.google.sps.servlets;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.util.List;
import java.net.URL;
import java.util.ArrayList;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.BufferedReader;
import java.util.HashMap;
import java.lang.reflect.Type;
import java.lang.Math;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@WebServlet("/k-hot")
public class KHotModelServlet extends HttpServlet {

private String getParameter(HttpServletRequest request, String name, String defaultValue) {
        String value = request.getParameter(name);
        if (value == null) {
                return defaultValue;
        }
        return value;
}

//get method
@Override
public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String[] home = getParameter(request,"home", "").split("\\|"); 
        String[] away = getParameter(request,"away", "").split("\\|"); 

        double linear_reg = 0.0;


        try {
            // create Gson instance
            Gson gson = new Gson();

            // create a reader
            Path pathToFile = Paths.get("player_coef.json");
            BufferedReader reader = Files.newBufferedReader(pathToFile.toAbsolutePath());

            // convert JSON file to map
            Type type = new TypeToken<HashMap<String, Double>>(){}.getType();
            HashMap<String, Double> map = gson.fromJson(reader, type);

            // close reader
            reader.close();

            for (String player : home) {
            double coef = map.get(player);
            linear_reg += coef;

            }
            for (String player : away) {
                double coef = map.get(player);
                linear_reg -= coef;
            }
            linear_reg += map.get("intercept");

            double logistic_reg = (Math.exp(linear_reg) / (1 + Math.exp(linear_reg)));
            HashMap<String,Double> mymap = new HashMap<String, Double>();
            mymap.put("home_pct", logistic_reg);
            response.setContentType("application/json");
            response.getWriter().println(gson.toJson(mymap));

        } catch (Exception ex) {
            ex.printStackTrace();
        }       
}

//post method
@Override
public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        assert true;
    }
}
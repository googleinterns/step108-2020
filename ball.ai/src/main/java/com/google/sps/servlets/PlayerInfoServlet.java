package com.google.sps.servlets;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/playerInfo")
public class PlayerInfoServlet extends HttpServlet {


    //reads in csv file of players and prints it in the servlet
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        BufferedReader br = null;
        try{
            br = new BufferedReader(new FileReader("players.csv"));
            String contentLine = br.readLine();
            while(contentLine != null){
                response.getWriter().println(contentLine);
                contentLine = br.readLine();
            }
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
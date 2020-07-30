package com.google.sps.servlets;

import com.google.gson.Gson;
import com.google.sps.data.Team;
import java.io.IOException;
import java.util.List;
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
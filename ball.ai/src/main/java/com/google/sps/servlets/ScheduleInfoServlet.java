package com.google.sps.servlets;

import com.google.gson.Gson;
import com.google.sps.data.CSVToObj;
import com.google.sps.data.Game;
import com.google.sps.data.Schedule;
import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.util.List;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/scheduleInfo")
public class ScheduleInfoServlet extends HttpServlet {
  String newDir = "resources/new_schedules/";
  String pastDir = "resources/past_schedules/";
  // Reads in schedule for the specified year and converts it to json
  @Override
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
    response.setContentType("application/json;");
    String filename = null;
    try {
      int year = Integer.parseInt(request.getParameter("year"));
      if (year >= 2013 && year <= 2018) {
        filename = String.format("%s%d.csv", pastDir, year);
      } else {
        response.getWriter().println("false");
      }
    } catch (NumberFormatException e) {
      // Get random new schedule
      File scheduleDir = new File(newDir);
      FileFilter filter = new FileFilter() {
        @Override
        public boolean accept(File f) {
          return f.getName().endsWith(".csv");
        }
      };
      File[] schedules = scheduleDir.listFiles(filter);
      // Random choice
      String choice = schedules[(int)(System.currentTimeMillis() % schedules.length)].getName();
      filename = String.format("%s%s", newDir, choice);
      System.out.println(filename);
    }
    if (filename != null) {
      CSVToObj csv = new CSVToObj();
      List<Game> games = csv.fromFile(filename, Game.class);
      if (games != null) {
        Schedule schedule = new Schedule();
        schedule.addGames(games);
        Gson gson = new Gson();
        response.getWriter().println(gson.toJson(schedule));
      } else {
        response.getWriter().println("false");
      }
    } else {
      response.getWriter().println("false");
    }
  }
}
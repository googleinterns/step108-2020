package com.google.sps.servlets;

import com.google.gson.Gson;
import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/randomSchedule")
public class RandomScheduleServlet extends HttpServlet {
  String newDir = "resources/new_schedules/";
  // Returns a random schedule filename
  @Override
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
    File scheduleDir = new File(newDir);
    FileFilter filter = f -> f.getName().endsWith(".csv");

    // Get random new schedule
    File[] schedules = scheduleDir.listFiles(filter);
    String choice = schedules[(int)(System.currentTimeMillis() % schedules.length)].getName();
    String filename = "/".concat(String.format("%s%s", newDir, choice));

    response.setContentType("application/json;");
    Gson gson = new Gson();
    response.getWriter().println(gson.toJson(filename));
  }
}
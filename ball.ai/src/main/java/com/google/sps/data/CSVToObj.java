package com.google.sps.data;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

public class CSVToObj {
  public <T> List<T> fromFile(String filename, Class<T> c) {
    Field[] fields = c.getFields();
    List<T> list = new ArrayList<>();

    BufferedReader br = null;
    try {
      br = new BufferedReader(new FileReader(filename));
      CSVParser records = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(br);
      for (CSVRecord record : records) {
        try {
          T obj = c.getDeclaredConstructor().newInstance();
          for (Field field : fields) {
            field.set(obj, record.get(field.getName()));
          }
          list.add(obj);
        } catch (InstantiationException | IllegalAccessException | NoSuchMethodException
            | InvocationTargetException e) {
          e.printStackTrace();
        }
      }
    } catch (IOException e) {
      e.printStackTrace();
    } finally {
      try {
        if (br != null) {
          br.close();
        }
      } catch (IOException e) {
        e.printStackTrace();
      }
    }

    return list;
  }
}
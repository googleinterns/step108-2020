const teams = 30;
const days = 176;
let team_arr = [];
for (let i = 0; i < teams; i++) {
  team_arr[i] = [];
}

const svgDiv = document.getElementById("svgContainer");
const svg = d3.select(svgDiv).append("svg");
// Read csv into team_arr
const csv = d3.csv("schedule.csv").then(data => {
  for (let i = 0; i < data.length; i++) {
    // Convert strings to floats
    data[i].day = +data[i].day;
    data[i].team1 = +data[i].team1;
    data[i].team2 = +data[i].team2;
    const home_team = data[i].team1;
    const away_team = data[i].team2;
    team_arr[home_team].push(data[i]);
    team_arr[away_team].push(data[i]);
  }
  redraw();
});

function redraw() {
  // Csv might not be read yet
  if (team_arr[0].length === 0) {
    return;
  }

  // Extract the width and height of the window.
  const width = svgDiv.clientWidth;
  const height = svgDiv.clientHeight;

  // Set the size of the SVG element.
  svg
    .attr("width", width)
    .attr("height", height);

  // Scaling to make space for text
  const rect_g_width = width * 0.93;
  const rect_g_height = height;
  let rect_g = svg.append("g");
  rect_g.attr("transform", `translate(${width - rect_g_width}, 0)`);

  // Rectangle margin
  const epsilon = 1;

  // Move the text onto screen
  const fontsize = 15;
  let text_g = svg.append("g");
  text_g.attr("transform", `translate(0, ${fontsize})`);

  // Draw text and boxes
  for (let i = 0; i < teams; i++) {
    text_g.append("text")
      .attr("x", 0)
      .attr("y", i * rect_g_height / teams)
      .attr("font-family", "sans-serif")
      .attr("font-size", `${fontsize}px`)
      .attr("fill", "black")
      .text(`Team ${i}`);
    for (let j = 0; j < team_arr[i].length; j++) {
      let color = "black";
      if (team_arr[i][j].team2 === i) {
        color = "red";
      }
      rect_g.append("rect")
        .attr("x", j * rect_g_width / 82)
        .attr("y", i * rect_g_height / teams)
        .attr("width", rect_g_width / 82 - epsilon)
        .attr("height", rect_g_height / teams - epsilon)
        .attr("fill", color);
    }
  }
}

// Redraw when the window is resized
window.addEventListener("resize", redraw);
const days = 176;

const firstday = d3.timeDay(new Date("2015-10-20"));
console.log(firstday);

let teams = [];

const teamCsv = d3.csv("/resources/teams.csv").then(data => {
    data.forEach(d => {
        teams.push(d["team_abbrev"]);
    })
});

const scheduleCsv = d3.csv("schedule.csv").then(data => {
    data.forEach(d => {
        // Map to dates and team names
        // d.day = d3.timeDay.offset(firstday, +d.day);
        d.day = +d.day;
        d.team1 = teams[+d.team1];
        d.team2 = teams[+d.team2];
    });

    // Count number of games per day
    let schedule = [];
    for (let i = 0; i < days; i++) {
        const date = d3.timeDay.offset(firstday, i);
        schedule.push({"date": date, "value": data.filter(d => d.day === i).length});
    }
    this.data = data;
    this.schedule = schedule;
    drawCalendar();
});

const svgDiv = document.getElementById("svgContainer");
// Extract the width and height of the window.
const width = svgDiv.clientWidth;
const height = svgDiv.clientHeight;

const svg = d3.select(svgDiv).append("svg");

// Set the size of the SVG element.
svg
    .attr("width", width)
    .attr("height", height);

function drawCalendar() {
    const values = this.schedule.map(d => d.value);
    const maxValue = d3.max(values);
    const minValue = 0;

    console.log(values);

    const cellSize = 40;
    const yearHeight = cellSize * 7;
    const group = svg.append("g");
    group.attr("transform", `translate(50, ${cellSize * 1.5})`)

    group
        .append("text")
        .attr("x", -5)
        .attr("y", -30)
        .attr("text-anchor", "end")
        .attr("font-size", 16)
        .attr("font-weight", 550)
        .attr("transform", "rotate(270)")
        .text("2015");

    const formatDay = d =>
        ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d.getUTCDay()];

    const countDay = d => d.getUTCDay();
    const timeWeek = d3.utcSunday;
    const formatDate = d3.utcFormat("%x");
    const colorFn = d3
        .scaleSequential(d3.interpolateBuGn)
        .domain([Math.floor(minValue), Math.ceil(maxValue)]);
    const format = d3.format("+.2%");

    group
        .append("g")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data(d3.range(7).map(i => new Date(1995, 0, i)))
        .join("text")
        .attr("x", -5)
        .attr("y", d => (countDay(d) + 0.5) * cellSize)
        .attr("dy", "0.31em")
        .attr("font-size", 12)
        .text(formatDay);

    group
        .append("g")
        .selectAll("rect")
        .data(this.schedule)
        .join("rect")
        .attr("width", cellSize - 1.5)
        .attr("height", cellSize - 1.5)
        .attr(
            "x",
            d => timeWeek.count(d3.utcYear(d.date), d.date) * cellSize + 10
        )
        .attr("y", d => countDay(d.date) * cellSize + 0.5)
        .attr("fill", d => colorFn(d.value))
        .on("click", d => {
            const day = d3.timeDay.count(firstday, d.date);
            const games = this.data.filter(d => d.day === day);
            const formatted = games.map(d => `${d.team1} vs. ${d.team2}`)
            alert(formatted.join("\n"));
        })
        .append("title")
        .text(d => `${formatDate(d.date)}: ${d.value}`);

    const legend = group
        .append("g")
        .attr(
            "transform",
            `translate(10, ${yearHeight + cellSize * 2})`
        );

    const categoriesCount = maxValue / 2;
    const categories = [...Array(categoriesCount)].map((_, i) => {
        const upperBound = (maxValue / categoriesCount) * (i + 1);
        const lowerBound = (maxValue / categoriesCount) * i;

        return {
            upperBound,
            lowerBound,
            color: d3.interpolateBuGn(upperBound / maxValue),
            selected: true
        };
    });

    console.log(categories);

    const legendWidth = 60;

    legend
        .selectAll("rect")
        .data(categories)
        .enter()
        .append("rect")
        .attr("fill", d => d.color)
        .attr("x", (d, i) => legendWidth * i)
        .attr("width", legendWidth)
        .attr("height", 15)
    // .on("click", toggle);

    legend
        .selectAll("text")
        .data(categories)
        .join("text")
        // .attr("transform", "rotate(90)")
        .attr("x", (d, i) => legendWidth * i)
        .attr("y", 25)
        .attr("dx", legendWidth / 4)
        .attr("text-anchor", "start")
        .attr("font-size", 11)
        .text(d => `${d.lowerBound} - ${d.upperBound}`);

    legend
        .append("text")
        .attr("dy", -5)
        .attr("font-size", 14)
        .attr("text-decoration", "underline")
    // .text("Click on category to select/deselect days");
}


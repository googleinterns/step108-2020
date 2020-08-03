// ?players={}

const firstDay = d3.timeDay(new Date("2015-10-28"));
const gamesPerTeam = 82;

const svgDiv = document.getElementById("svgContainer");
const collapseDiv = document.getElementById('filterCollapse');
const modalTitle = document.getElementById("modalTitle");
const modalBody = document.getElementById("modalBody");
const svgToggle1 = document.getElementById("svgToggle1");
const svgToggle2 = document.getElementById("svgToggle2");

// Extract the width and height of the window.
const width = svgDiv.clientWidth;
const height = svgDiv.clientHeight;

const svg = d3.select(svgDiv).append("svg");
const collapse = d3.select(collapseDiv).append("svg");

let colorFn = d3.scaleSequential(d3.interpolateBuGn);

let teams = [];
let teamAbbrv = {};
let days = 0;
let workingSet;
let scheduleData;
let finalSchedule;
d3.csv("/resources/teams.csv").then(data => {
    data.forEach(d => {
        teams.push({"abbrv": d["team_abbrev"], "name": `${d["team_name"]} ${d["team_nickname"]}`});
        teamAbbrv[d["team_abbrev"]] = `${d["team_name"]} ${d["team_nickname"]}`;
    });
    loadSchedule();
});

function loadSchedule() {
    d3.csv("schedule.csv").then(data => {
        data.forEach(d => {
            // Map to dates and team names
            d.day = +d.day;
            d.team1 = teams[+d.team1]["abbrv"];
            d.team2 = teams[+d.team2]["abbrv"];
            days = Math.max(d.day, days);
        });
        days++;

        // Count number of games per day
        let schedule = [];
        for (let i = 0; i < days; i++) {
            const date = d3.timeDay.offset(firstDay, i);
            schedule.push({"date": date, "value": data.filter(d => d.day === i).length});
        }
        scheduleData = data;
        workingSet = new Set(data);
        finalSchedule = schedule;
        drawFilter(drawCalendar());
        // drawTeamSchedule(teams[0]);
    });
}

function drawCalendar() {
    clear(svgDiv)
    const values = finalSchedule.map(d => d.value);
    let maxValue = Math.max(...values);

    const cellSize = 40;
    const yearHeight = cellSize * 7;
    const season = svg.append("g");
    season.attr("transform", `translate(50, ${cellSize * 1.5})`)

    // season
    //     .append("text")
    //     .attr("x", 50)
    //     .attr("y", -10)
    //     .attr("text-anchor", "end")
    //     .attr("font-size", 16)
    //     .attr("font-weight", 550)
    //     // .attr("transform", "rotate(270)")
    //     .text("2015");

    var yearDiv = season.append("foreignObject")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("x", 0)
        .attr("y", -40)
    //     .attr("class", "col-auto")
    //
    //
    //
    // yearDiv.append("xhtml:select")
    //     .attr("class", "custom-select")
    //     .selectAll("option")
    //     .data([1, 2, 3])
    //     .join("option")
    //     .attr("value", d => d)
    //     .text(d => d)

    const yearButton = yearDiv.append("xhtml:button")
        .attr("class", "btn btn-primary dropdown-toggle")
        .attr("id", "selectYear")
        .attr("type", "button")
        .attr("data-toggle", "dropdown")
        .text("Select year")
        // .append("xhtml:span")
        .on("click", () => {
            const rects = Array(...document.getElementsByTagName('rect'));
            rects.forEach(d => {
                d.style.pointerEvents = "none";
            });
            window.onclick = () => {
                rects.forEach(d => {
                    d.style.pointerEvents = "all";
                });
                window.onclick = null;
            }
        });

    yearDiv.append("xhtml:div")
        .attr("class", "dropdown-menu")
        .attr("aria-labelledby", "selectYear")
        .selectAll("option")
        .data([2015, 2016, 2017, 2018, 2019])
        .join("a")
        .attr("class", "dropdown-item")
        .on("click", (d, i, nodes) => {
            yearButton.text(d);
            nodes[i].classList.add("disabled");
        })
        .text(d => d);


    const formatDay = d =>
        ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d];

    const formatDate = d3.utcFormat("%x");
    colorFn.domain([0, maxValue]);

    season
        .append("g")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data([...d3.range(7)])
        .join("text")
        .attr("x", -5)
        .attr("y", d => (d + 0.5) * cellSize)
        .attr("dy", "0.31em")
        .attr("font-size", 12)
        .text(formatDay);

    season
        .append("g")
        .selectAll("rect")
        .data(finalSchedule, d => d.date)
        .join("rect")
        .attr("width", cellSize - 1.5)
        .attr("height", cellSize - 1.5)
        .attr("x", d => d3.utcSunday.count(firstDay, d.date) * cellSize + 10)
        .attr("y", d => d.date.getUTCDay() * cellSize + 0.5)
        .attr("fill", d => colorFn(d.value))
        .attr("data-toggle", "modal")
        .attr("data-target", "#scheduleModal")
        .on("click", data => {
            while (modalBody.firstChild) {
                modalBody.removeChild(modalBody.lastChild);
            }

            modalTitle.innerText = formatDate(data.date);
            const day = d3.timeDay.count(firstDay, data.date);
            const games = scheduleData.filter(d => d.day === day);
            const formatted = games.map(d => `${d.team1} vs. ${d.team2}`)
            for (let i = 0; i < formatted.length; i++) {
                let li = document.createElement("li");
                li.innerText = formatted[i];
                li.classList.add("list-group-item");
                li.onclick = e => {
                    for (let j = 0; j < modalBody.children.length; j++) {
                        let classes = modalBody.children[j].classList;
                        if (classes.contains("active")) {
                            classes.remove("active");
                            break;
                        }
                    }
                    e.target.classList.add("active");
                }
                modalBody.appendChild(li);
            }
        })
        .append("title")
        .text(d => `${formatDate(d.date)}: ${d.value}`);

    // Stretch node for overflow
    stretch(svg);

    return season;
}

function drawFilter(schedule) {
    clear(collapseDiv);
    const filter = collapse
        .append("g")
        // .attr("transform", `translate(10, ${yearHeight + cellSize * 2})`);
        .attr("transform", `translate(10, 0)`);

    const rowLen = 6;
    const categories = teams.map(t => {
        return {
            abbrv: t["abbrv"],
            src: `/resources/logos/${t["name"]}.png`,
            selected: true
        }
    });

    const imageWidth = 60;

    const paddingX = 30;
    const paddingY = 15;
    filter
        .selectAll("image")
        .data(categories)
        .join("image")
        .attr('xlink:href', d => d.src)
        .attr("x", (d, i) => (imageWidth + paddingX) * (i % rowLen))
        .attr("y", (d, i) => (imageWidth + paddingY) * (Math.floor(i / rowLen)))
        .attr("width", imageWidth)
        .attr("height", imageWidth)
        .on("click", legendClick);

    function legendClick(data, i, nodes) {
        const {selected} = data;
        data.selected = !selected;
        nodes[i].style.opacity = data.selected ? 1 : 0.2;
        console.log(svgToggle1.classList);

        if (isActive(svgToggle1)) {
            // Season schedule
            const change = data.selected ? g => {
                if (workingSet.has(g)) {
                    return false
                } else {
                    return workingSet.add(g);
                }
            } : workingSet.delete
            const boundChange = change.bind(workingSet);

            // "Dirty" indices
            const teamArr = new Array()
            scheduleData.forEach(g => {
                if (g.team1 === data.abbrv || g.team2 === data.abbrv) {
                    if (boundChange(g)) {
                        teamArr.push(g)
                    }
                }
            });
            const teamDays = teamArr.map(g => finalSchedule[g.day]);
            // Update number of games per day
            data.selected ? teamDays.forEach(g => g.value++) : teamDays.forEach(g => g.value--);
            let max = 0
            for (let day in teamDays) {
                max = Math.max(max, teamDays[day].value);
            }
            colorFn.domain([0, max + 1])

            schedule.selectAll("rect")
                .data(teamDays, d => d.date)
                .transition()
                .duration(500)
                .attr('fill', d => colorFn(d.value));
        } else {
            // Team schedule
            console.log(i);
            console.log(data);
            console.log(nodes[i])
        }
    }

    stretch(collapse);
}

function drawTeamSchedule(team) {
    clear(svgDiv);
    const teamSchedule = scheduleData.filter(d => d.team1 === team.abbrv || d.team2 === team.abbrv);
    const rows = 4;
    const baseCellSize = 40;
    const cellSize = baseCellSize * 7 / rows;
    const yearHeight = baseCellSize * 7;
    const schedule = svg.append("g");
    schedule.attr("transform", `translate(50, ${baseCellSize * 1.4})`)

    schedule
        .append("text")
        .attr("x", 50)
        .attr("y", -10)
        .attr("text-anchor", "end")
        .attr("font-size", 16)
        .attr("font-weight", 550)
        // .attr("transform", "rotate(270)")
        .text(team.abbrv);

    schedule
        .append("g")
        .selectAll("image")
        .data(teamSchedule)
        .join("image")
        .attr("xlink:href", d => `/resources/logos/${teamAbbrv[neqTeam(d, team)]}.png`)
        .attr("width", cellSize - 1.5)
        .attr("height", cellSize - 1.5)
        .attr("x", (d, i) => (i % Math.ceil(gamesPerTeam / rows)) * cellSize + 0.5)
        .attr("y", (d, i) => Math.floor(i / Math.ceil(gamesPerTeam / rows)) * cellSize + 10)
        // .attr("data-toggle", "modal")
        // .attr("data-target", "#scheduleModal")
        .append("title")
        .text((d, i) => `Game ${i}`);

    const winColor = game => {
        return game.team1 === team.abbrv ? "green" : "red";
    }
    schedule
        .append("g")
        .selectAll("rect")
        .data(teamSchedule)
        .join("rect")
        .attr("width", cellSize - 4)
        .attr("height", cellSize - 4)
        .attr("x", (d, i) => (i % Math.ceil(gamesPerTeam / rows)) * cellSize + 0.5 + 2)
        .attr("y", (d, i) => Math.floor(i / Math.ceil(gamesPerTeam / rows)) * cellSize + 10 + 2)
        .attr("stroke", winColor)
        .attr("stroke-width", 3)
        .attr("fill-opacity", 0);

    // schedule.append("g")
    stretch(svg);

    return schedule;
}

function swapCalendar(e) {
    if (isActive(svgToggle1)) {
        if (e.target.id === "svgToggle1") {
            return false;
        }
        const schedule = drawTeamSchedule(teams[0]);
        drawFilter(schedule);
    } else {
        if (e.target.id === "svgToggle2") {
            return false;
        }
        const season = drawCalendar()
        drawFilter(season);
    }
}

function stretch(svg) {
    const svgBox = svg.node().getBBox();
    svg
        .attr("width", svgBox.x + svgBox.width + svgBox.x)
        .attr("height",  svgBox.y + svgBox.height + svgBox.y);
}

function clear(node) {
    $(node.children[0]).empty();
}

function neqTeam(game, team) {
    return game.team1 === team.abbrv ? game.team2 : game.team1
}

function isActive(ele) {
    return ele.classList.contains("active")
}
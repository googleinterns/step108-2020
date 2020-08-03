// ?players={}

var url = new URL(window.location.href);
var urlTeam = url.searchParams.get("team");

const firstDay = d3.timeDay(new Date("2015-10-28"));
const gamesPerTeam = 82;
const emptySet = new Set();
let currentTeam;

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
const formatDate = d3.utcFormat("%x");

let teams = [];
let teamAbbrv = {};
let days = 0;
let workingSetAll;
let scheduleData;
let finalSchedule;
d3.csv("/resources/teams.csv").then(data => {
    let validUrlTeam = false;
    data.forEach(d => {
        if (urlTeam === d["team_abbrev"]) {
            validUrlTeam = true;
        }
        teams.push({"abbrv": d["team_abbrev"], "name": `${d["team_name"]} ${d["team_nickname"]}`});
        teamAbbrv[d["team_abbrev"]] = `${d["team_name"]} ${d["team_nickname"]}`;
    });
    currentTeam = validUrlTeam ? teams.filter(t => t.abbrv === urlTeam)[0] : teams[0];
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
        const schedule = daySchedule(data, emptySet);
        scheduleData = data;
        workingSetAll = new Set(data);
        finalSchedule = schedule;
        drawFilter(drawCalendar());
        // drawTeamSchedule(teams[0]);
    });
}

// Could save memory by separating date and value + speed up w/o filter() but it's not significant
function daySchedule(data, teams) {
    let schedule = [];
    for (let i = 0; i < days; i++) {
        const date = d3.timeDay.offset(firstDay, i);
        // Count number of games for each day
        schedule.push({"date": date, "value": data.filter(d => d.day === i && !teams.has(d.team1) && !teams.has(d.team2)).length});
    }
    return schedule;
}

function drawCalendar() {
    clear(svgDiv)
    const values = finalSchedule.map(d => d.value);
    let maxValue = Math.max(...values);

    const cellSize = 40;
    const yearHeight = cellSize * 7;
    const season = svg.append("g");
    season.attr("transform", `translate(50, ${cellSize * 1.5})`)

    var yearDiv = season.append("foreignObject")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("x", 0)
        .attr("y", -40)

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

/** @param {D3 selection} schedule Selection to update */
function drawFilter(schedule) {
    let workingSet = new Set(workingSetAll);
    let tmpSchedule = daySchedule(scheduleData, emptySet);
    let teamSchedule = scheduleData.filter(d => (d.team1 === currentTeam.abbrv || d.team2 === currentTeam.abbrv));
    let filterTeams = new Set();

    clear(collapseDiv);
    const filter = collapse
        .append("g")
        .attr("transform", `translate(10, 0)`);

    // Get logo files
    const rowLen = 6;
    const categories = teams.map(t => {
        return {
            abbrv: t["abbrv"],
            src: `/resources/logos/${t["name"]}.png`,
            selected: true
        }
    });

    // Draw logos
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

    // Handle filtering for each schedule variant
    function legendClick(data, i, nodes) {
        const {selected} = data;
        data.selected = !selected;
        nodes[i].style.opacity = data.selected ? 1 : 0.2;
        data.selected ? filterTeams.delete(data.abbrv) : filterTeams.add(data.abbrv);

        if (isActive(svgToggle1)) {
            // Season schedule
            tmpSchedule = daySchedule(scheduleData, filterTeams);
            let max = 0;
            tmpSchedule.forEach(day => max = Math.max(max, day.value))

            /*
            // Cheaper but more complex to catch all cases
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
                 if ((g.team1 === data.abbrv || g.team2 === data.abbrv) && boundChange(g)) {
                     teamArr.push(g)
                 }
             });
             const teamDays = teamArr.map(g => Object.assign(tmpSchedule[g.day]));
             // Update number of games per day
             data.selected ? teamDays.forEach(g => g.value++) : teamDays.forEach(g => g.value--);
             let max = 0
             for (let day in teamDays) {
                 max = Math.max(max, teamDays[day].value);
             }
             */

            colorFn.domain([0, max + 1])

            // Update color
            schedule.selectAll("rect")
                .data(tmpSchedule, d => d.date)
                .transition()
                .duration(500)
                .attr('fill', d => colorFn(d.value));

            // Update hover text
            schedule.selectAll("title")
                .data(tmpSchedule, d => d.date)
                .text(d => `${formatDate(d.date)}: ${d.value}`);


        } else {
            // Team schedule
            let showTeams = teamSchedule.filter(d => !filterTeams.has(d.team1) && !filterTeams.has(d.team2));
            schedule.selectAll("image")
                .data(showTeams, d => teamSchedule.indexOf(d))
                .join(
                    enter => enter,
                    update => update
                        .style("opacity", 1),
                    exit => exit
                        .style("opacity", 0.2)
                );
        }
    }

    stretch(collapse);
}

function drawTeamSchedule(team) {
    clear(svgDiv);
    const teamSchedule = scheduleData.filter(d => d.team1 === team.abbrv || d.team2 === team.abbrv);
    console.log(teamSchedule);
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

    stretch(svg);
    return schedule;
}

function swapCalendar(e) {
    if (isActive(svgToggle1)) {
        if (e.target.id === "svgToggle1") {
            return false;
        }
        const schedule = drawTeamSchedule(currentTeam);
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
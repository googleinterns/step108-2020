const firstDay = d3.timeDay(new Date("2015-10-28"));
const gamesPerTeam = 82;

const svgDiv = document.getElementById("svgContainer");
const collapseDiv = document.getElementById('filterCollapse');
const modalTitle = document.getElementById("modalTitle");
const modalBody = document.getElementById("modalBody");
// Extract the width and height of the window.
const width = svgDiv.clientWidth;
const height = svgDiv.clientHeight;

const svg = d3.select(svgDiv).append("svg");
const collapse = d3.select(collapseDiv).append("svg");

let teams = [];
let days = 0;
d3.csv("/resources/teams.csv").then(data => {
    data.forEach(d => {
        teams.push({"abbrv": d["team_abbrev"], "name": `${d["team_name"]} ${d["team_nickname"]}`});
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
        this.data = data;
        this.workingSet = new Set(data);
        this.schedule = schedule;
        drawCalendar();
    });
}

function drawCalendar() {
    const values = this.schedule.map(d => d.value);
    let maxValue = Math.max(...values);

    const cellSize = 40;
    const yearHeight = cellSize * 7;
    const season = svg.append("g");
    season.attr("transform", `translate(50, ${cellSize * 1.5})`)

    season
        .append("text")
        .attr("x", -5)
        .attr("y", -30)
        .attr("text-anchor", "end")
        .attr("font-size", 16)
        .attr("font-weight", 550)
        .attr("transform", "rotate(270)")
        .text("2015");

    const formatDay = d =>
        ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d];

    const formatDate = d3.utcFormat("%x");
    let colorFn = d3
        .scaleSequential(d3.interpolateBuGn)
        .domain([0, maxValue]);

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
        .data(this.schedule, d => d.date)
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
            const games = this.data.filter(d => d.day === day);
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

    const legend = collapse
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
    legend
        .selectAll("image")
        .data(categories)
        .join("image")
        .attr('xlink:href', d => d.src)
        .attr("x", (d, i) => (imageWidth + paddingX) * (i % rowLen))
        .attr("y", (d, i) => (imageWidth + paddingY) * (Math.floor(i / rowLen)))
        .attr("width", imageWidth)
        .attr("height", imageWidth)
        .on("click", (data, i, nodes) => {
            const {src, selected} = data;
            data.selected = !selected;
            nodes[i].style.opacity = data.selected ? 1 : 0.2;

            const change = data.selected ? g => {
                if (this.workingSet.has(g)) {
                    return false
                } else {
                    return this.workingSet.add(g);
                }
            } : this.workingSet.delete
            const boundChange = change.bind(this.workingSet);

            // "Dirty" indices
            const teamArr = new Array()
            this.data.forEach(g => {
                if (g.team1 === data.abbrv || g.team2 === data.abbrv) {
                    if (boundChange(g)) {
                        teamArr.push(g)
                    }
                }
            })
            const teamDays = teamArr.map(g => this.schedule[g.day]);
            // Update number of games per day
            data.selected ? teamDays.forEach(g => g.value++) : teamDays.forEach(g => g.value--);
            let max = 0
            for (let day in teamDays) {
                max = Math.max(max, teamDays[day].value);
            }
            colorFn.domain([0, max + 1])

            season.selectAll("rect")
                .data(teamDays, d => d.date)
                .transition()
                .duration(500)
                .attr('fill', d => colorFn(d.value));
        });

    // Stretch node for overflow
    const svgs = [svg, collapse];
    stretch(svgs);
}

function stretch(svgs) {
    for (let svgIdx in svgs) {
        const svg = svgs[svgIdx];
        const svgBox = svg.node().getBBox();
        svg
            .attr("width", svgBox.x + svgBox.width + svgBox.x)
            .attr("height",  svgBox.y + svgBox.height + svgBox.y);
    }
}
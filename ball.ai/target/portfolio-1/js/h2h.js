function predictProba(){
    const home = document.getElementById("home-team").value.split(/\r?\n/).map(v => v.toLowerCase()).map(v => v.replace(/\s+/g, '')); 
    var filtered_home = home.filter(function (el) {return el != "";});
    const away = document.getElementById("away-team").value.split(/\r?\n/).map(v => v.toLowerCase()).map(v => v.replace(/\s+/g, ''));
    var filtered_away = away.filter(function (el) {return el != "";});
    console.log(filtered_home)
    console.log(filtered_away)

    var url = "/k-hot?";
    url = url.concat("home=")
    for (var i = 0; i < filtered_home.length; i ++) {
        url = url.concat(filtered_home[i], "|")
    }
    url = url.concat("&away=")
    for (var i = 0; i < filtered_away.length; i ++) {
        url = url.concat(filtered_away[i], "|")
    }
    
    fetch(url).then(response => response.json()).then((returnObj) => {
        console.log(returnObj["home_pct"])
        var pct_chance = parseFloat(returnObj["home_pct"]).toFixed(3);
        document.getElementById("results-display").innerText = "Probability of Home team winning is: ".concat(pct_chance*100, "%");
    });
}


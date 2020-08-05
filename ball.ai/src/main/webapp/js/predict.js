var jsondict = {};
var model;

//ONLOAD FUNC
async function loadData() {
    $(".dropdown-toggle").width(43)
    //FIRST SUBFUNCTION WE WANT - LOAD NECESSARY JSONS
    await loadSingleJson("ids_dict");
    await loadSingleJson("starters_dict");
    await loadSingleJson("raw_player_names");
    await loadSingleJson("player_info_dict");
    model = await tf.loadLayersModel('resources/nn_model/tfjs-model/model.json');

    await allowSim();
}

async function allowSim() {
    const simButton = document.getElementById("simButton");
    simButton.disabled = false;
    simButton.innerHTML = "Simulate";
}

async function loadSingleJson(jsonName) {
    await fetch('/resources/nn_model/aux-files/'.concat(jsonName, ".json")).then((response) => response.json()).then((data) => {
        jsondict[jsonName] = data;
    })
}

function loadYears(prefix) {
    var playername = document.getElementById(prefix.concat("name")).value;
    if (playername == "") {
        var playername = document.getElementById(prefix.concat("name")).placeholder;
    }
    const playerid = jsondict["ids_dict"][playername];
    const years_avail = jsondict["player_info_dict"][playerid]["seasons_avail"];

    var div = document.getElementById(prefix.concat("year", "_dropdown"));
    div.innerHTML = "";
    years_avail.forEach(year => {
        div.innerHTML += `<a class="dropdown-item">${year}</a>`;
    });
}

//simulation outer loop
async function simulate() {

    //checkValidInputs();
    if (!("train_std" in jsondict)) {
        await loadSingleJson("train_std");
        await loadSingleJson("train_mean");
    }

    var raw_arr = await generateDataset();
    var pred = await predict(raw_arr);
    await displayResults(pred);
}

async function displayResults(pred) {

    var pred_pct = pred*100; //float
    var roundpred = pred_pct.toFixed(1); //string
    var intpred = Math.round(pred_pct); //int

    var pred_pct_aw = (1-pred)*100; //float
    var roundpred_aw = pred_pct_aw.toFixed(1); //string
    var intpred_aw = Math.round(pred_pct_aw); //int

    var i = 0;
    function makeProgress(){
        if(i < intpred){
            i = i + 1;
            $("#progress-bar-home").css("width", i + "%").text(i + " %");
            $("#progress-bar-away").css("width", (100-i) + "%").text((100-i) + " %");
            setTimeout(makeProgress(), 50);
        }
    }
    makeProgress();
    $("#progress-bar-home").text(roundpred.concat("% Home")).css({"width":roundpred.concat("%")});
    $("#progress-bar-away").text(roundpred_aw.concat("% Away")).css({"width":roundpred_aw.concat("%")});

}

async function generateDataset() {
    var keys = [];
    for(var k in jsondict["train_mean"]) {keys.push(k);}
    var raw_arr = [];
    leftovers = keys.slice(-5)
    keys = keys.slice(0, -5)

    keys.forEach(function(entry) {
        const first_pref = entry.slice(0, 5);
        if (first_pref.slice(3, 4) == "c") {var prefix = first_pref}
        else {var prefix = entry.slice(0, 7)}
        var stat = entry.slice(prefix.length);

        var playername = document.getElementById(prefix.concat("name")).value;
        if (playername == "") {
            var playername = document.getElementById(prefix.concat("name")).placeholder;
        }
        var playerid = jsondict["ids_dict"][playername];

        var season = document.getElementById(prefix.concat("year")).value;
        if (season == "") {
            var season = Math.max.apply(Math, jsondict["player_info_dict"][playerid]["seasons_avail"]);
            $("#".concat(prefix,"year")).text(season).append(' <span class="caret"></span>').prop("value", season);
        }
        var statvalue = jsondict["player_info_dict"][playerid][season][stat];
        raw_arr.push(statvalue)
    });

    leftovers.forEach(function(entry) {
        raw_arr.push(jsondict["train_mean"][entry])
    });

    return raw_arr;
}

async function predict(raw_arr) {

    var means = Object.values(jsondict["train_mean"]);
    var stds = Object.values(jsondict["train_std"]);
    normalized_arr = [];

    for (var i = 0; i < means.length; i++) {
        normalized_arr.push((raw_arr[i]-means[i])/stds[i]);
    }

    const norm_tensor = tf.tensor(normalized_arr, [1,465]);
    var evaluated_tensor = model.predict(norm_tensor);
    const values = evaluated_tensor.dataSync();
    const arr = Array.from(values);
    return arr[0]
}

//simulation outer loop
async function simulate_for_jeremy(hm_arr, aw_arr) { //[array of length 5 ... each item is "firstname lastname year position"]
    var d = {}
    function parse_players(arr, prefix) {
        arr.forEach(entry => {
            const pos = entry.slice(-1);
            const season = entry.slice(-5, -1);
            const name = entry.slice(0, -5);
            let index;
            if (pos === "c") {
                index = prefix.concat("c_");
            } else if (prefix.concat(pos, "_1_") in d) {
                index = prefix.concat(pos, "_2_");
            } else {
                index = prefix.concat(pos, "_1_");
            }
            d[index] = {
                "name": name,
                "season": season
            };
        });
    }

    parse_players(hm_arr, "hm_");
    parse_players(aw_arr, "aw_");

    //checkValidInputs();
    if (!("train_std" in jsondict)) {
        await loadSingleJson("train_std");
        await loadSingleJson("train_mean");
        await loadSingleJson("ids_dict");
        await loadSingleJson("starters_dict");
        await loadSingleJson("raw_player_names");
        await loadSingleJson("player_info_dict");
        model = await tf.loadLayersModel('resources/nn_model/tfjs-model/model.json');
    }

    var raw_arr = await generateDataset_jeremy(d);
    var pred = await predict(raw_arr);
    return pred;
}

async function generateDataset_jeremy(d) {
    var keys = [];
    for(var k in jsondict["train_mean"]) {keys.push(k);}
    var raw_arr = [];
    leftovers = keys.slice(-5)
    keys = keys.slice(0, -5)

    keys.forEach(function(entry) {
        const first_pref = entry.slice(0, 5);
        if (first_pref.slice(3, 4) == "c") {var prefix = first_pref}
        else {var prefix = entry.slice(0, 7)}
        var stat = entry.slice(prefix.length);

        var playername = d[prefix]["name"];
        var season = d[prefix]["season"];
        var playerid = jsondict["ids_dict"][playername];
        var statvalue = jsondict["player_info_dict"][playerid][season][stat];
        raw_arr.push(statvalue)
    });

    leftovers.forEach(function(entry) {
        raw_arr.push(jsondict["train_mean"][entry])
    });

    return raw_arr;
}

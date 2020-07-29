var aw_train_mean;
var aw_train_std;
var hm_train_mean;
var hm_train_std;
var playername_encodings_dict;

async function loadData() {
    var lst_of_required_datasets = ["aw_train_mean", "aw_train_std", "hm_train_mean", "hm_train_std", "playername_encodings_dict"]
    lst_of_required_datasets.forEach(async function(entry) {
            await fetch('/resources/nn_model/aux-files/'.concat(entry, ".json")).then((response) => response.json()).then((data) => {
                eval(entry + "= data;");
            });
        }); 
    
    const myButton = document.getElementById("myButton");
    myButton.disabled = false;
}

function test() {
    const playername = document.getElementById("hm_g_1_name").innerText;
    const year = document.getElementById("hm_g_1_year").innerText;
    console.log(playername, year);
}
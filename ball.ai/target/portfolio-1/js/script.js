google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart);

function searchFunction() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('searchQuery');
  filter = input.value.toUpperCase();
  ul = document.getElementById("listPlayers");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

//draws a chart of players selected by the user
function drawChart(){
  fetch('/playerInfo').then(response => response.json()).then((team) => {
    text = localStorage.getItem("playersArray");
    selectedPlayers = JSON.parse(text);
    const players = Object.values(team);
    var data = new google.visualization.DataTable();
    var counter = 1;
    const map = new Map(Object.entries(team));
    for(i=0;i < selectedPlayers.length;i++){
      if(i==0){
        data.addColumn('string','Stats');
        data.addRows(3);
        data.setCell(0,0,'PPG');
        data.setCell(1,0,'REB');
        data.setCell(2,0,'STL');
      }
      if(map.has(selectedPlayers[i].id)){
        data.addColumn('number',map.get(selectedPlayers[i].id).name);
        data.setCell(0,counter,map.get(selectedPlayers[i].id).points);
        data.setCell(1,counter,map.get(selectedPlayers[i].id).rebounds);
        data.setCell(2,counter,map.get(selectedPlayers[i].id).steals);
        counter++;
      }
      console.log("hi");
      /*for(j=0; j < selectedPlayers.length; j++){
        console.log(selectedPlayers[j].name);
        if(selectedPlayers[j].name==players[i].name && 
          selectedPlayers[j].year==players[i].year){
          data.addColumn('number',players[i].name);
          data.setCell(0,counter,players[i].points);
          data.setCell(1,counter,players[i].rebounds);
          data.setCell(2,counter,players[i].steals);
          counter++;
        }
      }*/
    }
    var options = {
      colors:['gray'],
      width: 600,
      height: 400,
      legend: { position: 'top', maxLines: 3 },
      bar: { groupWidth: '75%' },
      isStacked: true,
    };

    var chart = new google.charts.Bar(document.getElementById('chart-container'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
  });
}

//adds a player to the area in storage
function choosePlayer(id){
  text = localStorage.getItem("playersArray");
  var players = JSON.parse(text);
  var sname = document.getElementById('player-input'+id).value;
  var season = document.getElementById('year-input'+id).value;
  player ={
    name: sname,
    year: season,
    id: sname+season,
  }
  if(players[0].name==""){
    players[0]=player;
  }else{
    players.push(player);
  }
  console.log(player.name);
  var playerJSON = JSON.stringify(players);
  localStorage.setItem("playersArray",playerJSON);
  drawChart();
}

//creates an empty array of players and stores it
function createPlayersArray(){
  var players = new Array();
  player ={
    name: "",
    year: "",
    id: "",
  }
  players.push(player);
  var playerJSON = JSON.stringify(players);
  localStorage.setItem("playersArray",playerJSON);
}


google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart);

const selectedPlayers = new Array();

function search(){
  fetch('/search').then(response => response.json()).then((players) => {
    const listPlayers = Object.keys(players);
    const seasonsPlayed = new Map(Object.entries(players));
    input = document.getElementById('searchQuery').value;
    document.getElementById('list').innerHTML= '';
    counter = 0;
    for(i=0; i < listPlayers.length;i++){
      if(((listPlayers[i].toLowerCase()).indexOf(input.toLowerCase()))>-1){

        var node = document.createElement("option"); 
        var val = document.createTextNode(listPlayers[i]); 
        node.appendChild(val); 

        document.getElementById('list').appendChild(node); 
        counter++;
        if(counter >6){
          break;
        }
      }
    }
  });
}

function selectedPlayer(){
  fetch('/search').then(response => response.json()).then((players) => {
    const seasonsPlayed = new Map(Object.entries(players));
    input = document.getElementById('searchQuery').value;
    document.getElementById('list').innerHTML= '';
    counter = 0;

    var player = document.createElement('ul');
    player.id = 'listPlayers';
    var liElement = document.createElement('li');
    liElement.innerText = input;
    var datalist = document.createElement('datalist');
    datalist.id = 'seasons';
    var season = document.createElement('input');
    season.type = 'text';
    season.list = 'seasons';

    for(j=0; j< seasonsPlayed.get(input).length;j++){
      var opt = document.createElement("option");
      var value = document.createTextNode(seasonsPlayed.get(input)[j])
      opt.appendChild(value);
      datalist.appendChild(opt);
    }
    liElement.appendChild(season);
    liElement.appendChild(datalist);
    player.appendChild(liElement);
    document.getElementById('selectedPlayer').appendChild(player);

  });
}

//draws a chart of players selected by the user
function drawChart(){
  fetch('/playerInfo').then(response => response.json()).then((team) => {
    const players = new Map(Object.entries(team));
    var data = new google.visualization.DataTable();
    var counter = 1;
    for(i=0;i < selectedPlayers.length;i++){
      if(i==0){
        data.addColumn('string','Stats');
        data.addRows(3);
        data.setCell(0,0,'PPG');
        data.setCell(1,0,'REB');
        data.setCell(2,0,'STL');
      }
      if(players.has(selectedPlayers[i].id)){
        data.addColumn('number',players.get(selectedPlayers[i].id).name);
        data.setCell(0,counter,players.get(selectedPlayers[i].id).points);
        data.setCell(1,counter,players.get(selectedPlayers[i].id).rebounds);
        data.setCell(2,counter,players.get(selectedPlayers[i].id).steals);
        counter++;
      }

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
  var name = document.getElementById('player-input'+id).value;
  var season = document.getElementById('year-input'+id).value;
  player ={
    id: name+season,
  }
  selectedPlayers.push(player);
  console.log(player.id);
  drawChart();
}




google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart);

const selectedPlayers = new Array();
var listId = 0;

function search(){
  fetch('/search').then(response => response.json()).then((players) => {
    const listPlayers = Object.keys(players);
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

//creates an element of the players chosen
function selectedPlayer(){
  fetch('/search').then(response => response.json()).then((players) => {
    const playerInfo = new Map(Object.entries(players));
    input = document.getElementById('searchQuery').value;
    document.getElementById('list').innerHTML= '';

    var player = document.getElementById('listPlayers');
    var liElement = document.createElement('li');
    liElement.id=listId;
    liElement.innerText = input;
    var datalist = document.createElement('datalist');
    datalist.id = 'seasons'+listId;
    var season = document.createElement('input');
    season.placeholder = 'Select a season';
    season.type = 'number';
    season.setAttribute('list','seasons'+listId);
    listId++;
    const addPlayerButton = document.createElement('input');
    addPlayerButton.type = 'button';
    addPlayerButton.value = 'Add Player';
    const deletePlayerButton = document.createElement('input');
    deletePlayerButton.type = 'button';
    deletePlayerButton.value = 'Remove Player';
    const position = document.createElement('input');
    position.placeholder = 'choose position';
    position.setAttribute('list','positions');
    position.innerHTML = '<datalist id="positions">'+
                            '<option>PG</option>'+
                            '<option>SG</option>'+
                            '<option>SF</option>'+
                            '<option>PF</option>'+
                            '<option>C</option>'+
                          '</datalist>';
    position.value = 'PG';

    //button adds the selected player to the chart
    addPlayerButton.addEventListener('click',() => {
      player ={
        id: input+season.value,
      }
      createPlayernode(input,playerInfo.get(input).player_id,player.id,position.value);
      selectedPlayers.push(player);
      console.log(player.id);
      drawChart();
    });

    deletePlayerButton.addEventListener('click',() => {
      liElement.remove();
    });

    for(j=0; j< playerInfo.get(input).seasonsPlayed.length;j++){
      var opt = document.createElement("option");
      var value = document.createTextNode(playerInfo.get(input).seasonsPlayed[j])
      opt.appendChild(value);
      datalist.appendChild(opt);
    }
    liElement.appendChild(season);
    liElement.appendChild(datalist);
    liElement.appendChild(position);
    liElement.appendChild(addPlayerButton);
    liElement.appendChild(deletePlayerButton);
    player.appendChild(liElement);

  });
}

function createPlayernode(name,id,playerid,pos){
  var container  = document.getElementById(''+pos+'-container');
  var player = document.createElement('li');
  player.innerText = name;
  var url = "/images/downsize_player/"+id+".jpg"
  var img = document.createElement('img');
  img.height = "60";
  player.appendChild(img);
  var deleteButton = document.createElement('input');
  deleteButton.type = 'button';
  deleteButton.value = 'remove from team';

  //removes player from chart
  deleteButton.addEventListener('click',() => {
    player.remove();
    for(i=0; i < selectedPlayers.length;i++){
      if(selectedPlayers[i].id == playerid){
        selectedPlayers.splice(i,i+1);
      }
    }
    drawChart();
    
  });
  player.appendChild(deleteButton);
  //if(imageExists(url)){
    img.src = url;
  //}
  container.appendChild(player);
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
        data.addRows(5);
        data.setCell(0,0,'PPG');
        data.setCell(1,0,'AST');
        data.setCell(2,0,'REB');
        data.setCell(3,0,'STL');
        data.setCell(4,0,'BLK');

      }
      if(players.has(selectedPlayers[i].id)){
        data.addColumn('number',players.get(selectedPlayers[i].id).name);
        data.setCell(0,counter,players.get(selectedPlayers[i].id).points);
        data.setCell(1,counter,players.get(selectedPlayers[i].id).assists);
        data.setCell(2,counter,players.get(selectedPlayers[i].id).rebounds);
        data.setCell(3,counter,players.get(selectedPlayers[i].id).steals);
        data.setCell(4,counter,players.get(selectedPlayers[i].id).blocks);
        counter++;
      }

    }
    var options = {
      //colors:['gray'],
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

function onInput() {
  var val = document.getElementById('searchQuery').value;
  var opts = document.getElementById('list').childNodes;
  for (var i = 0; i < opts.length; i++) {
    if (opts[i].value === val) {
      selectedPlayer();
      break;
    }
  }
}

function imageExists(url){

  var image = new Image();

  image.src = url;

  if (!image.complete) {
      return false;
  }
  else if (image.height === 0) {
      return false;
  }

  return true;
}



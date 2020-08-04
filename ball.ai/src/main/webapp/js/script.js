google.charts.load('current', {'packages':['bar']});

const selectedPlayers = new Array();

/**
 * @return object of players and lists of years they played
 */
async function getPlayers() {
  const response = await fetch('/search');
  const players = await response.json();
  return players;
}

/**
 * @return current input in searchQuery
 */
function getInput() {
  return document.getElementById('searchQuery').value;
}

/**
 * Auto completes users input by providing options to select based on their input
 */
async function search() {
  document.getElementById('list').innerHTML = '';
  const players = await getPlayers();
  const listPlayers = Object.keys(players);
  input = getInput();
  counter = 0;
  for (i = 0; i < listPlayers.length; i++){
    if (((listPlayers[i].toLowerCase()).indexOf(input.toLowerCase())) > - 1 && counter < 6) {
      var node = document.createElement("option"); 
      var val = document.createTextNode(listPlayers[i]); 
      node.appendChild(val); 
      document.getElementById('list').appendChild(node); 
      counter++;
    }
  }
}

/**
 * creates an element of the players chosen from search bar
 */
async function selectPlayer() {
  const players = await getPlayers();
  const playerInfo = new Map(Object.entries(players));
  input = getInput();
  document.getElementById('listPlayers').innerHTML = '';
  var player = document.getElementById('listPlayers');
  var liElement = document.createElement('li');
  liElement.innerText =  input;
  var seasonsList = document.createElement('select');
  const addPlayerButton = document.createElement('input');
  addPlayerButton.type = 'button';
  addPlayerButton.className = 'btn btn-primary';
  addPlayerButton.value = 'Add Player';
  const deletePlayerButton = document.createElement('input');
  deletePlayerButton.type = 'button';
  deletePlayerButton.className = 'btn btn-primary';
  deletePlayerButton.value = 'Remove Player';
  const position = document.createElement('select');

  //button adds the selected player to the chart
  addPlayerButton.addEventListener('click',() => {
    if (selectedPlayers.length < 5) {
      var player = createplayer(input, seasonsList.value, position.id)
      createPlayernode(input, playerInfo.get(input).player_id, player.id, position.value);
      selectedPlayers.push(player);
      console.log(player.id);
      drawChart();
    } else {
        alert('You can only select 5 players');
    }
  });

  //removes liElement for the player selected
  deletePlayerButton.addEventListener('click',() => {
    liElement.remove();
  });

  //adds seasons the player played to seasonsList
  for ( j = 0; j < playerInfo.get(input).seasonsPlayed.length; j++) {
    var option = document.createElement("option");
    var value = document.createTextNode(playerInfo.get(input).seasonsPlayed[j]);
    option.appendChild(value);
    seasonsList.appendChild(option);
  }

  //creates the position options list
  for (i = 0; i < playerInfo.get(input).positionsPlayed.length; i++) {
    var option1 = document.createElement("option");
    var option2 = document.createElement("option");
    var pos = playerInfo.get(input).positionsPlayed[i];
    if (pos == 'G') {
      option1.innerText = 'P' + pos;
      option2.innerText = 'S' + pos;
      position.appendChild(option1);
      position.appendChild(option2);
      position.id = 'G';
    } else if (pos == 'F') {
      option1.innerText = 'S' + pos;
      option2.innerText = 'P' + pos;
      position.appendChild(option1);
      position.appendChild(option2);
      position.id = 'F';
    } else {
      option1.innerText = pos;
      position.appendChild(option1);
      position.id = 'C';
    }
  }

  liElement.appendChild(seasonsList);
  liElement.appendChild(position);
  liElement.appendChild(addPlayerButton);
  liElement.appendChild(deletePlayerButton);
  player.appendChild(liElement);
}

/**
 * creates player node that is displayed on the page.
 * @param {name of the current player} name 
 * @param {id for image to be shown} imageId 
 * @param {id of the current player} playerid 
 * @param {position selected for the player} pos 
 */
function createPlayernode(name, imageId, playerid, position) {
  var container  = document.getElementById('' + position + '-container');
  var player = document.createElement('li');
  player.innerHTML = '<center>' + name + '</center>';
  var url = "/images/cropped/" + imageId + ".jpg"
  var img = document.createElement('img');
  img.height = "60";
  player.appendChild(img);
  var deleteButton = document.createElement('input');
  deleteButton.type = 'button';
  deleteButton.className = 'btn btn-primary';
  deleteButton.value = 'remove from team';

  //removes player from chart
  deleteButton.addEventListener('click',() => {
    player.remove();
    size = selectedPlayers.length;
    for (i = 0; i < size ; i++) {
      if (selectedPlayers[i].id == playerid) {
        selectedPlayers[i].id = selectedPlayers[size-1].id;
        selectedPlayers.pop();
      }
    }
    drawChart();
  });
  player.appendChild(deleteButton);
  img.src = url;
  container.appendChild(player);
}

//draws a chart of players selected by the user
function drawChart() {
  fetch('/playerInfo').then(response => response.json()).then((team) => {
    const players = new Map(Object.entries(team));
    var data = new google.visualization.DataTable();
    var counter = 1;
    //creates a data table of the selected players and their stats
    for (i = 0; i < selectedPlayers.length; i++) {
      if ( i == 0) {
        data.addColumn('string', 'Stats');
        data.addRows(5);
        data.setCell(0, 0, 'PPG');
        data.setCell(1, 0, 'AST');
        data.setCell(2, 0, 'REB');
        data.setCell(3, 0, 'STL');
        data.setCell(4, 0, 'BLK');
      }
      if (players.has(selectedPlayers[i].id)) {
        data.addColumn('number', players.get(selectedPlayers[i].id).name);
        data.setCell(0, counter, players.get(selectedPlayers[i].id).points);
        data.setCell(1, counter, players.get(selectedPlayers[i].id).assists);
        data.setCell(2, counter, players.get(selectedPlayers[i].id).rebounds);
        data.setCell(3, counter, players.get(selectedPlayers[i].id).steals);
        data.setCell(4, counter, players.get(selectedPlayers[i].id).blocks);
        counter++;
      }
    }

    //the style of the chart created
    var options = {
      colors:['blue'],
      width: 600,
      height: 400,
      legend: { position: 'top', maxLines: 3 },
      bar: { groupWidth: '75%' },
      isStacked: true,
    };

    //creates a chart based on the data table and options
    var chart = new google.charts.Bar(document.getElementById('chart-container'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
  });
}

/**
 * calls selectPlayer() when the searchQuery matches on of elements in the data list
 */
function onInput() {
  var val = document.getElementById('searchQuery').value;
  var options = document.getElementById('list').childNodes;
  for (var i = 0; i < options.length; i++) {
    if (options[i].value === val) {
      selectPlayer();
    }
  }
}

/**
 * sends created team to calendar page
 */
function createTeam() {
  if (selectedPlayers.length == 5) {
    var team = document.getElementById('team').value;
    var year = document.getElementById('year').value;
    var queryString = "?player1=" + selectedPlayers[0].id + selectedPlayers[0].position
                    + "&player2=" + selectedPlayers[1].id + selectedPlayers[1].position 
                    + "&player3=" + selectedPlayers[2].id + selectedPlayers[2].position 
                    + "&player4=" + selectedPlayers[3].id + selectedPlayers[3].position
                    + "&player5=" + selectedPlayers[4].id + selectedPlayers[4].position 
                    + "&team=" + team + "&year=" + year;
    window.location.href = "scheduler/home-away/calendar.html" + queryString;
  } else {
    alert('You need 5 players to create a team');
  }
}

/**
 * adds 5 players to the team
 */
function quickTeam() {
  var derrick = createplayer('Derrick Rose', 2008, 'G');
  var klay = createplayer('Klay Thompson', 2011, 'G');
  var kevin = createplayer('Kevin Durant', 2018, 'F');
  var tim = createplayer('Tim Duncan', 2015, 'F');
  var joel = createplayer('Joel Embiid', 2016, 'C');
  selectedPlayers.push(derrick);
  selectedPlayers.push(klay);
  selectedPlayers.push(kevin);
  selectedPlayers.push(tim);
  selectedPlayers.push(joel);
  createPlayernode(derrick.name, 201565, derrick.id, 'PG');
  createPlayernode(klay.name, 202691, klay.id, 'SG');
  createPlayernode(kevin.name, 201142, kevin.id, 'SF');
  createPlayernode(tim.name, 1495, tim.id, 'PF');
  createPlayernode(joel.name, 203954, joel.id, 'C');
  drawChart();
}

/**
 * creates player object from params
 * @param {name of player} player 
 * @param {season of player} year 
 * @param {position of player} pos 
 * @return returns player object
 */
function createplayer(player, year, pos)  {
  player = {
    name: player,
    position: pos,
    id: player + year,
  }
  return player;
}

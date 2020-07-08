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


function drawChart(){
  fetch('/playerInfo').then(response => response.json()).then((team) => {
    const players = Object.values(team);
    var data = new google.visualization.DataTable();
    for(i=0;i < players.length;i++){
      if(i==0){
        data.addColumn('string','Stats');
        data.addRows(3);
        data.setCell(0,0,'PPG');
        data.setCell(1,0,'REB');
        data.setCell(2,0,'STL');
      }
      data.addColumn('number',players[i].name);
      data.setCell(0,i+1,players[i].points);
      data.setCell(1,i+1,players[i].rebounds);
      data.setCell(2,i+1,players[i].steals);
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


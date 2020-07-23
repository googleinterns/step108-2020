google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart);

function searchFunction() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('searchQuery');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
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
  var data = google.visualization.arrayToDataTable([
    ['Player','Anthony Davis', 'LeBron James', 'Kentavious Caldwell-Pope',
     'Avery Bradley', 'Dwight Howard', { role: 'annotation' } ],
    ['PPG', 26.7, 25.7, 9.5, 8.6, 7.5,''],
    ['REB', 16, 22, 23, 30, 16,  ''],
    ['STL', 28, 19, 29, 30, 12,  '']
  ]);

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
}

// AUTOCOMPLETE FOR NAMES
$( async function() {
    await loadData();
    var availableNames = jsondict["raw_player_names"]["names"];
    $( ".playername-input" ).autocomplete({
      source: availableNames
    });
  } );

// DROPDOWN MENU CODCHANGEE
$( document ).ready(function() {
    $('.dropdown').each(function (key, dropdown) {
        var $dropdown = $(dropdown);
        $dropdown.on('click', ".dropdown-item", function () {
            $dropdown.find('button').text($(this).text()).append(' <span class="caret"></span>').prop("value", $(this).text());
        });
    });
});
$(document).ready(function() {
  music.playback_changed.connect(function(song, state) {
    $('#playback-state').text(song.title);
  });

  $('#cpu-usage').text(system.cpu.usage);

  desktop.launchers.forEach(function(launcher) {
    $('<div />', {text: launcher.name}).appendTo('body');
  });
});
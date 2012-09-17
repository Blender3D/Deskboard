less.watch();

var textual_time = function(date) {
	var hours = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE2', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN2', 'ELEVEN', 'TWELVE', 'ASD'];
	var text = ['IT', 'IS'];
	var time = typeof date === 'undefined' ? new Date() : date;
	var minutes = time.getMinutes();
	var hour = time.getHours() % 12;

	var distance = minutes > 30 ? 60 - minutes : minutes;

	if ((2.5 < distance) && (distance <= 7.5)) {
		text.push('FIVE1');
	} else if ((7.5 < distance) && (distance <= 12.5)) {
		text.push('TEN');
	} else if ((12.5 < distance) && (distance <= 17.5)) {
		text.push('QUARTER');
	} else if ((17.5 < distance) && (distance <= 22.5)) {
		text.push('TWENTY');
	} else if ((22.5 < distance) && (distance <= 27.5)) {
		text.push('TWENTY');
		text.push('FIVE1');
	} else if ((27.5 < distance) && (distance <= 30)) {
		text.push('HALF');
		text.push(hours[hour]);

		return text;
	}

	if (distance <= 2.5) {
		text.push(hours[(hour + 11) % 12]);
		text.push('OCLOCK');
	} else if (minutes <= 30) {
		text.push('PAST');
		text.push(hours[(hour + 11) % 12]);
	} else {
		text.push('TO');
		text.push(hours[hour]);
	}

	return text;
};

var random_date = function(start, end) {
	start = typeof start === 'undefined' ? new Date(2012, 0, 1) : start;
	end = typeof end === 'undefined' ? new Date(2012, 0, 2) : end;

  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()))
}

var is_numeric = function(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

var print_clock = function() {
	var $clock = $('<div />', {'class': 'clock'});
	var clock = [
		['IT', 'L', 'IS', 'BFAMPM'],
		['AC', 'QUARTER', 'DC'],
		['TWENTY', 'X', 'FIVE1'],
		['HALF', 'B', 'TEN', 'F', 'TO'],
		['PAST', 'ERU', 'NINE'],
		['ONE', 'SIX', 'THREE'],
		['FOUR', 'FIVE2', 'TWO'],
		['EIGHT', 'ELEVEN'],
		['SEVEN', 'TWELVE'],
		['TEN2', 'SE', 'OCLOCK']
	];

	for (var i in clock) {
		var row = clock[i];
		var $row = $('<div />', {'class': 'row'}).appendTo($clock);

		for (var j in row) {
			var word = row[j];
			var $word = $('<span />', {'class': 'word', 'id': 'clock-' + word.toLowerCase()}).appendTo($row);
			var $letters = word.split('').map(function(letter) {
				var $letter = $('<span />', {'class': 'letter', 'text': letter});

				if (is_numeric(letter)) {
					$letter.hide();
				}

				return $letter;
			});

			$letters.forEach(function($letter) {
				$letter.appendTo($word);
			});
		}
	}

	return $clock;
}

var display_time = function(date) {
	var time = textual_time(date);

	$('.word').removeClass('highlighted');

	for (var i in time) {
		var word = time[i].toLowerCase();

		$('#clock-' + word).addClass('highlighted');
	}
}

$(document).ready(function() {
	var $clock_box = $('<li />', {'class': 'box'}).appendTo('#grid');

  $clock_box.attr('data-row', 1);
  $clock_box.attr('data-col', 2);
  $clock_box.attr('data-sizex', 4);
  $clock_box.attr('data-sizey', 4);
  var $clock = print_clock().appendTo($clock_box);

  $('#grid').gridster({
  	widget_selector: '.box',
		widget_margins: [10, 10],
		widget_base_dimensions: [100, 100],
    min_cols: 6
	});

  (timer = function() {
  	display_time(random_date());
  })();

  setInterval(timer, 3000);
});
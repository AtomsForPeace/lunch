function add_restaurant(restaurant) {
	name = restaurant[0]
	vote = restaurant[1]
	$('.left').append(
		'<div class="restaurant row border-0" id=' + name + '>' + name + '</div>'
	)
	$('.right').append(
			'<div class="row border-0">' + vote + '</div>'
	)
}

$.ajax({
	url: '/restaurants',
	success: function(data) {
		data = $.parseJSON(data);
		data['message'].map(r => add_restaurant(r))
		$('.restaurant').each(function(index) {
			$(this).click(function() {
				ws.send(JSON.stringify(
					{"message": $(this).text()}));
			})
		})
	},
	error: function() {
		console.log('ERROR!')
	}
});

// Websocket logic
var ws = new WebSocket(
	'ws://' + document.domain + ':' + location.port + '/update')

window.setInterval(function() {
	data = JSON.stringify({'message': 'online'})
	ws.send(data);
}, 1000);

ws.onmessage = function(event) {
	if (event.data == '406') {
		alert('Du darfst nur einmal pro Option waehlen!')
		return
	}
	data = event.data;
	rest = $('#' + data)
	index = $('.name').children().index(rest)
	old_value = parseInt($('.vote').children()[index].textContent)
	$('.vote').children()[index].textContent = old_value + 1
}

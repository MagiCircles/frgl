
function setupCards() {
    $('.card').unbind('click');
    $('.card').click(function(e) {
	var card = $(this);
	if (card.attr('href').match('^/addcard') === null) {
	    e.preventDefault();
	    $.get('/ajax' + card.attr('href'), function(data) {
		freeModal(card.find('.title').text(), data, 0);
		reloadDisqus();
	    });
	    return false;
	}
    });
}

$(document).ready(function() {
    setupCards();
    pagination('/ajax/cards/', setupCards);
});


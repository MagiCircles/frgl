
function setupCards() {
    // Show card details modal
    $('.card').unbind('click');
    $('.card').click(function(e) {
	var card = $(this);
	if (card.attr('href').match('^/addcard') === null) {
	    e.preventDefault();
	    showCardModal(gettext('About'), card);
	    return false;
	}
    });
    handleClickAddCardToCollection();
}

$(document).ready(function() {
    setupCards();
    pagination('/ajax/cards/', '', setupCards);
});

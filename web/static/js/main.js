
function freeModal(title, body, buttons) {
    $('#freeModal .modal-header h4').html(title);
    $('#freeModal .modal-body').html(body);
    $('#freeModal .modal-footer').html('<button type="button" class="btn btn-main" data-dismiss="modal">OK</button>');
    if (buttons === 0) {
	$('#freeModal .modal-footer').hide();
    } else if (typeof buttons != 'undefined') {
	$('#freeModal .modal-footer').html(buttons);
	$('#freeModal .modal-footer').show();
    }
    $('#freeModal').modal('show');
}

function load_more_function(nextPageUrl, newPageCallback) {
    var button = $("#load_more");
    button.html('<div class="loader">Loading...</div>');
    var next_page = button.attr('data-next-page');
    $.get(nextPageUrl + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page, function(data) {
	button.replaceWith(data);
	pagination(nextPageUrl, newPageCallback);
	newPageCallback();
    });
}

function pagination(nextPageUrl, newPageCallback) {
    var button = $("#load_more");
    $(window).scroll(
	function () {
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		load_more_function(nextPageUrl, newPageCallback);
	    }
	});
}

function reloadDisqus() {
    window.DISQUSWIDGETS = undefined;
    $.getScript("http://schoolidol.disqus.com/count.js");
}

$("#togglebutton").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

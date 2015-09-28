
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

function formloaders() {
    $('button[data-form-loader=true]').click(function(e) {
	$(this).html('<i class="flaticon-loading"></i>');
	$(this).unbind('click');
	$(this).click(function(e) {
	    e.preventDefault();
	    return false;
	});
    });
}

function load_more_function(nextPageUrl, newPageParameters, newPageCallback, onClick) {
    var button = $("#load_more");
    button.html('<div class="loader">Loading...</div>');
    var next_page = button.attr('data-next-page');
    $.get(nextPageUrl + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page + newPageParameters, function(data) {
	button.replaceWith(data);
	if (onClick) {
	    paginationOnClick(onClick, nextPageUrl, newPageParameters, newPageCallback);
	} else {
	    pagination(nextPageUrl, newPageParameters, newPageCallback);
	}
	if (newPageCallback) {
	    newPageCallback();
	}
    });
}

function pagination(nextPageUrl, newPageParameters, newPageCallback) {
    var button = $("#load_more");
    $(window).scroll(
	function () {
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		load_more_function(nextPageUrl, newPageParameters, newPageCallback, false);
	    }
	});
}

function paginationOnClick(buttonId, nextPageUrl, newPageParameters, newPageCallback) {
    var button = $('#' + buttonId);
    button.unbind('click');
    button.click(function(e) {
	e.preventDefault();
	load_more_function(nextPageUrl, newPageParameters, newPageCallback, buttonId);
	return false;
    });
}

function reloadDisqus() {
    window.DISQUSWIDGETS = undefined;
    $.getScript("http://schoolidol.disqus.com/count.js");
}

function hidePopovers() {
    $('[data-manual-popover=true]').popover('hide');
    $('[data-toggle=popover]').popover('hide');
    $('#you').popover('hide');
}

function showCardModal(modaltitle, cardlink) {
    $.get('/ajax' + cardlink.attr('href'), function(data) {
	freeModal(modaltitle, data, 0);
	reloadDisqus();
    });
}

function genericAjaxError(xhr, ajaxOptions, thrownError) {
    alert(xhr.responseText);
}

function handleClickAddCardToCollection() {
    $('.addcardform').unbind('submit');
    $('.addcardform').submit(function(e) {
	e.preventDefault();
	var form = $(this);
	if (typeof form.attr('data-submitting') == 'undefined') {
	    form.attr('data-submitting', true);
	    form.ajaxSubmit({
		success: function(data) {
		    $('#you').popover({
			content: gettext('The card has been added to your collection.'),
			placement: 'bottom',
			trigger: 'manual',
			container: $('nav.navbar'),
		    });
		    $('#you').popover('show');
		    form.removeAttr('data-submitting');
		},
		error: function(x, a, t) {
		    form.removeAttr('data-submitting');
		    genericAjaxError(x, a, t);
		},
	    });
	}
	return false;
    });
}

function updateActivities() {
    $('a[href=#likecount]').unbind('click');
    $('a[href=#likecount]').click(function(e) {
	e.preventDefault();
	var socialbar = $(this).closest('.socialbar');
	$(this).popover({
	    content: socialbar.find('.likers-wrapper').html(),
	    placement: 'right',
	    trigger: 'manual',
	    container: socialbar,
	    html: true,
	});
	$(this).popover('show');
	return false;
    });
    $('.likeactivity').unbind('submit');
    $('.likeactivity').submit(function(e) {
	e.preventDefault();
	$(this).ajaxSubmit({
	    context: this,
	    success: function(data) {
		if (data == 'liked') {
		    $(this).find('input[type=hidden]').prop('name', 'unlike');
		} else {
		    $(this).find('input[type=hidden]').prop('name', 'like');
		}
		var value = $(this).find('button[type=submit]').html();
		$(this).find('button[type=submit]').html($(this).find('button[type=submit]').attr('data-reverse'));
		$(this).find('button[type=submit]').attr('data-reverse', value);
	    },
	    error: genericAjaxError,
	});
	return false;
    });
}

$(document).ready(function() {

    $("#togglebutton").click(function(e) {
	e.preventDefault();
	$("#wrapper").toggleClass("toggled");
    });

    formloaders();

    // Dismiss popovers on click outside
    $('body').on('click', function (e) {
	if ($(e.target).data('toggle') !== 'popover'
	    && $(e.target).parents('.popover.in').length === 0
	    && $(e.target).data('manual-popover') != true) {
	    hidePopovers();
	}
    });

    // Index activities
    if ($('#activities').length > 0) {
	$.get('/ajax/activities/?avatar_size=2&feed', function(data) {
	    $('#activities').html(data);
	    updateActivities();
	    pagination('/ajax/activities/', '&avatar_size=2&feed', updateActivities);
	});
    }
    if ($('#hotactivities').length > 0) {
	$.get('/ajax/activities/?avatar_size=2', function(data) {
	    $('#hotactivities').html(data);
	    updateActivities();
	    pagination('/ajax/activities/', '&avatar_size=2', updateActivities);
	});
    }
});


function cardsDetails() {
    $('.ownedcard-wrapper').unbind('click');
    $('.ownedcard-wrapper').click(function(e) {
	var ownedcard = $(this);
	ownedcard.popover({
	    content: function() {
		return $(this).find('.form-wrapper').html();
	    },
	    placement: 'bottom',
	    trigger: 'manual',
	    html: true,
	    placement: 'top',
	}).parent().delegate('form', 'submit', function(e) {
	    e.preventDefault();
	    $(this).ajaxSubmit({
	    	success: function(data) {
	    	    ownedcard.popover('hide');
	    	    ownedcard.popover('destroy');
	    	    ownedcard.parent().remove();
	    	},
	    	error: genericAjaxError,
	    });
	    return false;
	}).delegate('a', 'click', function(e) {
	    e.preventDefault;
	    showCardModal(gettext('About'), $(this));
	    return false;
	});
	ownedcard.popover('show');
    });
}

function handleTabs() {

    var loadingHTML = '<br><div class="alert alert-warning">Loading...</div>';

    $('ul.nav-tabs li a').click(function (e) {
	e.preventDefault();
	$(this).tab('show');
    });
    $('ul.nav-tabs li a').on('show.bs.tab', function (e) {
	var id = $(e.target).attr('href');
	var tab = $(id);
	var account = tab.closest('.panel').prop('id');
	if (tab.text() == '') {
	    if (id.indexOf('#accountTabActivities') == 0) {
		tab.html(loadingHTML);
		$.get('/ajax/activities/?avatar_size=1&account=' + account, function(data) {
		    tab.html(data);
		    paginationOnClick('activities' + account, '/ajax/activities/', '&avatar_size=1&account=' + account);
		});
	    } else if (id.indexOf('#accountTabEvents') == 0) {
		tab.html(loadingHTML);
		$.get('/ajax/eventparticipations/' + account + '/', function(data) {
		    tab.html(data);
		});
	    }
	}
    });
}

function profileDescriptionMarkdown() {
    $('.topprofile .description').html(Autolinker.link($('.topprofile .description').html(), { newWindow: true, stripPrefix: true } ));
}

function handlefollow() {
    $('#follow').submit(function(e) {
	e.preventDefault();
	$(this).ajaxSubmit({
	    success: function(data) {
		if (data == 'followed') {
		    $('#follow input[type="hidden"]').prop('name', 'unfollow');
		} else {
		    $('#follow input[type="hidden"]').prop('name', 'follow');
		}
		var value = $('#follow input[type="submit"]').prop('value');
		$('#follow input[type="submit"]').prop('value', $('#follow input[type="submit"]').attr('data-reverse'));
		$('#follow input[type="submit"]').attr('data-reverse', value);
	    },
	    error: genericAjaxError,
	});
    });

    $('a[href="#followers"]').click(function(e) {
	e.preventDefault();
	var username = $('#username').text();
	var text = $(this).closest('tr').find('th').text();
	$.get('/ajax/followers/' +  username + '/', function(data) {
	    freeModal(username + ': ' + text, data);
	});
    });
    $('a[href="#following"]').click(function(e) {
	e.preventDefault();
	var username = $('#username').text();
	var text = $(this).closest('tr').find('th').text();
	$.get('/ajax/following/' +  username + '/', function(data) {
	    freeModal(username + ': ' + text, data);
	});
    });
}

$(document).ready(function() {
    cardsDetails();
    handlefollow();
    handleTabs();
    profileDescriptionMarkdown();
});

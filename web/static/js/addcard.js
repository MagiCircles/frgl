
function toggleSelectedRarityFields() {
    var rarity = 'C'
    if ($('#id_rarity').length > 0) {
	rarity = $('#id_rarity').val();
    } else {
	var match = $('#id_parent option:selected').text().match(/\[([^)]+)\]/);
	if (match) {
	    rarity = match[1];
	}
    }
    if (rarity == 'C') {
	$('#id_skill').closest('.form-group').hide();
	$('#id_skill_value').closest('.form-group').hide();
	$('#id_trigger_value').closest('.form-group').hide();
	$('#id_trigger_chance').closest('.form-group').hide();
	$('#id_maximum_performance_ability').closest('.form-group').hide();
    } else if (rarity == 'R' || rarity == 'SR') {
	$('#id_skill').closest('.form-group').show();
	$('#id_skill_value').closest('.form-group').show();
	$('#id_trigger_value').closest('.form-group').show();
	$('#id_trigger_chance').closest('.form-group').show();
	$('#id_maximum_performance_ability').closest('.form-group').hide();
    } else {
	$('#id_skill').closest('.form-group').show();
	$('#id_skill_value').closest('.form-group').show();
	$('#id_trigger_value').closest('.form-group').show();
	$('#id_trigger_chance').closest('.form-group').show();
	$('#id_maximum_performance_ability').closest('.form-group').show();
    }
}

function toggleRewardNameValue() {
    if ($('#id_reward_type').length > 0) {
	var reward_type = $('#id_reward_type').val();
	if (reward_type == 'profile') {
	    $('#id_add_value').closest('.form-group').hide();
	    $('#id_name').closest('.form-group').show();
	} else {
	    $('#id_add_value').closest('.form-group').show();
	    $('#id_name').closest('.form-group').hide();
	}
    }
}

$(document).ready(function(e) {
    toggleSelectedRarityFields();
    toggleRewardNameValue();
    $('#id_reward_type').change(function(e) {
	toggleRewardNameValue();
    });
    $('#id_reward_type + .cuteform .cuteform-elt').click(function() {
	toggleRewardNameValue();
    });
    $('#id_rarity').change(function(e) {
	toggleSelectedRarityFields();
    });
    $('#id_rarity + .cuteform .cuteform-elt').click(function() {
	toggleSelectedRarityFields();
    });
    $('#id_parent').change(function(e) {
	toggleSelectedRarityFields();
    });
});

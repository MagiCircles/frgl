
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

$(document).ready(function(e) {
    toggleSelectedRarityFields();
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

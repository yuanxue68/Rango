$(document).ready(function() {
	$('#suggestion').keyup(function(){
			console.log('in ajax');
	        var query;
	        query = $(this).val();
	        $.get('/rango/suggest_category/', {suggestion: query}, function(data){
	         $('#cats').html(data);
	        });
	});
});
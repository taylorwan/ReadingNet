$( function() {

	init();

});

function init() {
	console.log("in error.js");
}

function error( msg ) {
	var $msgBox =  $( 'html #errorMsg' )
	$msgBox.text( msg );
	$msgBox.fadeIn();
	window.setTimeout( function() {
		$msgBox.fadeOut();
	}, 3000 );
}

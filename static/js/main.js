$( function() {

	init();

});

function init() {
	console.log("main.js loaded");
}

function message( msg ) {
	// finding our messagebox
	var $msgBox =  $( 'html #message' );

	// set text
	$msgBox.text( msg );

	// fade it in, and then out
	$msgBox.fadeIn();
	window.setTimeout( function() {
		$msgBox.fadeOut();
	}, 3000 );
}

function error( msg ) {
	message( "Something seems off. " + msg + ". Try again!" );
}
function success( msg ) {
	message( msg );
}
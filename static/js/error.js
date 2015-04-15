$( function() {

	init();

});

function init() {
	console.log("in error.js");
}

function error( msg ) {
	// finding our messagebox
	var $msgBox =  $( 'html #errorMsg' );

	// set text
	$msgBox.text( msg );

	// fade it in, and then out
	$msgBox.fadeIn();
	window.setTimeout( function() {
		$msgBox.fadeOut();
	}, 3000 );
}

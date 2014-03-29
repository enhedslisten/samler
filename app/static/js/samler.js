$(document).ready(function() {
	
	/**
	* Masonry plugin - helps presentation of elements
	*/
	var container = document.querySelector('#posts');
    var msnry;
    // initialize Masonry after all images have loaded
    imagesLoaded( container, function() {
      msnry = new Masonry( container,  {
        // options
        columnWidth: 260,
        gutter: 15,
        itemSelector: '.post'
      } );
    });


	/**
	* Create fancybox popups for images.
	* Different widths for the different services.  
	**/
    

	$('a.iframe.instagram').fancybox({
		'width' : 600,
		'height' : 1200
	});	

	$('a.iframe.twitter').fancybox({
		'width' : 400,
		'height' : 1200
	});

	$('a.hidePost').click(function(){
		return confirm("Er du sikker du vil skjule denne post?");
	});

});
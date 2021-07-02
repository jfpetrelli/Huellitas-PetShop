(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

var band = true
function devolver(){
	if(band){
		document.getElementById("sidebar").style.width = "100px";
    	document.getElementById("content").style.marginLeft = "250px";
		band = false
	}else{
		document.getElementById("sidebar").style.width = "0";
    	document.getElementById("content").style.marginLeft = "5px";
		band = true
	}
}

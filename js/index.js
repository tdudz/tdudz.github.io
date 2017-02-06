// Parallax Scrolling
$(document).ready(function(){
	$window = $(window);
    $('section[data-type="background"]').each(function(){
        var $bgobj = $(this); // assigning the object
        
        $(window).scroll(function() {
            var yPos = -($window.scrollTop() / $bgobj.data('speed')); 
             
            // Put together our final background position
            var coords = '50% ' + yPos + 'px';
            // Move the background
            $bgobj.css({ backgroundPosition: coords });

        }); 
    });    
    // Fading of logo
    var fadeStart=000 // 100px scroll or less will equiv to 1 opacity
        ,fadeUntil=300 // 200px scroll or more will equiv to 0 opacity
        ,fading = $('#article-name')
        ,fading2 = $('#article-triangles')
    ;

    $(window).bind('scroll', function(){
        var offset = $(document).scrollTop()
            ,opacity=0
        ;
        if( offset<=fadeStart ){
            opacity=1;
        }else if( offset<=fadeUntil ){
            opacity=1-offset/fadeUntil;
        }
        fading.css('opacity',opacity);
        fading2.css('opacity',opacity);
    });

    /* Every time the window is scrolled ... */
    $(window).scroll( function(){
        $('#p2_head2').each( function(i){
            var bottom_of_object = $(this).position().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop();// + $(window).height();
            /* If the object is completely visible in the window, fade it in */
            if( bottom_of_window > bottom_of_object && bottom_of_object > bottom_of_window - $(window).height()){
                $(this).animate({'opacity':'1'},1500);
            }
        }); 
        $('#p2_head3').each( function(i){
            var bottom_of_object = $(this).position().top + $(this).outerHeight()+150;
            var bottom_of_window = $(window).scrollTop();// + $(window).height();
            /* If the object is completely visible in the window, fade it in */
            if( bottom_of_window > bottom_of_object && bottom_of_object > bottom_of_window - $(window).height()){
                $(this).animate({'opacity':'1'},1500);
            }
        }); 
        /* Check the location of each desired element */
        $('.row').each( function(i){

            var bottom_of_object = $(this).position().top + $(this).outerHeight() + 100;
            var bottom_of_window = $(window).scrollTop();// + $(window).height();


            /* If the object is completely visible in the window, fade it in */
            if( bottom_of_window > bottom_of_object && bottom_of_object > bottom_of_window - $(window).height()){
                $(this).animate({'opacity':'1'},1500);
            }
            // if(bottom_of_object < bottom_of_window){
            //     $(this).animate({'opacity':'0'},1000);
            // }
            // if(bottom_of_object < bottom_of_window - $(window).height()){
            //     $(this).animate({'opacity':'0'},1000);
            // }
        }); 

    });
});


// Create HTML5 elements for IE
  
document.createElement("article");
document.createElement("section");
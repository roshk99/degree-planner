// List with handle
Sortable.create(classesList, {
    sort: true,
    group: {
        name: 'class',
        put: ['fall-semester', 'spring-semester', 'class']
    },
    animation: 150,
    handle: '.panel-heading',
    scroll: true
});

var sortable, recalculate_credits;
$('.semester-list').each(function() {
    sortable = new Sortable(this, {
        sort: true,
        group: {
            name: 'semester',
            put: ['class', 'semester']
        },
        animation: 150,
        handle: '.panel-heading',
        scroll: true,

         // Element is dropped into the list from another list
        onAdd: function (evt) {
            console.log(this);
        },

        // Element is removed from the list into another list
        onRemove: function (evt) {
            console.log(this);
        }
    });
});

$(function() {
   // navigation click actions
	$('.scroll-link').on('click', function(event){
		event.preventDefault();
		var sectionID = $(this).attr("data-id");
		scrollToID('#' + sectionID, 750);
	});

	// scroll to top action
	$('.scroll-top').on('click', function(event) {
		event.preventDefault();
		$('html, body').animate({scrollTop:0}, 'slow');
	});

	// mobile nav toggle
	$('#nav-toggle').on('click', function (event) {
		event.preventDefault();
		$('#main-nav').toggleClass("open");
	});

    //collapse all classes
    $('.panel-body').slideUp();
});

// scroll function
function scrollToID(id, speed){
    var offSet = 130;
    var targetOffset = $(id).offset().top - offSet;
    var mainNav = $('#main-nav');
    $('html,body').animate({scrollTop:targetOffset}, speed);
    if (mainNav.hasClass("open")) {
        mainNav.css("height", "1px").removeClass("in").addClass("collapse");
        mainNav.removeClass("open");
    }
}

// collapse expand class function
$(document).on('click', '.panel-heading span.clickable', function(e){
    var $this = $(this);
	if(!$this.hasClass('panel-collapsed')) {
		$this.parents('.panel').find('.panel-body').slideUp();
		$this.addClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
	} else {
		$this.parents('.panel').find('.panel-body').slideDown();
		$this.removeClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
	}
})
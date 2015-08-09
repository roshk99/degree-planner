// List with handle
Sortable.create(classesList, {
    sort: true,
    group: {
        name: 'class',
        put: ['semester', 'class']
    },
    filter: '.placeholder',
    animation: 150,
    handle: '.panel-heading',
    scroll: true,
    draggable: ".list-group-item"
});

var sortable, credits;
$('.semester-list').each(function() {
    sortable = Sortable.create(this, {
        sort: true,
        group: {
            name: 'semester',
            put: ['class', 'semester']
        },
        animation: 150,
        handle: '.panel-heading',
        filter: '.placeholder',
        scroll: true,
        draggable: '.list-group-item',

        onAdd: function(evt) {
            credits = 0;
            $(evt.to).children().each(function() {
                credits += parseFloat($(this).find('.badge').text());
            });
            $(evt.to).parent().find('.credits').text(credits);
        },

        onRemove: function(evt) {
            credits = 0;
            $(evt.from).children().each(function() {
                credits += parseFloat($(this).find('.badge').text());
            });
            $(evt.from).parent().find('.credits').text(credits);
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

    //Calculate all credits
    $('.semester-list').each(function() {
        credits = 0.0;
        $(this).children().each(function() {
            credits += parseFloat($(this).find('.badge').text());
        });
        $(this).parent().find('.credits').text(credits);
    });
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
});

$('#save-classes').on('click', function(e) {
    e.preventDefault();
    var semesters, number;
    semesters = {};
    $('.semester-list').each(function() {
        number = parseInt(this.id.match(/\d+/)[0]);
        semesters[number] = [];
        $(this).children().each( function() {
           semesters[number][semesters[number].length] = $(this).data('id');
        });
    });

    return $.ajax({
        url: '/plan',
        type: 'POST',
        data: {
            'data': JSON.stringify(semesters)
        },
        success: function(data) {
            window.location.reload();
            console.log(data);

        }
    });
});

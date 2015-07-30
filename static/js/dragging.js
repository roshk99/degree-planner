// List with handle
Sortable.create(classesList, {
    group: {
        name: 'class',
        put: ['semester']
    },
    animation: 150,
    handle: '.glyphicon-move',
    scroll: true,
    filter: '.placeholder'
});

var sortable, recalculate_credits;
$('.semester-list').each(function() {
    sortable = new Sortable(this, {
        group: {
            name: 'semester',
            put: ['class']
        },
        animation: 150,
        handle: '.glyphicon-move',
        scroll: true,
        filter: '.placeholder',

         // Element is dropped into the list from another list
        onAdd: function (evt) {
            recalculate_credits(this);
        },

        // Element is removed from the list into another list
        onRemove: function (evt) {
            recalculate_credits(this);
        }
    });
});

recalculate_credits = function(semester) {
    console.log
};
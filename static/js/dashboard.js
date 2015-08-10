$('#add-majors-button').on('click', function(e) {
    e.preventDefault();
    var major_id = $('#input-add-majors').val();
    if (major_id == null) {
        return alert('Did not select any major to add');
    }

    return $.ajax({
        url: '/dashboard/addmajor',
        type: 'POST',
        data: {
            'id': major_id
        },
        success: function(data) {
            window.location.reload();
            if (data == 'Already added!') {
                return alert('Already added!');
            }
            else {
                return alert('Success!');
            }
        }
    });
});

$('#clear-majors-button').on('click', function(e) {
    e.preventDefault();
    var confirm = window.confirm("Are you sure you want to delete all your majors and all the classes in your plan?");
    if (confirm) {
        return $.ajax({
            url: '/dashboard/clearmajors',
            type: 'GET',
            success: function() {
                window.location.reload();
            }
        });
    }
});

$('#delete-account-button').on('click', function(e) {
    e.preventDefault();
    var confirm = window.confirm("Are you sure you want to delete all your data on this site?");
    if (confirm) {
        return $.ajax({
            url: '/deleteaccount',
            type: 'GET',
            success: function() {
                window.location = '/';
            }
        });
    }
});
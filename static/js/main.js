$(function() {
   $('#login-button').on('click', function(e) {
      var field, fields, postData, field_names, i, len;
        e.preventDefault();
        field_names = ['Email', 'Password'];
        fields = [$('#input-login-email'), $('#input-login-password')];
        for (i = 0, len = fields.length; i < len; i++) {
            field = fields[i];
            if (field.val().trim() === "") {
                return alert('Missing: ' + field_names[i]);
            }
        }

        postData = {
            'email': fields[0].val().trim(),
            'password': fields[1].val().trim()
        };
        return $.ajax({
            url: '/login',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function(data) {
                if (data == 'Invalid Email/Password Combination') {
                    return alert('Invalid Email/Password Combination');
                }
                else {
                    window.location = '/dashboard';
                }
            }
        });
   });

    $('#register-button').on('click', function(e) {
      var field, fields, postData, field_names, i, len;
        e.preventDefault();
        field_names = ['First Name', 'Last Name', 'Email', 'Password', 'Confirm Password', 'University'];
        fields = [$('#input-register-first-name'), $('#input-register-last-name'), $('#input-register-email'),
            $('#input-register-password'), $('#input-register-confirm-password'), $('#input-register-university')];
        for (i = 0, len = fields.length; i < len; i++) {
            field = fields[i];
            if (field.val().trim() === "") {
                return alert('Missing: ' + field_names[i]);
            }
        }

        if (fields[3].val().trim() != fields[4].val().trim()) {
            return alert('Password and Password Confirmation must match');
        }

        postData = {
            'first_name': fields[0].val().trim(),
            'last_name': fields[1].val().trim(),
            'email': fields[2].val().trim(),
            'password': fields[3].val().trim(),
            'university': fields[5].val().trim()
        };
        return $.ajax({
            url: '/register',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function(data) {
                if (data == 'This email is already in use') {
                    return alert('This email is already in use');
                }
                else {
                    window.location = '/dashboard';
                }
            }
        });
   });
});


// Script that handles the sign up form
$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/home"
    },
    error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
  });

  e.preventDefault();
});

// Script that handles the login form
$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/home"
    },
    error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
  });

  e.preventDefault();
});

// Script that handles the create dictionary button
$("form[name=create_directory_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/create_directory",
    type: "GET",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.alert("Directory was created successfully\nUntil said directory will be deleted creation of another wont be possible")
    },
    error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
  });

  e.preventDefault();
});


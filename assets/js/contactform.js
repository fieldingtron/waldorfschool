/* eslint-disable no-undef */
$(function() {
  $("#contactus input,#contactus select,#contactus textarea").not("[type=submit]").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      console.log("error");

      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      console.log("submitting");
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var name = $("input#contact-name").val();
      var email = $("input#contact-email").val();
      var subject = $("input#contact-subject").val();
      var message = $("textarea#contact-message").val();
      var firstName = name; // For Success/Failure Message
      // Check for white space in name for Success/Fail message
      if (firstName.indexOf(" ") >= 0) {
        firstName = name.split(" ").slice(0, -1).join(" ");
      }
      $this = $("#sendMessageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "https://jumprock.co/mail/gonkertron",
        type: "POST",
        data: {
          name: name,
          subject: subject,
          email: email,
          message: message
        },
        cache: false,
        success: function() {
          // Success message
          $("#success").html("<div class='alert alert-success'>");
          $("#success > .alert-success").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $("#success > .alert-success")
            .append("<strong>Your message has been sent. </strong>");
          $("#success > .alert-success")
            .append("</div>");
          //clear all fields
          $("#contactForm").trigger("reset");
        },
        error: function() {
          // Fail message
          $("#success").html("<div class='alert alert-danger'>");
          $("#success > .alert-danger").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $("#success > .alert-danger").append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
          $("#success > .alert-danger").append("</div>");
          //clear all fields
          $("#contactForm").trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$("#name").focus(function() {
  $("#success").html("");
});


/* eslint-disable no-undef */
$(function() {
  $("#cmodal input,#cmodal select,#cmodal textarea").not("[type=submit]").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      console.log("error");

      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      console.log("submitting contact modal form");
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var name = $("#cmodal input#contact-name").val();
      var email = $("#cmodal input#contact-email").val();
      var phone = $("#cmodal input#contact-phone").val();
      var subject = $("#mretreatname").text();
      var dates =  $("#modalselect").val();
      var message = dates + "  " + $("#cmodal textarea#contact-message").val();
      console.log("subject = " + message);


      var firstName = name; // For Success/Failure Message
      // Check for white space in name for Success/Fail message
      if (firstName.indexOf(" ") >= 0) {
        firstName = name.split(" ").slice(0, -1).join(" ");
      }
      $this = $("#sendMessageButtonCM");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "https://jumprock.co/mail/gonkertron",
        type: "POST",
        data: {
          name: name,
          subject: subject,
          phone: phone,
          email: email,
          message: message
        },
        cache: false,
        success: function() {
          // Success message
          $("#successcm").html("<div class='alert alert-success'>");
          $("#successcm > .alert-success").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $("#successcm > .alert-success")
            .append("<strong>Your message has been sent. </strong>");
          $("#successcm > .alert-success")
            .append("</div>");
          //clear all fields
          $("#cmodalForm").trigger("reset");
        },
        error: function() {
          // Fail message
          $("#successcm").html("<div class='alert alert-danger'>");
          $("#successcm > .alert-danger").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $("#successcm > .alert-danger").append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
          $("#successcm > .alert-danger").append("</div>");
          //clear all fields
          $("#cmodalForm").trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$("#name").focus(function() {
  $("#successcm").html("");
});


$(document).ready(function() {
  $("#pageselect").change(function() {
    var selectedVal = $(this).children("option:selected").val();
    $("#modalselect").val(selectedVal);
    // alert("You have selected the country - " + selectedCountry);
  });
});

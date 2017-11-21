// DOM is ready
$(document).ready(function () {
  // Polling function
  var polling = function (task_id) {
    $.get('/result/' + task_id, function (data) {
      if (data.ready) {
        $('.modal-body').html('<p>From task ' + data.task_id +
                              ' we got: ' + data.result);
        $('.modal').modal('show');
      } else {
        setTimeout(function () {
          polling(task_id);
        }, 1000);
      }
    });
  };

  var click_count = 0;

  // Bind click event
  $('.pushme').click(function () {
    click_count += 1;

    // AJAX request
    $.get('/data?cc=' + click_count, function (data) {
      var row_html = 
          '<tr><td>' + data.count + '</td>' +
          '<td>' + data.squared + '</td></tr>';

      // Append our row
      $('.ourtable > tbody').append(row_html);

      // Run polling for task
      polling(data.task_id);
    });

    return false;
  });
});

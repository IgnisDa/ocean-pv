$("#id_username").change(function () {
    var form = $(this).closest("form");
    $.ajax({
        url: form.attr("data-validate-username-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.exists) {
                var fields = JSON.parse(data['usernames']);
                console.log(fields)
                var i;
                for (i = 0; i < fields.length; i++) {
                    $("#my_table tbody").prepend(
                        `<tr>
                    <td>${fields[i]['fields']["user"]}</td>
                    </tr>`
                    )
                }
            } else {
                alert("No such username exists")
            }
        }
    });

});
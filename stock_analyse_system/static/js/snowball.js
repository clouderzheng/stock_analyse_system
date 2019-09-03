$(function () {
    $('.datetimePicker').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        minuteStep: 1,
    });

});

function query_stock_position() {
    var begin_time = $("#begin_time").val();
    var end_time = $("#end_time").val();
    var token = check_token();

    $.ajax({
         url: "/snowball/get_position_combination",
            type: "post",
            data: {"begin_time": begin_time, "end_time": end_time,"token":token},
            success: function (res) {
                alert(res)
            },
            error: function () {
                alert("请联系管理人员")
            }
    })
}
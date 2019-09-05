$(function () {
    $('.datetimePicker').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        minuteStep: 1,
    });

});

var index = 0;
function query_stock_position() {
    var begin_time = $("#begin_time").val();
    var end_time = $("#end_time").val();
    var count = $("#count").val();
    var page = $("#page").val();
    var token = check_token();

    var mycars=new Array("active","success","warning","danger")

    if(index == 4){
        index = 0;
    }else {
        index++;
    }

    $.ajax({
         url: "/snowball/get_position_combination",
            type: "post",
            data: {"begin_time": begin_time, "end_time": end_time,"token":token,"count":count,"page":page},
            datatype : "json",
            success: function (res) {
                if(res.code = "0000"){
                    var stock_list = res.stock_list;
                    var html = "";
                    for (key in stock_list){
                        stock_info = stock_list[key];

                        var code = $("#"+stock_info.stock_code).text();
                        if(code != undefined && code != ""){
                            var count = $("#"+stock_info.stock_code+"_count").text();
                            $("#"+stock_info.stock_code+"_count").text(Number(count)+1);
                            continue;
                        }

                        html += "<tr class='"+mycars[index]+"'>";
                        html += "<td>"+stock_info.stock_name+"</td>";
                        html += "<td id='"+stock_info.stock_code+"'>"+stock_info.stock_code+"</td>";
                        html += "<td id='"+stock_info.stock_code+"_count'>"+stock_info.count+"</td>";
                        html += "</tr>";
                    }
                    $("#stock_info").append(html);
                }else{
                    alert("查询失败,请联系管理人员")
                }
            },
            error: function () {
                alert("请联系管理人员")
            }
    })
}
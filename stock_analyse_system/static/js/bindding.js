/*竞价查询方法*/
function bidding_query() {
    var token = check_token();
    var count = $("#count").val();
    var min_gain = $("#min_gain").val();
    var max_gain = $("#max_gain").val();
    $.ajax({
        url : "/snowball/get_bidding_info",
        type : "POST",
        data : {"token" : token,"count":count,"min_gain":min_gain,"max_gain":max_gain},
        success : function (res) {
            if(res.code == "0000"){
                var html = "";
                var result = res.result;
                for (key in result){
                    var stock_info = result[key];
                      html += "<tr >";
                        html += "<td>"+stock_info.name+"</td>";
                        html += "<td >"+stock_info.symbol+"</td>";
                        html += "<td >"+stock_info.current+"</td>";
                        html += "<td >"+stock_info.volume+"</td>";
                        html += "<td >"+stock_info.percent+"</td>";
                        html += "</tr>";
                }
                 $("#stock_info").append(html);
            }
        },
        error : function () {
            alert("查询竞价信息失败")
        }

    })
};
/*回调支撑选股方法*/
function call_back_query() {
    var token = check_token();
    var call_back_day = $("#call_back_day").val();
    var exclude_day = $("#exclude_day").val();
    var float_per = $("#float_per").val();
    $.ajax({
        url : "/snowball/get_call_back_support_stock",
        type : "POST",
        data : {"token" : token,"call_back_day":call_back_day,"exclude_day":exclude_day,"float_per":float_per},
        success : function (res) {
            if(res.code = "0000"){
                var html = "";
                var result = res.result;
                for (key in result){
                    var stock_info = result[key];
                      html += "<tr >";
                        html += "<td>"+stock_info.stock_name+"</td>";
                        html += "<td >"+stock_info.area_stock_code+"</td>";
                        html += "<td >"+stock_info.current_new_price+"</td>";
                        html += "<td >"+stock_info.current_low_price+"</td>";
                        html += "<td >"+stock_info.current_low_day+"</td>";
                        html += "<td >"+stock_info.last_high_price+"</td>";
                        html += "<td >"+stock_info.last_high_day+"</td>";
                        html += "<td >"+stock_info.percent+"</td>";
                        html += "</tr>";
                }
                 $("#stock_info").append(html);
            }
        },
        error : function () {
            alert("查询竞价信息失败")
        }

    })
}
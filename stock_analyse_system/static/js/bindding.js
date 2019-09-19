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
            if(res.code = "9999"){
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
}
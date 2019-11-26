/**
 * 查询策略信息
 */
var strategy_id = sessionStorage.getItem('strategy_id');

function query_strategy() {
    var token = check_token();
    $.ajax({
        url: "/analyse/query_strategy_info",
        type: "get",
        data: {"strategy_ids": strategy_id, "token": token},
        success: function (res) {
            if (res.code == '0000') {
                var data = res.data;
                $("#strategy_name").html(data[0].strategy);
                $("#strategy_desc").html(data[0].remark);
                var html = "";
                for (var index in data) {
                    param = data[index];
                    html += " <div class='form-group'>" +
                        "<span style='float: left;margin-top: 1%'>"+param.param_desc+"</span><input value='"+param.strategy_param+"' hidden/><input type='text'  style='width: 20%' readonly value='"+param.strategy_value+"' class='form-control'>" +
                        " </div>";
                }
                $("#strategy_params").append(html);

            }
        },
        error: function () {
            alert("出错了，请联系技术人员")
        }
    })
}

$(document).ready(function () {
    query_strategy();
})
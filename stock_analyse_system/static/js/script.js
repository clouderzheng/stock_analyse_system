// 设置tbody的html
function setTbody(arr) {
    var html = '';
    for (var i = 0; i < arr.length; i++) {
        var item = arr[i];
        html += '<tr>'
            + '<td>' + item.stock_code + '</td>'
            + '<td>' + item.stock_name + '</td>'
            + '<td>' + item.create_date + '</td>'
            + '<td>' + item.current_rate + '</td>'
            + '<td>' + item.current_price + '</td>';
        detail_info = item.track_info;
        var day = 0;
        var choose_price = item.current_price;
        for (var index in detail_info) {
            track_price = detail_info[index].close_price
            if (track_price > choose_price) {
                html += '<td style="color: red">' + detail_info[index].close_price + '</td>';
            } else {
                html += '<td style="color: green">' + detail_info[index].close_price + '</td>';
            }
            day++;
        }
        while (day < 5) {
            html += '<td>--</td>';
            day++;
        }
        html += '</tr>';
    }
    $('.tbody').html(html);
}


// 初始化分页
$('.box2').MyPaging({
    size: 10,
    total: 0,
    current: 1,
    prevHtml: '上一页',
    nextHtml: '下一页',
    layout: 'total, totalPage, prev, pager, next, jumper',
    jump: function () {
        var _this = this;
        setTimeout(function () {
            // 模拟ajax获取数据
            var token = check_token();
            $.ajax({
                url: "/analyse/query",
                type: "get",
                data: {"page": _this.current, "limit": _this.size, "strategy_ids": strategy_id, "token": token},
                success: function (res) {
                    if (res.code == '0000') {
                        setTbody(res.data);
                        _this.setTotal(res.count);
                    } else {
                        setTbody([]);
                        _this.setTotal(0);
                    }
                }
            });
        }, 100);
    }
});
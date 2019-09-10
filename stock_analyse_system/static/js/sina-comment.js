function query_comment() {
    var begin_time = $("#begin_time").val();
    var end_time = $("#end_time").val();
    var token = check_token();
    $.ajax({
        url : "/sina/get_word_nephogram",
        type : "post",
        data : {"begin_time":begin_time,"end_time":end_time,"token":token},
        success : function (res) {
            if(res.code == "0000"){
                $("#stock_comment_img").attr("src","/static/comment_picture/"+res.picture_url)
            }
        },
        error : function () {
            alert("查询失败，请联系管理员")
        }
    })

};

function add_shield_word() {
    var field_word = $("#field_word").val();
    if(field_word == undefined || field_word == ""){
        alert("请先输入屏蔽词汇")
    }
     var token = check_token();
     $.ajax({
        url : "/sina/add_shield_word",
        type : "post",
        data : {"field_word":field_word,"token":token},
        success : function (res) {
            if(res.code == "0000"){
                alert("添加成功")
            }
        },
        error : function () {
            alert("添加失败，请联系管理员")
        }
    })
};

function open_history_picture(t) {

    $("#stock_comment_img").attr('src', t.src);

}
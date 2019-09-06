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

}
function change_content(page_name) {
    var token = sessionStorage.getItem("token");
    if(token == undefined){
         window.location.href = "/auth/login";
     }
    var url = "/auth/change_content?token="+token+"&pageName="+page_name;
    $("#content").attr("src",url);
}

function change_strategy(page_name,strategy_id) {
    sessionStorage.setItem("strategy_id",strategy_id)
    change_content(page_name)
}
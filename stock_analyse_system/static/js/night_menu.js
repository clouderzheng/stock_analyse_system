function change_content(page_name) {
    var token = sessionStorage.getItem("token");
    if(token == undefined){
         window.location.href = "/auth/login";
     }
    var url = "/auth/change_content?token="+token+"&pageName="+page_name;
    $("#content").attr("src",url);
}

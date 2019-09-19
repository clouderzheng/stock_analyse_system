function echart_k(times,codeName,data,indexName,volume,yaxis) {
    var option = {
    title : {
        text: codeName
    },
    tooltip : {
        trigger: 'axis',
        formatter: function (params) {
            var res = params[0].seriesName + ' ' + params[0].name;
            res += '<br/>  开盘 : ' + params[0].value[0] + '  最高 : ' + params[0].value[3];
            res += '<br/>  收盘 : ' + params[0].value[1] + '  最低 : ' + params[0].value[2];
            res += '<br/>  成交量 : ' + params[1].value ;
            return res;
        }
    },
    legend: {
        data:["指数","成交量"]
    },

    dataZoom : {
        show : true,
        realtime: true,
        start : 50,
        end : 100
    },
    xAxis : [
        {
            type : 'category',
            boundaryGap : true,
            axisTick: {onGap:false},
            splitLine: {show:false},
            data : times
        }
    ],
    yAxis : [
        {
            type : 'value',
            scale:true,
            name : "指数",
            boundaryGap: [0.01, 0.01]
        },
        {
            type : 'value',
            name : "交易量",
            scale:true,
            max : yaxis
        }
    ],
    series : [
        {
            name:codeName,
            type:'k',
            data:data// 开盘，收盘，最低，最高
        },
        {
            name:codeName,
            type:'bar',
            yAxisIndex: 1,
            data:volume,// 成交量
            itemStyle:{
                     normal:{
                       color:function (params,data) {
                           var index = params.dataIndex;
                           if(index == 0){
                                return "red";
                           }
                           var today_volume = params.series.data[index];
                           var lastday_volume = params.series.data[index - 1];
                           if(today_volume > lastday_volume){
                               return  "red";
                           }else{
                               return  "green";
                           }
                       },
                       }},
        }
    ]
};
$("#"+indexName).css({"width":$(".index-info-night").width(),"height":$(".index-info-night").height()})
var myChart = echarts.init(document.getElementById(indexName));
myChart.setOption(option);
};

//校验token是否存在方法
function check_token() {
    var token = sessionStorage.getItem("token");
    if(token == undefined){
         window.location.href = "/auth/login";
         return ;
    }
    return token;
}



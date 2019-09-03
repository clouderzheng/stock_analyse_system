from get_international_indice import InternationalIndice
import numpy as np
import math
def get_international_index(result,code ,code_name):

    internationalIndice = InternationalIndice()
    # 获取纳克达斯指数
    data = internationalIndice.get_International_Index(code)

    # 按照时间先后排序 升序
    data = data.sort_values(by="day", axis=0, ascending=True)
    deal_with_data(result,data,code_name,"day")

def get_internal_index_service(result,code,code_name):
    internationalIndice = InternationalIndice()
    data = internationalIndice.get_internal_Index(code)
    deal_with_data(result,data,code_name,"index")

def deal_with_data(result,data , suff,sort_column):

    times = []
    # 获取时间作为x轴
    if("index" == sort_column):
        date_ = data.index.date
        for _date in date_:
            times.append(str(_date))
    else:
        for _date in np.array(data[sort_column]).tolist():
            times.append(str(_date))


    # 开盘价 收盘价 最高价 最低价最为 y轴
    view_data = np.array(data[['open', 'close', 'low', 'high']]).tolist()
    # 指数名称作为提示指标
    code_name =suff
    result["times_" + suff] =  times
    result["view_data_" + suff] =  view_data
    result["code_name_" + suff] =  code_name
    volumes = np.array(data['volume']).tolist()
    result["volume_" + suff] = volumes
    result["volume_yaxis_" + suff] =  math.ceil(max(volumes) * 3)
# import pandas as pd
# internationalIndice = InternationalIndice()
# data = internationalIndice.get_SSE_50_Index(100)
# # print(type(data.index[0]))
# date = data.index.date

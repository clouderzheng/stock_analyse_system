import tushare as ts
from python.mysql import mysql_pool
#
# print(ts.__version__)
# pool = mysql_pool.sql_pool()
#
# sql = "select  stock_code,`current_date` from stock_hostory_data limit 1"
# # sql = "select * from system_user"
# stocks = pool.selectMany(sql)
#
# for stock in stocks:
#     df = ts.get_tick_data(code=stock["stock_code"], date=stock["current_date"], src="nt")
#     # df = ts.get_hist_data('000002',start='2019-12-05',end='2020-04-18')
#     data = df.drop(["change", "amount"], axis=1)
#     sl = "insert into stock_history_tick_data(stock_code,create_date,tick_data) values(?,?,?)"
#
#     pool.insert(sl,(stock["stock_code"],stock["current_date"],data.values.tolist()))
#     break

df = ts.get_tick_data(code="600898", date="2020-04-20", src="nt")
print(df)

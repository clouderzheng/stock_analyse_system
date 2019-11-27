"""股票代码与名称映射集合"""
stock_name_code_mapping = "stock_name_code_mapping"
"""当天股票信息集合"""
current_day_stock_map = "current_day_stock_map"
# current_day_stock_map = "stock"

"""特殊策略时间锁 每隔特定时间才进行选择"""
strategy_lock = "strategy_lock"
"""策略时间锁时间 减去半天时间为了防止再次开始时未解锁"""
strategy_lock_time = 7 * 24 * 60 * 60 - 12 * 60 * 60
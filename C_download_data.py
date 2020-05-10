import yfinance as yf
from datetime import date, datetime

today_date = date.today()
today_date_str = today_date.strftime("%Y-%m-%d")

start_date = date(2010, 1, 1)
end_date = date(2020, 4, 24)
diff = today_date - end_date
new_start_date = start_date + diff
start_date_str = new_start_date.strftime("%Y-%m-%d")

names_list = ['^GSPC', '000001.SS', '^N100', '^HSI', '^KS11', '^N225', '^BSESN']
index_list = []
for i in range(len(names_list)):
	tickerSymbol = names_list[i]
	tickerData = yf.Ticker(tickerSymbol)
	df = tickerData.history(period='1d', start=start_date_str, end=today_date_str).fillna(method ='pad')
	# df = tickerData.history(period='1d', start='2010-01-01', end='2018-01-01').fillna(method ='pad')
	df.drop(['Stock Splits', 'Dividends', 'Open'], axis='columns', inplace=True)
	index_list.append(df)

date = []
for df in index_list:
	data = df 
	a = (list(data.index))
	l = len(a)
	train_date_list = []
	for i in range(5):
		a1 = str(a[l-i-1])
		a1 = a1[:10]
		train_date_list.append(a1)
	date.append(train_date_list)
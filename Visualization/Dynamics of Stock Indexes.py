#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta
import math

global INDEX_MAME 
INDEX_MAME = ['NIKKEI', 'HANGSENG', 'SENSEX', 'SP500', 'KOSPI', 'SSE', 'EURONEXT']

#Назви файлів з данимим - потрібні для отримання даних задля побудови графіків і моделювання роботи інвестиційного фонду
adresses_list_NIKKEI = ['NIKKEI.csv']
adresses_list_HANGSENG = ['HANGSENG.csv']
adresses_list_SENSEX = ['SENSEX.csv']
adresses_list_SP500 = ['SP500.csv']
adresses_list_KOSPI = ['KOSPI.csv']
adresses_list_SSE = ['SSE.csv']
adresses_list_EURONEXT = ['EURONEXT.csv']

#тут зберігатимуться дані в обробленому вигляді; саме ці списки будуть використовуватися в графічному інтерфейсі
NIKKEI_prices = []
HANGSENG_prices = []
SENSEX_prices = []
SP500_prices = []
KOSPI_prices = []
SSE_prices = []
EURONEXT_prices = []

#отримуємо інформацію із csv файлу, створюємо список, кожен елемент якого - таблиця для однієї акції 
class get_data_1:
	def __init__(self, adresses):
		self.adress = adresses[0]

	def get_information_1(self):
		stocks_list = []
		stock = pd.read_csv(self.adress, index_col=None)
		stocks_list.append(stock)
		return stocks_list

#залишаємо в таблиці лише колнку із цінами закриття і номери рядків
class get_data_2(get_data_1):
	def __init__(self, adresses):
		super().__init__(adresses)

	def get_information_2(self):
		self.stocks_list = self.get_information_1()
		close_prices_list = []

		for i in range(len(self.stocks_list)):
			stocks = self.stocks_list[i]
			close = stocks['Close']
			close_prices_list.append(close)
		return close_prices_list

#трансформуємо таблицю з однією колонкою в список, елементи якого дорівнюють значенням рядків таблиці
class get_data_3(get_data_2):
	def __init__(self, adresses):
		super().__init__(adresses)

	def get_information_3(self):
		self.close_prices_list = self.get_information_2()
	
		list_of_stock_prices = []
		for element in self.close_prices_list[0]:
			list_of_stock_prices.append(element)
		return list_of_stock_prices

#створює список, елементи якого - дати, крок між сусідніми датами - один тиждень; потрібен, аби намалювати графік
class Time_list_month:
	def __init__(self, list_of_stock_prices):
		self.list_of_stock_prices = list_of_stock_prices

	def time_return(self):
		some_day = dt.datetime(year=1999, month=12, day=25)
		time = [] #зберігатиме число місяців, які пройшли з початку торгівлі
		for i in range(len(self.list_of_stock_prices)):
			some_day += timedelta(days=7)
			time.append(some_day)
		return time 

#малює графік за списком цін і списком дат; зберігає його як файл визначеного розміру у форматі jpg
class draw_graph:
	def __init__(self, list_of_stock_prices, time, name):
		self.list_of_stock_prices = list_of_stock_prices
		self.time = time
		self.name = name

	def draw(self):
		# print(len(self.list_of_stock_prices))
		plt.plot(self.time, self.list_of_stock_prices, color='mediumblue', linewidth=0.9)
		plt.tight_layout()
		plt.gcf().subplots_adjust(top=0.9, bottom=0.13, left=0.15)
		font = {'fontname':'Times New Roman'}
		plt.ylabel('\nЗначення індексу', {'fontname':'Times New Roman'})
		plt.xlabel('Дата', **font)
		index_name = ''
		for i in range(len(self.name)-4):
			index_name = index_name + self.name[i]
		plt.title('Динаміка індексу '+index_name, **font)
		ax = plt.axes()
		ax.spines["right"].set_visible(False)
		ax.spines["top"].set_visible(False)
		for tick in ax.get_xticklabels():
			tick.set_fontname("Times New Roman")
		for tick in ax.get_yticklabels():
			tick.set_fontname("Times New Roman")
		plt.savefig(self.name)
		plt.close()

#функція округляє елементи списку (ціни акцій) до 2 знаків після коми 
#потрібно для коректного відображення в графічному інтерфейсі
def round_list(data, my_list):
	for element in data:
		copy = round(element, 2)
		my_list.append(copy)

#отримує на список списків (із даними), список із датами(для осі абсцис) та список імен для майбутніх зображень
#і зберігає графіки з цими іменами
def save_few_graphs(stock_graph_list, time, name_list):
	for i in range(len(stock_graph_list)):
		c = draw_graph(stock_graph_list[i], time, name_list[i])
		c.draw()

#отримуємо оброблені дані для акцій кожної із 5 компаній, які використовуються в моделюванні (ціни по місяцях)
a = get_data_3(adresses_list_NIKKEI)
data_1 = a.get_information_3()
a = get_data_3(adresses_list_HANGSENG)
data_2 = a.get_information_3()
a = get_data_3(adresses_list_SENSEX)
data_3 = a.get_information_3()
a = get_data_3(adresses_list_SP500)
data_4 = a.get_information_3()
a = get_data_3(adresses_list_KOSPI)
data_5 = a.get_information_3()
a = get_data_3(adresses_list_SSE)
data_6 = a.get_information_3()
a = get_data_3(adresses_list_EURONEXT)
data_7 = a.get_information_3()

#створюємо список з датами (в тижнях)
time = Time_list_month(data_1)
time = time.time_return()
stock_graph_list = [data_1, data_2, data_3, data_4, data_5, data_6, data_7]
name_list = ["NIKKEI.jpg", "HANGSENG.jpg", "SENSEX.jpg", "SP500.jpg", "KOSPI.jpg", "SSE.jpg", "EURONEXT.jpg"]#назви для графіків

#зберігаємо графіки у тій же папці, що і код програми 
save_few_graphs(stock_graph_list, time, name_list)


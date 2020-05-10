import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels as sml
import matplotlib.pyplot as plt
import warnings
from itertools import product

from C_download_data import *

names_list = ['^GSPC', '000001.SS', '^N100', '^HSI', '^KS11', '^N225', '^BSESN']
opt_param = [[4, 4, 'nc'], [3, 2, 'nc'], [1, 0, 'nc'], [0, 0, 'c'], [0, 0, 'c'], [0, 0, 'c'], [2, 3, 'nc']]
text_ARIMA, predict_ARIMA = [], []
ARIMA_param = [[] for i in range(7)]

warnings.filterwarnings('ignore')

for i in range(len(index_list)):

	p = range(0, 3)
	d = 1
	q = range(0, 3)
	t = ['c', 'nc']
	parameters = product(p, q, t)
	parameters_list = list(parameters)

	best_aic = float("inf")
	try:
		param_ = opt_param[i]
		best_model = sml.tsa.arima_model.ARIMA(index_list[i]['Close'], \
			order=(param_[0], d, param_[1])).fit(disp=-1, trend=param_[2])
		best_aic = best_model.aic
		for p in best_model.pvalues:
			if p > 0.05:
				raise ValueError
		ARIMA_param[i].append(param_[0])
		ARIMA_param[i].append(1)
		ARIMA_param[i].append(param_[1])
		ARIMA_param[i].append(param_[2])
	except:
		ARIMA_param[i].append(np.nan)
		ARIMA_param[i].append(np.nan)
		ARIMA_param[i].append(np.nan)
		ARIMA_param[i].append(np.nan)

	for param in parameters_list:
		try:
			model=sml.tsa.arima_model.ARIMA(index_list[i]['Close'], \
				order=(param[0], d, param[1])).fit(disp=-1, trend=param[2])
		except:
			continue
		aic = model.aic
		coeff = True
		
		if aic<best_aic:
			for p in model.pvalues:
				if p > 0.05 and coeff != False:
					coeff = False
		else:
			coeff = False

		if coeff == True:
			best_model = model
			best_aic = model.aic
			ARIMA_param[i][0] = param[0]
			ARIMA_param[i][1] = 1
			ARIMA_param[i][2] = param[1]
			ARIMA_param[i][3] = param[2]

	text='ARIMA('+str(ARIMA_param[i][0])+', '+str(ARIMA_param[i][1])+', '+str(ARIMA_param[i][2])+', '+str(ARIMA_param[i][3])+')'  
	text_ARIMA.append(text)

	forecast = best_model.forecast()
	if text_ARIMA[i] != 'ARIMA(nan, nan, nan, nan)':
		if forecast[0][0] > index_list[i]['Close'][len(index_list[i]['Close'])-1]:
			predict_ARIMA.append(1)
		elif forecast[0][0] < index_list[i]['Close'][len(index_list[i]['Close'])-1]:
			predict_ARIMA.append(-1)
		else:
			predict_ARIMA.append(0)
	else:
		predict_ARIMA.append(np.nan)

warnings.filterwarnings('default')
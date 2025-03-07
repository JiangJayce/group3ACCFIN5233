import  matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
from minepy import MINE
import pandas as pd

register_matplotlib_converters()
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

score_data=pd.read_csv('score.csv')
sector_data=pd.read_csv('sector_data.csv')
score_data['avg_score'] = np.round(score_data['score'].rolling(window=10,min_periods=1).mean(), 2)
sector_data['avg_price'] = np.round(sector_data['closing price(yuan)'].rolling(window=10,min_periods=1).mean(), 2)

                        

mine = MINE(alpha=0.6, c=15)
mine.compute_score(score_data['avg_score'], sector_data['avg_price'])
print(mine.mic())

plt.plot(score_data['date'], score_data['avg_score'],linestyle='--',label='sentiments')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.twinx()
plt.plot(sector_data['date'],sector_data['avg_price'],color='red',label='stock price')
plt.xticks(score_data['date'][::5],rotation=45)
plt.legend(loc='upper right')
plt.title('MIC='+str(mine.mic()))
plt.show()

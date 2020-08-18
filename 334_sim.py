import numpy as np
from numpy.random import *
import datetime

def delta_ms(x):
  ans = ((x.days * 86400 + x.seconds) * 1000 + (x.microseconds / 1000))
  return ans

time_s = datetime.datetime.now()

fname = 'result.csv'
with open(fname,mode='w') as f:
  
  print('Hello!')
  f.write('attend_n,delay[ms],median[pt],RoR_prob[%]\n')
  
  np.random.seed(seed=2020)
  n = 1000000    # 試行回数
  time_std = 10. # タイムの標準偏差 [ms]

  res_list = [] 
  for i in range(n):
    res_90day = [randn() for j in range(90)]
    res_list.append(res_90day)

  attend_n_list = [45]
  attend_list = []
  
  for attend_n in attend_n_list:
    print('attend_n:',attend_n)
    
    for i in range(n):
      attend_bool = [rand() for j in range(90)]
      threshold = sorted(attend_bool)[attend_n-1]
      attend_bool = list(map(lambda x: 1. if x<=threshold else 0.,attend_bool))
      attend_list.append(attend_bool)
    
    # 減衰係数
      decay = [ min(1.,(i+1.)/61.)  for i in range(90)]

    for time_avg in [0.1*i for i in range(0,10)]:
      print('Delay:','{:.1f}ms'.format(time_avg))
      point_list = []
      for res,attend in zip(res_list,attend_list):
        record = list(map(lambda x: int(time_avg+time_std*x),res)) #タイムに変換
        record = list(map(lambda x: 10000.*(0.1**(x/100.)) if x>=0 else 0.,record)) #ポイントに変換
        record = (np.array(record) * np.array(decay)) #減衰を考慮
        record = record * np.array(attend) #不参加を考慮
        point = np.mean(sorted(record)[-10:])
        point_list.append(point)
      
      point_list = sorted(point_list)
      median   = np.median(point_list)
      ror_prob = 100*np.mean(list(map(lambda x: 1 if x>=9500 else 0,point_list)))
      f.write(str(attend_n)+','+'{:.1f}'.format(time_avg)+','+'{:.2f}'.format(median)+','+'{:.4f}'.format(ror_prob)+'\n')

time_e = datetime.datetime.now()
print('Execution time:',int(delta_ms(time_e - time_s)),'[ms]')
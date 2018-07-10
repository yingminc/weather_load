import pandas as pd
from datetime import datetime,timedelta

def dealwithshit(d):
   return d.apply(lambda x: x.split(' ')[0] if isinstance(x,str) else x).replace({'--':0}).apply(pd.to_numeric,errors='coerce')




class ob:
    def __init__(self, ob_code ,level, prec_no):
        self.prec = prec_no
        self.code =ob_code
        self.level = level


# obsl = [('a','43','0363'),('a','42','1019'),('a','42','1021'),('s','42','47624'),('a','43','1009'),('a','43','1070'),('a','42','0346'),
#  ('s','43','47626'),('a','44','1002'),('a','43','0364'),('a','43','1232')]
obsl =[('a','44','0371'),('a','45','0382')]

obs = [ob(i[2],i[0],i[1]) for i in obsl]


d1 = datetime(2016,8,7)
d2 = datetime(2017,5,31)

delta = d2-d1
span = []
for i in range(delta.days+1):
     intdate = map(int, str(d1+timedelta(days=i)).split(' ')[0].split('-'))
     span.append(intdate)
print len(span)


# In[ ]:
for ob in obs:
    for day in span:
        yyyy,mm,dd = day[0],day[1],day[2]

        print ob.code, day
        url = 'http://www.data.jma.go.jp/obd/stats/etrn/view/10min_{}1.php?prec_no={}&block_no={}&year={}&month={}&day={}&view='.format(ob.level,ob.prec,ob.code,yyyy,mm,dd)
        w = w = pd.read_html(url)[0]
        w = w.ix[2:]
        if ob.level == 'a':
            w.columns = ['time', 'rain(mm)', 'temp(c)', 'wind_speed(m/s)','wind_dir','max_wind_speed(m/s)', 'max_wind_dir','sun(min)']
        else:
            w.columns = ['time',  'air_pressure(hPa)', 'sea_air_pressure(hPa)','rain(mm)', 'temp(c)','humidity(%)','wind_speed(m/s)','wind_dir','max_wind_speed(m/s)', 'max_wind_dir','sun(min)']
            w = w[['time', 'rain(mm)', 'temp(c)', 'wind_speed(m/s)','wind_dir','max_wind_speed(m/s)', 'max_wind_dir','sun(min)']]
        w['year'], w['month'], w['day']=day

        #clean the format
        w['sun(min)'].fillna(0,inplace=True)

        w['date']=pd.to_datetime(w[['year','month','day']].astype(str).apply(lambda x:"-".join(x),axis=1))
        w.loc[w['time']=='24:00','date']=w.loc[w['time']=='24:00','date']+timedelta(days=1)
        w.loc[w['time']=='24:00','time']='00:00'

        w['datetime']=w['date'].astype(str)+' '+w['time']

        w.drop(['date','time','year','month','day'],axis=1,inplace=True)

        with open('../../p_weather/weather_ob{}_{}.csv'.format(ob.code,yyyy-2000),'a') as f:
            if (mm,dd)==(1,1):
                w.to_csv(f,header = True, index =None, encoding ='utf-8')
            else:
                w.to_csv(f,header = None, index =None,encoding ='utf-8')

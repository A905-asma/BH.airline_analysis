import pandas as pd
import requests
import time
def collect_flight_data(day,flight_dirction):
    '''
    this fun scrape data from BH airport.
    Args:
        day (str): it will be today (TD) or tommorow (TW)
        flight_dirction (STR): it will be ARRIVALS or DEPARTURE

        Returns:
            pandas DataFrame that have 7 columns

    '''
    url= f"https://www.bahrainairport.bh/flight-{flight_dirction}?date={day}"
    response=requests.get(url)
    soup = BeautifulSoup(response.text,)
    time_list = []
    distination_list = []
    airway_list = []
    gate_list = []
    status_list = []
    flight_list = []

    flights = soup.find_all("div",{"class": f"flight-table-list row dv{flight_dirction[:-1].title()}List"})
    
    for f in flights:
        time_list.append(f.find('div',class_='col col-flight-time').text.strip())
        distination_list.append(f.find('div',class_='col col-flight-origin').text.strip())
        try:
            airway_list.append(f.find('img')['alt'])
        except:
            airway_list.append(pd.NA)
        gate_list.append(f.find('div',class_='col col-gate').text.strip()) 
        status_list.append(f.find('div',class_='col col-flight-status').text.strip())
        flight_list.append(f.find('div',class_='col col-flight-no').text.strip())
        
    flights_data = {'distintion':distination_list,
            'flight_number':flight_list,
            'airline':airway_list,
            'gate':gate_list,
            'status':status_list,
            'time':time_list}
    df=pd.DataFrame(flights_data)
    if day=="TD":
        date=datetime.date.today()
    elif day =='TM':
        date=datetime.date.today() + datetime.timedelta(days=1)
    
    df["date"]=date
    df["direction"]=flight_dirction

        
    return df
    
arr_df= collect_flight_data('TD','DEPARTURES')   
arr_df

import time
def collect_arr_dep():
    tables=[]
    directions=['ARRIVALS','DEPARTURES']
    days=["TD","TM"]
    for direction in directions:
        for day in days:
            tables.append(collect_flight_data(day,direction))
            time.sleep(10)
    df=pd.concat(tables)
    return df
    
def save_data(df)
    today=datetime.date.today()
    path=f'all_flights_data_{today}.csv'.replace("-","_")
    df.to_csv(path)

df=collect_arr_dep()
save_data(df)
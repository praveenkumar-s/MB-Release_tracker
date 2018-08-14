import pandas

def groupby_year_month(jsondata,data_struct={}):
    
    for items in jsondata.keys():
        year=pandas.to_datetime(items).strftime('%Y')
        month= pandas.to_datetime(items).strftime('%B')
        date=pandas.to_datetime(items).strftime('%D')
        if(data_struct.has_key(year)):
            if(data_struct[year].has_key(month)):
                if(data_struct[year][month].has_key(date)):
                    data_struct[year][month][date].append(jsondata[items]) 
                else:
                    data_struct[year][month][date]=[]
                    data_struct[year][month][date].append(jsondata[items]) 
            else:
                data_struct[year][month]={}
                data_struct[year][month][date]=[] 
                data_struct[year][month][date].append(jsondata[items]) 
        else:
            data_struct[year]={}
            data_struct[year][month]={}
            data_struct[year][month][date]=[] 
            data_struct[year][month][date].append(jsondata[items]) 
    return data_struct


def monthSorter(list):    
    ls=[]
    for month in ['January','February','March','April','May','June','July','August','September','October','November','December']:
        if(month in list):
            ls.append(month)
    return ls

def date_formater(shortdate):
    return pandas.to_datetime(shortdate).strftime('%d %B %Y')

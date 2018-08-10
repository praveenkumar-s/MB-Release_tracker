import pandas

def groupby_year_month(jsondata,data_struct={}):
    
    for items in jsondata.keys():
        year=pandas.to_datetime(items).strftime('%Y')
        month= pandas.to_datetime(items).strftime('%B')
        if(data_struct.has_key(year)):
            if(data_struct[year].has_key(month)):
                data_struct[year][month].append(jsondata[items]) 
            else:
                data_struct[year][month]=[]
                data_struct[year][month].append({pandas.to_datetime(items).strftime('%D') :jsondata[items]}) 
        else:
            data_struct[year]={}
            data_struct[year][month]=[]
            data_struct[year][month].append({pandas.to_datetime(items).strftime('%D') :jsondata[items]}) 
    return data_struct
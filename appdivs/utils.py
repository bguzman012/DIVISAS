
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def prepare_data_divisas():
    url = 'https://www.infodolar.com.do/'
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")

    gdp = soup.find_all("table", attrs={"class": "cotizaciones"})

    table1 = gdp[1]
    body = table1.find_all("tr")
    head = body[0] 
    body_rows = body[1:] 

    headings = []
    for item in head.find_all("th"): 
        item = (item.text).rstrip("\n")
        headings.append(item)

    all_rows = [] 
    for row_num in range(len(body_rows)): 
        row = [] 
        for row_item in body_rows[row_num].find_all("td"): 
            aa =row_item.text
            row.append(aa)
        all_rows.append(row)

    df = pd.DataFrame(data=all_rows,columns=headings)
    nombres_bancos = []
    for i in range(len(df)):
        df.iloc[i]['Entidad'] = re.sub("(\xa0)|(\r)|(\n)|,","", df.iloc[i]['Entidad'])
        nombres_bancos.append(df.iloc[i]['Entidad'])

        df.iloc[i]['Compra'] = re.sub("(\xa0)|(\r)|(\n)|","", df.iloc[i]['Compra'])
        df.iloc[i]['Venta'] = re.sub("(\xa0)|(\r)|(\n)|","", df.iloc[i]['Venta'])

        compra = df.iloc[i]['Compra']
        df.iloc[i]['Compra'] = float(str(compra).split('$')[1].split(' ')[0].replace(".", "" ).replace(",", "." ))
        
        venta = df.iloc[i]['Venta']
        if venta != '':
            df.iloc[i]['Venta'] = float(str(venta).split('$')[1].split(' ')[0].replace(".", "" ).replace(",", "." ))
    
    

    return nombres_bancos

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
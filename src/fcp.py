import requests
import webbrowser
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FCPEuro:
    def __init__(self, year: str = "1999", model: str = "323i", part_number: str = "33176770788") -> None:
        self.base_path = "https://www.fcpeuro.com/BMW-parts/323i/?year=1999&m=20&e=177&t=6&b=5&d=65&v="
        self.model = model 
        self.year = year 
        self.part_number = part_number

    def sign_in(self, creds):
        pass
    def select_search(self):
        
        # grab group item in df
        # grab first 
        # check if first name and/or descrip contians part number 
        df.find_all("itemprop=name"
        if gname 
        pass

    def grab_item(self, part_num):

        search_path = "https://www.fcpeuro.com/Parts/?keywords="
        search_p = search_path+part_num

        webbrowser.open(search_p)
        return(search_p)

class Table(BaseModel):
    id: int = 1
    No: str = "Foo"
    Description: Optional[str] = "Bar"
    #Supp: datetime = datetime(2020, 1, 1)
    #Qty: datetime = datetime(2020, 1, 1)
    partNumber: str = None

class Car(BaseModel):
    id: int = 1
    Name: str = "323"
    Description: Optional[str] = "Bar"
    submod: datetime = datetime(2020, 1, 1)
    model: datetime = datetime(2020, 1, 1)
    year: str = None


class RealOEM:

    def __init__(self):
        
        self.path = "https://www.realoem.com/bmw/enUS/showparts?id=AM33-USA---E46-BMW-323i&diagId=33_0839"
        soup = self.get_page(self.path)
        table = self.get_table(soup)
        jsonobj = self.get_json(table)
        return None
    
    def list_part_groups():
        part_grps = "https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA-11-1998-E46-BMW-323i"
        res = requests.get(part_grps)
        soup = BeautifulSoup(res.content, features="lxml")
        table = soup.find_all('table')[0] 
        df = pd.read_html(str(table))
        print(df)
        
    def list_parts(grp: str):
        part_grp = f"https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i&mg={grp}"
        res = requests.get(part_grp)
        soup = BeautifulSoup(res.content, features="lxml")
        table = soup.find_all('table')[0] 
        df = pd.read_html(str(table))
        print(df)

    def get_page(self, path):
        res = requests.get(path)
        soup = BeautifulSoup(res.content, features="lxml")
        return soup

    def get_table(self, soup):
        table = soup.find_all('table')[0] 
        df = pd.read_html(str(table))
        return df 

    def get_json(self, df):
        json_asset = df[0].to_json(orient='records')
        return json_asset
    
    def get_bolt(self, obj):
        for e in obj:
            print(e)

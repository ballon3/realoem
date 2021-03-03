 
from datetime import datetime
from typing import List, Optional

import click
import pandas as pd
import webbrowser
import requests
import typer
from bs4 import BeautifulSoup
from pydantic import BaseModel
import lxml
from terminaltables import AsciiTable
from collections import OrderedDict 

basep = "https://www.realoem.com"

@click.group()
def cli():
    pass

class Part(BaseModel):
    set_id: int 
    url: str = None
    title: str = None
    img_url: str = None

@cli.command()
def initdb():
    click.echo("Checking RealOEM database")
    # realoem_raxle = "https://www.realoem.com/bmw/enUS/showparts?id=AM33-USA---E46-BMW-323i&diagId=33_0839"
    res = requests.get("https://www.realoem.com/bmw/enUS/showparts?id=AM33-USA---E46-BMW-323i&diagId=33_0839")
    soup = BeautifulSoup(res.content, features="lxml")
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    # records = df[0].to_json(orient='records')
    click.echo(df)

@cli.command()
def part_groups():
    click.echo("Checking RealOEM database, gathering part groups.")
    URL = 'https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='mg-thumb')
    ttable = [["Part Title", "Part URL" ]]
    i = 0 
    for part in results:
        i += 1
        part_title = part.find('div', class_='title').text.strip()
        part_url = part.find('a', href=True)
        part_data = {"set_id":i, "title":part_title, "url":part_url['href']}
        part = Part(**part_data)
        part_item = [part_title, part_url['href']]
        ttable.append(part_item)
    table = AsciiTable(ttable)
    print(table.table)

@cli.command()
def maingrp():
    click.echo("Select Part Groups")
    URL = 'https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='mg-thumb')
    ttable = [["PID", "Part Title" ]]
    i = 0 
    parts = OrderedDict() 
    for part in results:
        i += 1
        part_title = part.find('div', class_='title').text.strip()
        part_url = part.find('a', href=True)
        part_image = part.find('img')
        part_data = {"set_id":i, "title":part_title, "url":part_url['href'], "img_url":basep+part_image['src']}
        part = Part(**part_data)
        parts[i] = part
        part_item = [str(i), part_title]
        ttable.append(part_item)

    table = AsciiTable(ttable)
    print(table.table)

    value = click.prompt('Which Part Group are we looking at?')
    pobj = parts[int(value)]
    path = basep+pobj.url
    print(path)
    webbrowser.open(path)
    partgrp(path)

def partgrp(url):
    click.echo("Select Part Diagrams")
    #URL = 'https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i&mg=33'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='diag-thumb')
    ttable = [["PID", "Diagram Title" ]]

    i = 0 
    diagrams = OrderedDict() 
    for diagram in results:
        i += 1
        diagram_title = diagram.find('div', class_='title').text.strip()
        diagram_url = diagram.find('a', href=True)
        diagram_image = diagram.find('img')
        diagram_data = {"set_id":i, "title":diagram_title, "url":diagram_url['href'], "img_url":f"https://www.realoem.com{diagram_image['src']}"}
        diagram = Part(**diagram_data)
        diagrams[i] = diagram
        diagram_item = [str(i), diagram_title]
        ttable.append(diagram_item)

    table = AsciiTable(ttable)
    print(table.table)

    value = click.prompt('Which diagram Group are we looking at?')
    pobj = diagrams[int(value)]
    path = basep+pobj.url
    
    img_data = requests.get(pobj.img_url).content
    asset_name = pobj.title.replace(" ", "_") +'.jpg'
    #with open(asset_name, 'wb') as handler:
    #    handler.write(img_data)

    print(path)
    webbrowser.open(path)
    getparts(path)
           
def getparts(path):
    click.echo("Select Part Groups")
    URL = 'https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i'
    page = requests.get(path)
    df_list = pd.read_html(page.text) # this parses all the tables in webpages to a list
    part_df = df_list[0]
    part_df.drop(columns="Notes")
    print(part_df)
app = typer.Typer()

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

if __name__ == "__main__":
    maingrp()

class PartList(BaseModel):
    Parts: List[Part] = None

class Part(BaseModel):
    no: str
    description: str = None 
    supp: str = None 
    qty: str = None 
    date_from: str = None 
    date_to: str = None
    partnum: str = None 
    price: str = None 

 
import webbrowser
from collections import OrderedDict
from datetime import datetime

import click
import lxml
import pandas as pd
import requests
import typer
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

from models import Part
from fcp import FCPEuro

basep = "https://www.realoem.com"

@click.group()
def cli():
    pass

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

    value = click.prompt('Open group in browser?(y/n)')
    if value == "y":
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
    val = click.prompt('Open group in browser?(y/n)')
    if val == "y":
        webbrowser.open(path)

    getparts(path)
           
def getparts(path):
    click.echo("Select Part Groups")
    URL = 'https://www.realoem.com/bmw/enUS/partgrp?id=AM33-USA---E46-BMW-323i'
    page = requests.get(path)
    df_list = pd.read_html(page.text, converters={'Part Number': str}) # this parses all the tables in webpages to a list
    part_df = df_list[0]
    del part_df["Unnamed: 8"]
    
    print(part_df)
    
    euro = FCPEuro()
    items = []
    for ind in part_df.index: 
        try:
            pdescrip = part_df['Description'][ind]
            substrings = ['bolt', 'nut', 'gasket']
            match = any([substring in pdescrip for substring in substrings])
                
            if match: 
                partnum = str(part_df['Part Number'][ind])
                pnum = partnum.split(".", 1)
                print(pdescrip, pnum[0])
                items.append(pnum[0])
        except:
            pass

    set_list = list(set(items)) 

    for x in set_list:
        euro.grab_item(x)

    print("done")
    

app = typer.Typer()

if __name__ == "__main__":
    maingrp()

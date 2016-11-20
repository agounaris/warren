# -*- coding: utf-8 -*-

import click

import requests
from bs4 import BeautifulSoup

@click.command()
def main(args=None):
    """Console script for lehmanbrothers"""
    click.echo("Replace this message by putting your code into "
               "lehmanbrothers.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")

    symbol = 'csco'

    r = requests.get('http://www.nasdaq.com/symbol/{symbol}/financials?query=income-statement'.format(symbol=symbol))
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find('div', attrs={'class':'genTable'})
    table = div.find('table')
    rows = table.find_all('tr')
    statements = []
    result = []
    for row in rows:
        header = row.find('th')
        if header:
            header = header.text.lower().replace(' ', '_').replace(':', '').replace("'", "").replace('/', '-').replace('.', '').replace(',', '')
            cols = row.find_all('td')
            if header == 'period_ending':
                cols = row.find_all('th')
            cols = [ele.text.strip().split('/')[-1] for ele in cols if ele]
            # cols.insert(0, header)
            attribute = [header] + cols[-4:]
            statements.append(attribute)

    # print(len(cols[-4:]))
    for i in range(1, len(cols[-4:])):
        # print(i+1)
        yearly = {item[0]: item[i] for item in statements if len(item)>1}
        result.append(yearly)

if __name__ == "__main__":
    main()

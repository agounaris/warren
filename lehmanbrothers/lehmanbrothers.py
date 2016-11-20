# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup


class NotValidSymbolException(Exception):
    pass


class IncomeStatement(object):
    def __init__(self, values=None):
        if isinstance(values, dict):
            for key, value in values.items():
                setattr(self, key, value)
        else:
            raise ValueError('Parameter not a dict')

    def __eq__(self, income_statement):
        for attr, value in self.__dict__.iteritems():
            value_one = float(re.sub("[^0-9]", "", value))
            value_two = float(re.sub("[^0-9]", "", income_statement.__dict__[attr]))
            if value_two:
                percentage = (value_one - value_two) / value_two
                # print(percentage)
                print('{attr} change is {p:.2%}'.format(attr=attr, p=percentage))
                # break
            else:
                print('{attr} change is zero'.format(attr=attr))


class BalanceSheet(object):
    pass


class CashFlow(object):
    pass


class Statement(object):
    def __init__(self, symbol=None):
        if not symbol:
            raise NotValidSymbolException

        self.income_statements = []
        statements = self.fetch_income_statements(symbol)
        for st in statements:
            self.income_statements.append(IncomeStatement(st))

    @property
    def statements(self):
        return self.income_statements

    def get_statement_by_year(self, year=None):
        if not year:
            raise ValueError('Not a valid year')

        return [income for income in self.income_statements if income.period_ending == year][0]

    @classmethod
    def fetch_income_statements(self, symbol):
        r = requests.get(
            'http://www.nasdaq.com/symbol/{symbol}/financials?query=income-statement'.format(symbol=symbol))
        soup = BeautifulSoup(r.content, 'html.parser')
        div = soup.find('div', attrs={'class': 'genTable'})
        table = div.find('table')
        rows = table.find_all('tr')
        statements = []
        result = []
        for row in rows:
            header = row.find('th')
            if header:
                header = header.text.lower().replace(' ', '_').replace(':', '').replace("'", "").replace('/',
                                                                                                         '-').replace(
                    '.', '').replace(',', '')
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
            yearly = {item[0]: item[i] for item in statements if len(item) > 1}
            result.append(yearly)
        return result

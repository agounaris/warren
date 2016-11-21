# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup


class NotValidSymbolException(Exception):
    pass


class Statement(object):
    def __init__(self, values=None):
        if isinstance(values, dict):
            for key, value in values.items():
                setattr(self, key, value)
        else:
            raise ValueError('Parameter not a dict')

    def __eq__(self, statement):
        for attr, value in self.__dict__.iteritems():
            value_one = float(re.sub("[^0-9]", "", value))
            value_two = float(re.sub("[^0-9]", "", statement.__dict__[attr]))
            if value_two:
                percentage = (value_one - value_two) / value_two
                # print(percentage)
                print(
                    '{attr} change is {p:.2%}'.format(attr=attr, p=percentage))
                # break
            else:
                print('{attr} change is zero'.format(attr=attr))

                # def __str__(self):
                #     """
                #     placeholder
                #
                #     :return:
                #     """
                #     space = 40
                #     text = list()
                #     format_text = Occurrence.format_text
                #     text.append(format_text('Name', self.name, space))
                #     text.append(format_text('Version', self.release.number, space))
                #     text.append(format_text('Start Date', self.start_datetime, space))
                #     text.append(format_text('End Date', self.end_datetime, space))
                #     return '\n'.join(text)


class IncomeStatement(Statement):
    def __init__(self, *args, **kwargs):
        super(IncomeStatement, self).__init__(*args, **kwargs)


class BalanceSheet(Statement):
    def __init__(self, *args, **kwargs):
        super(BalanceSheet, self).__init__(*args, **kwargs)


class CashFlow(Statement):
    def __init__(self, *args, **kwargs):
        super(CashFlow, self).__init__(*args, **kwargs)


class FinancialPerformance(object):
    def __init__(self, symbol=None):
        if not symbol:
            raise NotValidSymbolException

        self._income_statements = []
        self._balance_sheets = []
        self._cash_flows = []
        income_statement = self.fetch_statement(symbol)
        balance_sheets = self.fetch_statement(symbol, query='balance-sheet')
        cash_flows = self.fetch_statement(symbol, query='cash-flow')
        for st in income_statement:
            self._income_statements.append(IncomeStatement(st))
        for st in balance_sheets:
            self._balance_sheets.append(BalanceSheet(st))
        for st in cash_flows:
            self._cash_flows.append(CashFlow(st))

    @property
    def income_statements(self):
        return self._income_statements

    @property
    def balance_sheets(self):
        return self._balance_sheets

    @property
    def cash_flows(self):
        return self._cash_flows

    def get_income_statement_by_year(self, year=None):
        """

        :param year:
        :return:
        """
        if not year:
            raise ValueError('Not a valid year')

        return [income for income in self._income_statements
                if income.period_ending == year][0]

    def get_balance_sheet_by_year(self, year=None):
        """

        :param year:
        :return:
        """
        if not year:
            raise ValueError('Not a valid year')

        return [bs for bs in self._balance_sheets
                if bs.period_ending == year][0]

    def get_cash_flow_by_year(self, year=None):
        """

        :param year:
        :return:
        """
        if not year:
            raise ValueError('Not a valid year')

        return [cf for cf in self._cash_flows
                if cf.period_ending == year][0]

    def return_on_asset(self, end_year=None):
        """

        :param end_year:
        :return:
        """
        if not end_year:
            return None

        income_statement = [income for income in self._income_statements
                            if income.period_ending == end_year][0]
        balance_sheets = [bs for bs in self._balance_sheets
                          if int(bs.period_ending) in [int(end_year),
                                                       int(end_year) - 1]]
        ebit = float(re.sub("[^0-9]", "",
                            income_statement.earnings_before_interest_and_tax))
        this_years_assets = float(
            re.sub("[^0-9]", "", balance_sheets[0].total_assets))
        previous_years_assets = float(
            re.sub("[^0-9]", "", balance_sheets[1].total_assets))
        average_total_assets = (this_years_assets + previous_years_assets) / 2
        return ebit / average_total_assets

    def return_on_equity(self, end_year=None):
        """

        :param end_year:
        :return:
        """
        if not end_year:
            return None
        income_statement = [income for income in self._income_statements
                            if income.period_ending == end_year][0]
        balance_sheets = [bs for bs in self._balance_sheets
                          if int(bs.period_ending) in [int(end_year),
                                                       int(end_year) - 1]]
        net_income = float(re.sub("[^0-9]", "", income_statement.net_income))
        this_years_equity = float(
            re.sub("[^0-9]", "", balance_sheets[0].total_equity))
        previous_years_equity = float(
            re.sub("[^0-9]", "", balance_sheets[1].total_equity))
        equity = (this_years_equity + previous_years_equity) / 2
        return net_income / equity

    def profit_margin(self, end_year=None, use_ebit=False):
        """

        :param end_year:
        :param use_ebit:
        :return:
        """
        if not end_year:
            return None
        income_statement = [income for income in self._income_statements
                            if income.period_ending == end_year][0]
        profit = float(re.sub("[^0-9]", "", income_statement.gross_profit))
        if use_ebit:
            profit = float(re.sub("[^0-9]", "",
                                  income_statement.earnings_before_interest_and_tax))

        total_revenue = float(
            re.sub("[^0-9]", "", income_statement.total_revenue))
        return profit / total_revenue

    @staticmethod
    def fetch_statement(symbol, query='income-statement'):
        r = requests.get(
            'http://www.nasdaq.com/symbol/{symbol}/financials?query={query}'.format(
                symbol=symbol, query=query))
        soup = BeautifulSoup(r.content, 'html.parser')
        div = soup.find('div', attrs={'class': 'genTable'})
        table = div.find('table')
        rows = table.find_all('tr')
        statements = []
        result = []
        for row in rows:
            header = row.find('th')
            if header:
                header = header.text.lower().replace(' ', '_').replace(':',
                                                                       '').replace(
                    "'", "").replace('/',
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

    def fetch_google_statements(self, query='NYSE:ORCL'):
        pass

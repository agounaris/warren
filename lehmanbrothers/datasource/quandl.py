import quandl
import pandas as pd
from api.statements import BalanceSheet
from api.statements import IncomeStatement
from api.statements import CashFlow
from api.statements import FinancialPerformance

codes = [
    'INTANGIBLES',
    'INVENTORY',
    'ASSETS',
    'ASSETSC',
    'LIABILITIESC',
    'LIABILITIES',
    'EQUITY',
    'CAPEX',
    'DEPAMOR',
    'NCFX',
    'NCF',
    'NCFF',
    'NETINC',
    'NCFI',
    'NCFO',
    'GP',
    'TAXEXP',
    'INTEXP',
    'NETINCCMN',
    'RND',
    'SGNA',
    'REVENUE',
    'EBIT',
    'RETEARN',
    'PAYABLES',
]

sample_balance_sheet = {
    'intengibles': 'INTANGIBLES',
    'inventory': 'INVENTORY',
    'total_current_assets': 'ASSETSC',
    'total_assets': 'ASSETS',
    'payables': 'PAYABLES',
    'total_current_liabilities': 'LIABILITIESC',
    'total_liabilities': 'LIABILITIES',
    'retained_earnings': 'RETEARN',
    'total_stockholder_equity': 'EQUITY'}

sample_cash_flow = {
    'capital_expenditures': 'CAPEX',
    'depreciation': 'DEPAMOR',
    'exchange_rate_effect': 'NCFX',
    'net_cash_flow': 'NCF',
    'net_income': 'NETINC',
    'net_investing_cash_flow': 'NCFI',
    'net_operating_cash_flow': 'NCFO',
    'net_financing_cash_flow': 'NCFF'}

sample_income_statement = {
    'ebit': 'EBIT',
    'gross_profit': 'GP',
    'income_tax': 'TAXEXP',
    'interest_expense': 'INTEXP',
    'net_income': 'NETINC',
    'net_income_to_common_shares': 'NETINCCMN',
    'research_and_development': 'RND',
    'sales_general_and_admin': 'SGNA',
    'total_revenue': 'REVENUE'}


class Retriever(object):
    def __init__(self, config, cache_service):
        self._config = config
        self._cache_service = cache_service

    def get_data(self, tokens):
        if not tokens:
            return None

        data = self._cache_service.get_data(tokens)

        if data is None or data.empty:
            quandl.ApiConfig.api_key = self._config['quandl']['api_key']

            tickers = [tokens['dependent_variable']]
            if 'independent_variables' in tokens and isinstance(tokens['independent_variables'], list):
                tickers = tickers + tokens['independent_variables']

            data = quandl.get_table('WIKI/PRICES',
                                    qopts={'columns': ['ticker', 'date', 'close']},
                                    ticker=tickers,
                                    date={'gte': tokens['date_from'], 'lte': tokens['date_to']})

            if not isinstance(data, pd.DataFrame):
                return None

            self._cache_service.save_data(tokens, data)
        return data

    def get_statements(self, tokens, database='SF0', mode='MRY'):
        if not tokens:
            return None

        data = self._cache_service.get_statements(tokens)
        # print(statements)

        if data is None or data.empty:
            needed_quandl_codes = {}
            for code in codes:
                needed_quandl_codes[code] = '{d}/{s}_{c}_{m}'.format(d=database,
                                                                     s=tokens['ticker'],
                                                                     c=code,
                                                                     m=mode)
            quandl.ApiConfig.api_key = self._config['quandl']['api_key']
            data = quandl.get(list(needed_quandl_codes.values())).to_csv()

            self._cache_service.save_statements(tokens, statements)



        balance_sheets = []
        income_statements = []
        cash_flows = []
        for timestamp, row_data in data.iterrows():
            # print(timestamp)
            # print(row_data['SF0/AAPL_DEPAMOR_MRY - Value'])

            balance_sheet = {}
            for key, value in sample_balance_sheet.items():
                balance_sheet[key] = row_data[self._format_code(tokens['ticker'], value)]
            balance_sheet['year'] = timestamp.year
            balance_sheets.append(BalanceSheet(balance_sheet))

            income_statement = {}
            for key, value in sample_income_statement.items():
                income_statement[key] = row_data[self._format_code(tokens['ticker'], value)]
            income_statement['year'] = timestamp.year
            income_statements.append(IncomeStatement(income_statement))

            cash_flow = {}
            for key, value in sample_cash_flow.items():
                cash_flow[key] = row_data[self._format_code(tokens['ticker'], value)]
            cash_flow['year'] = timestamp.year
            cash_flows.append(CashFlow(cash_flow))

        fp = FinancialPerformance(tokens['ticker'],
                                  income_statements,
                                  balance_sheets,
                                  cash_flows)

        return fp


    def _format_code(self, ticker, code, database='SF0', mode='MRY'):
        return '{d}/{s}_{c}_{m} - Value'.format(d=database,
                                                s=ticker,
                                                c=code.upper(),
                                                m=mode)

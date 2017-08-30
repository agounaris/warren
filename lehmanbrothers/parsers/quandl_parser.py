# -*- coding: utf-8 -*-

import os
import click
import json
import quandl
import pprint
import collections

pp = pprint.PrettyPrinter(indent=4)

quandl.ApiConfig.api_key = "Hxy5g7TB9gbWyzd42vys"


def flatten(config=None, parent_key='', sep='.'):
    """Flattens a dictionary to the form of
    key_a.key_b.value
    :param config: string
    :param parent_key: string
    :param sep: string
    :return: dict
    """
    items = []
    for key, value in config.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key.replace(' - Value', ''),
                                 sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


@click.command()
@click.option('--database', default='SF0', help='Database to search')
@click.option('--symbol', prompt='Symbol', help='The symbol to fetch.')
@click.option('--mode', default='MRY', help='The frequency of data')
def main(database, symbol, mode):
    """

    :param database:
    :param symbol:
    :param mode:
    :return:
    """
    symbol = symbol.upper()

    data = {
        'financial_performance': {
            'balance_sheets': {
                'yearly': [
                ]},
            'cash_flows': {
                'yearly': [
                ]},
            'income_statements': {
                'yearly': [
                ]}},
        'symbol': symbol}

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

    needed_quandl_codes = {}
    for code in codes:
        needed_quandl_codes[code] = '{d}/{s}_{c}_{m}'.format(d=database,
                                                             s=symbol,
                                                             c=code,
                                                             m=mode)

    balance_sheet = {
        'intengibles': needed_quandl_codes['INTANGIBLES'],
        'inventory': needed_quandl_codes['INVENTORY'],
        'total_current_assets': needed_quandl_codes['ASSETSC'],
        'total_assets': needed_quandl_codes['ASSETS'],
        'payables': needed_quandl_codes['PAYABLES'],
        'total_current_liabilities': needed_quandl_codes['LIABILITIESC'],
        'total_liabilities': needed_quandl_codes['LIABILITIES'],
        'retained_earnings': needed_quandl_codes['RETEARN'],
        'total_stockholder_equity': needed_quandl_codes['EQUITY'],
        'total_liabilities_and_equity': needed_quandl_codes['LIABILITIES']+needed_quandl_codes['EQUITY'],
        'year': 2016
        }

    cash_flow = {
        'capital_expenditures':needed_quandl_codes['CAPEX'],
        'date_released': '2016-01-01',
        'depreciation': needed_quandl_codes['DEPAMOR'],
        'exchange_rate_effect': needed_quandl_codes['NCFX'],
        'net_cash_flow': needed_quandl_codes['NCF'],
        'net_income': needed_quandl_codes['NETINC'],
        'net_investing_cash_flow': needed_quandl_codes['NCFI'],
        'net_operating_cash_flow': needed_quandl_codes['NCFO'],
        'net_financing_cash_flow': needed_quandl_codes['NCFF'],
        'year': 2016}

    income_statement = {
        'date_released': '2016-01-01',
        'ebit': needed_quandl_codes['EBIT'],
        'gross_profit': needed_quandl_codes['GP'],
        'income_tax': needed_quandl_codes['TAXEXP'],
        'interest_expense': needed_quandl_codes['INTEXP'],
        'net_income': needed_quandl_codes['NETINC'],
        'net_income_to_common_shares': needed_quandl_codes['NETINCCMN'],
        'research_and_development': needed_quandl_codes['RND'],
        'sales_general_and_admin': needed_quandl_codes['SGNA'],
        'total_revenue': needed_quandl_codes['REVENUE'],
        'year': 2016}

    values_from_quandl_file = os.path.join(os.path.dirname(__file__), '..',
                                           'data',
                                           '{symbol}_quandl.json'.format(
                                               symbol=symbol))

    # Lets check if the symbol data file exists otherwise call the quandl api
    if not os.path.isfile(values_from_quandl_file):
        # print(list(needed_quandl_codes.values()))
        response = quandl.get(list(needed_quandl_codes.values())).to_dict()
        quandl_data = {}
        for key, value in response.items():
            timeseries = {}
            for timestamp, numeric_value in value.items():
                time_key = '{}-{}-{}'.format(timestamp.day, timestamp.month,
                                             timestamp.year)
                timeseries[time_key] = numeric_value
            quandl_data[key] = timeseries
        with open(values_from_quandl_file, 'w') as file_:
            file_.write(json.dumps(quandl_data))
    else:
        with open(values_from_quandl_file, 'r') as file_:
            quandl_data = json.loads(file_.read())

    balance_sheets = []
    income_statements = []
    cash_flows = []

    key, value = quandl_data.popitem()
    years = [v for v in value.keys()]

    quandl_data = flatten(quandl_data)

    for year in years:
        parsed_balance_sheet = {}
        parsed_income_statement = {}
        parsed_cash_flow = {}

        parsed_balance_sheet['year'] = year.split('-')[-1]
        parsed_income_statement['year'] = year.split('-')[-1]
        parsed_cash_flow['year'] = year.split('-')[-1]
        for element, value in balance_sheet.items():
            if element == 'date_released':
                parsed_balance_sheet['date_released'] = year

            quandl_code = '{value}.{date_released}'.format(value=value,
                                                           date_released=year)
            if quandl_code in quandl_data.keys():
                parsed_balance_sheet[element] = quandl_data[quandl_code]
            else:
                if element != 'year' and element != 'date_released':
                    parsed_balance_sheet[element] = 0.0

        balance_sheets.append(parsed_balance_sheet)

        for element, value in income_statement.items():
            if element == 'date_released':
                parsed_income_statement['date_released'] = year

            quandl_code = '{value}.{date_released}'.format(value=value,
                                                           date_released=year)
            if quandl_code in quandl_data.keys():
                parsed_income_statement[element] = quandl_data[quandl_code]
            else:
                if element != 'year' and element != 'date_released':
                    parsed_income_statement[element] = 0.0

        income_statements.append(parsed_income_statement)

        for element, value in cash_flow.items():
            if element == 'date_released':
                parsed_cash_flow['date_released'] = year

            quandl_code = '{value}.{date_released}'.format(value=value,
                                                           date_released=year)
            if quandl_code in quandl_data.keys():
                parsed_cash_flow[element] = quandl_data[quandl_code]
            else:
                if element != 'year' and element != 'date_released':
                    parsed_cash_flow[element] = 0.0

        cash_flows.append(parsed_cash_flow)

    data['financial_performance']['balance_sheets']['yearly'] = balance_sheets
    data['financial_performance']['income_statements'][
        'yearly'] = income_statements
    data['financial_performance']['cash_flows']['yearly'] = cash_flows

    path = os.path.join(os.path.dirname(__file__), '..', 'data',
                        '{symbol}.json'.format(symbol=symbol))
    with open(path, 'w') as file_:
        file_.write(json.dumps(data))


if __name__ == "__main__":
    main()

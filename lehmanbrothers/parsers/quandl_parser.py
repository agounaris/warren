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
        'INTANGIBLES', 'INVENTORY', 'ASSETS', 'ASSETSC', 'LIABILITIESC',
        'LIABILITIES', 'EQUITY', 'CAPEX', 'DEPAMOR', 'NCFX', 'NCF', 'NCFF',
        'NETINC', 'NCFI', 'NCFO', 'GP', 'TAXEXP', 'INTEXP', 'NETINCCMN',
        'RND', 'SGNA', 'REVENUE'
    ]

    needed_quandl_codes = {}
    for code in codes:
        needed_quandl_codes[code] = '{d}/{s}_{c}_{m}'.format(d=database,
                                                             s=symbol,
                                                             c=code,
                                                             m=mode)

    balance_sheet = {
        'accounts_payable': 0.0,
        'capital_surplus': 0.0,
        'cash_and_cash_equivalents': 0.0,
        'common_stocks': 0.0,
        'date_released': '2016-01-01',
        'deferred_asset_charges': 0.0,
        'deferred_liabilities_charges': 0.0,
        'fixed_assets': 0.0,
        'goodwill': needed_quandl_codes['INTANGIBLES'],
        'intangible_assets': 0.0,
        'inventory': needed_quandl_codes['INVENTORY'],
        'long_term_debt': 0.0,
        'long_term_investments': 0.0,
        'minority_interest': 0.0,
        'net_receivables': 0.0,
        'other_assets': 0.0,
        'other_current_assets': 0.0,
        'other_current_liabilities': 0.0,
        'other_liabilities': 0.0,
        'other_stockholder_equity': 0.0,
        'retained_income': 0.0,
        'short_current_long_term_debt': 0.0,
        'short_term_investments': 0.0,
        'total_assets': needed_quandl_codes['ASSETS'],
        'total_current_assets': needed_quandl_codes['ASSETSC'],
        'total_current_liabilities': needed_quandl_codes['LIABILITIESC'],
        'total_liabilities': needed_quandl_codes['LIABILITIES'],
        'total_liabilities_and_equity': 0.0,
        'total_stockholder_equity': needed_quandl_codes['EQUITY'],
        'treasury_stock': 0.0,
        'year': 2016}

    cash_flow = {
        'capital_expenditures':needed_quandl_codes['CAPEX'],
        'date_released': '2016-01-01',
        'depreciation': needed_quandl_codes['DEPAMOR'],
        'exchange_rate_effect': needed_quandl_codes['NCFX'],
        'inventory_changes': 0.0,
        'investments': 0.0,
        'liability_changes': 0.0,
        'net_borrowings': 0.0,
        'net_cash_flow': needed_quandl_codes['NCF'],
        'net_financing_cash_flow': needed_quandl_codes['NCFF'],
        'net_income': needed_quandl_codes['NETINC'],
        'net_income_adjustments': 0.0,
        'net_investing_cash_flow': needed_quandl_codes['NCFI'],
        'net_operating_cash_flow': needed_quandl_codes['NCFO'],
        'other_changes': 0.0,
        'other_financing_activities_cash_flow': 0.0,
        'other_investing_activities': 0.0,
        'receivable_changes': 0.0,
        'sale_purchase_of_stock': 0.0,
        'year': 2016}

    income_statement = {
        'additional_income_expense': 0.0,
        'cost_of_revenue': 0.0,
        'date_released': '2016-01-01',
        'ebit': needed_quandl_codes['ASSETS'],
        'gross_profit': needed_quandl_codes['GP'],
        'income_before_tax': 0.0,
        'income_tax': needed_quandl_codes['TAXEXP'],
        'interest_expense': needed_quandl_codes['INTEXP'],
        'minority_interest': 0.0,
        'net_income': needed_quandl_codes['NETINC'],
        'net_income_to_common_shares': needed_quandl_codes['NETINCCMN'],
        'non_recurring_items': 0.0,
        'operating_income': 0.0,
        'other_operating_items': 0.0,
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
        response = quandl.get(needed_quandl_codes.values()).to_dict()
        quandl_data = {}
        for key, value in response.iteritems():
            timeseries = {}
            for timestamp, numeric_value in value.iteritems():
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
        for element, value in balance_sheet.iteritems():
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

        for element, value in income_statement.iteritems():
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

        for element, value in cash_flow.iteritems():
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

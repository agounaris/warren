# -*- coding: utf-8 -*-

import os
import click
import json
import quandl
import pprint
import collections

pp = pprint.PrettyPrinter(indent=4)

quandl.ApiConfig.api_key = "Hxy5g7TB9gbWyzd42vys"

database = 'SF0'
symbol = 'CSCO'
mode = 'MRY'

needed_quandl_codes = [
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='INTANGIBLES', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='INVENTORY', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='ASSETS', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='ASSETSC', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='LIABILITIESC', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='LIABILITIES', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='EQUITY', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='CAPEX', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='DEPAMOR', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NCFX', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NCF', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NCFF', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NETINC', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NCFI', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NCFO', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='GP', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='TAXEXP', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='INTEXP', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='NETINCCMN', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='RND', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='SGNA', m=mode),
    '{d}/{s}_{c}_{m}'.format(d=database, s=symbol, c='REVENUE', m=mode),
]

balance_sheet = {
    'accounts_payable': 0.0,
    'capital_surplus': 0.0,
    'cash_and_cash_equivalents': 0.0,
    'common_stocks': 0.0,
    'date_released': '2016-01-01',
    'deferred_asset_charges': 0.0,
    'deferred_liabilities_charges': 0.0,
    'fixed_assets': 0.0,
    'goodwill': 'SF0/CSCO_INTANGIBLES_MRY',
    'intangible_assets': 0.0,
    'inventory': 'SF0/CSCO_INVENTORY_MRY',
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
    'total_assets': 'SF0/CSCO_ASSETS_MRY',
    'total_current_assets': 'SF0/CSCO_ASSETSC_MRY',
    'total_current_liabilities': 'SF0/CSCO_LIABILITIESC_MRY',
    'total_liabilities': 'SF0/CSCO_LIABILITIES_MRY',
    'total_liabilities_and_equity': 0.0,
    'total_stockholder_equity': 'SF0/CSCO_EQUITY_MRY',
    'treasury_stock': 0.0,
    'year': 2016}

cash_flow = {
    'capital_expenditures': 'SF0/CSCO_CAPEX_MRY',
    'date_released': '2016-01-01',
    'depreciation': 'SF0/CSCO_DEPAMOR_MRY',
    'exchange_rate_effect': 'SF0/CSCO_NCFX_MRY',
    'inventory_changes': 0.0,
    'investments': 0.0,
    'liability_changes': 0.0,
    'net_borrowings': 0.0,
    'net_cash_flow': 'SF0/CSCO_NCF_MRY',
    'net_financing_cash_flow': 'SF0/CSCO_NCFF_MRY',
    'net_income': 'SF0/CSCO_NETINC_MRY',
    'net_income_adjustments': 0.0,
    'net_investing_cash_flow': 'SF0/CSCO_NCFI_MRY',
    'net_operating_cash_flow': 'SF0/CSCO_NCFO_MRY',
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
    'ebit': 'SF0/CSCO_ASSETS_MRY',
    'gross_profit': 'SF0/CSCO_GP_MRY',
    'income_before_tax': 0.0,
    'income_tax': 'SF0/CSCO_TAXEXP_MRY',
    'interest_expense': 'SF0/CSCO_INTEXP_MRY',
    'minority_interest': 0.0,
    'net_income': 'SF0/CSCO_NETINC_MRY',
    'net_income_to_common_shares': 'SF0/CSCO_NETINCCMN_MRY',
    'non_recurring_items': 0.0,
    'operating_income': 0.0,
    'other_operating_items': 0.0,
    'research_and_development': 'SF0/CSCO_RND_MRY',
    'sales_general_and_admin': 'SF0/CSCO_SGNA_MRY',
    'total_revenue': 'SF0/CSCO_REVENUE_MRY',
    'year': 2016}

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
    'symbol': 'csco'}


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
def main(args=None):
    """Console script for lehmanbrothers"""

    values_from_quandl_file = os.path.join(os.path.dirname(__file__), '..',
                                           'data',
                                           '{symbol}_quandl.json'.format(
                                               symbol=symbol))
    if not os.path.isfile(values_from_quandl_file):
        response = quandl.get(needed_quandl_codes).to_dict()
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

    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'csco.json')
    with open(path, 'w') as file_:
        file_.write(json.dumps(data))


if __name__ == "__main__":
    main()

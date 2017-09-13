from lehmanbrothers.api.statements import BalanceSheet
from lehmanbrothers.api.statements import IncomeStatement
from lehmanbrothers.api.statements import CashFlow
from lehmanbrothers.api.statements import FinancialPerformance


data = {
    'ebit': 100,
    'total_assets': 100,
    'net_income': 100,
    'total_stockholder_equity': 100,
    'gross_profit': 100,
    'total_revenue': 100,
    'year': 2016
}

previous_data = {
    'ebit': 100,
    'total_assets': 100,
    'net_income': 100,
    'total_stockholder_equity': 100,
    'gross_profit': 100,
    'total_revenue': 100,
    'year': 2016
}


class TestApi(object):

    def test_init_balance_sheet(self):
        balance_sheet = BalanceSheet(data)

        assert isinstance(balance_sheet, BalanceSheet)

    def test_init_income_statement(self):
        income_statement = IncomeStatement(data)

        assert isinstance(income_statement, IncomeStatement)

    def test_init_cash_flow(self):
        cash_flow = CashFlow(data)

        assert isinstance(cash_flow, CashFlow)

    def test_init_financial_statements(self):
        balance_sheet = BalanceSheet(data)
        income_statement = IncomeStatement(data)
        cash_flow = CashFlow(data)

        fs = FinancialPerformance('TEST',
                                  [income_statement],
                                  [balance_sheet],
                                  [cash_flow])

        assert isinstance(fs, FinancialPerformance)

    def test_get_balance_sheet_by_year(self):
        balance_sheet = BalanceSheet(data)
        income_statement = IncomeStatement(data)
        cash_flow = CashFlow(data)

        fs = FinancialPerformance('TEST',
                                  [income_statement],
                                  [balance_sheet],
                                  [cash_flow])

        assert isinstance(fs.get_balance_sheet_by_year(2016), BalanceSheet)

    def test_get_income_statement_by_year(self):
        balance_sheet = BalanceSheet(data)
        income_statement = IncomeStatement(data)
        cash_flow = CashFlow(data)

        fs = FinancialPerformance('TEST',
                                  [income_statement],
                                  [balance_sheet],
                                  [cash_flow])

        assert isinstance(fs.get_income_statement_by_year(2016),
                          IncomeStatement)

    def test_get_cash_flow_by_year(self):
        balance_sheet = BalanceSheet(data)
        income_statement = IncomeStatement(data)
        cash_flow = CashFlow(data)

        fs = FinancialPerformance('TEST',
                                  [income_statement],
                                  [balance_sheet],
                                  [cash_flow])

        assert isinstance(fs.get_cash_flow_by_year(2016), CashFlow)

    def test_return_on_assets(self):
        bss = [BalanceSheet(data), BalanceSheet(previous_data)]
        ics = [IncomeStatement(data), IncomeStatement(previous_data)]
        cfs = [CashFlow(data), CashFlow(previous_data)]
        fs = FinancialPerformance('TEST',
                                  bss,
                                  ics,
                                  cfs)

        assert fs.return_on_asset(2016) == 1.0

    def test_return_on_equity(self):
        bss = [BalanceSheet(data), BalanceSheet(previous_data)]
        ics = [IncomeStatement(data), IncomeStatement(previous_data)]
        cfs = [CashFlow(data), CashFlow(previous_data)]
        fs = FinancialPerformance('TEST',
                                  bss,
                                  ics,
                                  cfs)

        assert fs.return_on_equity(2016) == 1.0

    def test_profit_margin(self):
        bss = [BalanceSheet(data), BalanceSheet(previous_data)]
        ics = [IncomeStatement(data), IncomeStatement(previous_data)]
        cfs = [CashFlow(data), CashFlow(previous_data)]
        fs = FinancialPerformance('TEST',
                                  bss,
                                  ics,
                                  cfs)

        assert fs.profit_margin(2016) == 1.0

    def test_balance_sheet_compare(self):
        assert BalanceSheet(data) == BalanceSheet(previous_data)

    def test_income_statement_compare(self):
        assert IncomeStatement(data) == IncomeStatement(previous_data)

    def test_cash_flow_compare(self):
        assert CashFlow(data) == CashFlow(previous_data)

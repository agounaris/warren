from lehmanbrothers.api.statements import *

data = {'test': 1, 'test2': 2, 'year': 2016}


class TestApi(object):

    def test_init_balance_sheet(self):
        balance_sheet = BalanceSheet(data)

        assert isinstance(balance_sheet, BalanceSheet)

    def test_init_income_statement(self):
        income_statement = IncomeStatement(data)

        assert isinstance(income_statement, IncomeStatement)

    def test_init_cash_flow(self):
        cash_flow = CashFlow({'test': 1, 'test2': 2})

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

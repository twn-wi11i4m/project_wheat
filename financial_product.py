
class FinancialProduct:
    def __init__(self, invest_capital, initial_date, final_payoff_date) -> None:
        self.invest_capital = invest_capital
        self.initial_date = initial_date
        self.final_payoff_date = final_payoff_date

    def final_return_dollar(self) -> float:
        """
        assume there is some return, i.e., 5% of invest capital
        The dollar is including the management fee and other operational cost in KOI
        """
        return max(self.invest_capital * (1 + 0.05), 0)






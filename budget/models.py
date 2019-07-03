"""
a more clever way to build any payment function/ callable would be to give it an argument
    make_payment_predicate :: (month, day) -> bool
"""

import numpy as np

from budget import accounts

class Modeler(object):
    """
    tracks state and runs the simulation. "statics" should be a list
    """
    def __init__(self, starting_month, statics, dynamics):
        self.month = starting_month
        # self.days = np.unique([d.day for d in dynamics])
        self.days = np.arange(32)   #lol
        self.statics = statics
        self.dynamics = dynamics
        self.loans = [d for d in self.dynamics if isinstance(d, accounts.Loan)]


    def step(self):
        """
        run one month of the sim
        """
        expenditure_this_month = 0
        installment_this_month = 0
        for this_day in self.days:
            for this_dynamic in self.dynamics:
                this_paid_amount = this_dynamic(self.month, this_day)
                expenditure_this_month += this_paid_amount
                if isinstance(this_dynamic, accounts.Loan):
                    installment_this_month += this_paid_amount
        self.month += 1
        return expenditure_this_month, installment_this_month

    def some_steps(self, months):
        """
        returns dictionary {account_name: ndarray([(month, balance)])}
        """
        output = {}
        output["monthly expenditure"] = []
        output["installment expenditure"] = []
        for this_account in self.statics:
            output[this_account.name] = []

        for this_month in range(months):
            # uughhhh i feel dirty
            total_this_month, installment_this_month = self.step()
            output["monthly expenditure"].append((this_month, total_this_month))
            output['installment expenditure'].append((this_month, installment_this_month))

            for this_account in self.statics:
                output[this_account.name].append((this_month, this_account.balance))

        for this_account_name in output.keys():
            output[this_account_name] = np.vstack(output[this_account_name])
        output["monthly expenditure"] = np.vstack(output["monthly expenditure"])
        output["installment expenditure"] = np.vstack(output["installment expenditure"])

        return output

    def net_worth(self):
        loan_total = sum(self.loan_balances())
        account_total = sum(self.account_balances())
        return account_total - loan_total

    def loan_balances(self):
        return [l.balance for l in self.loans]

    def account_balances(self):
        return [a.balance for a in self.statics]



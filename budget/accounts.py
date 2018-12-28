


from budget import utils



class Loan(object):
    """
    special case of Account where balance is expected to go to zero. also it's a dynamic.
    """
    def __init__(self, account, payment, day, balance, apr, name):
        self.account = account
        self.payment = payment
        self.day = day
        self.coupon_factor = apr
        self.balance = balance
        self.name = name

    def goes_in(self, amount):
        """
        this is how you start a loan in the future
        """
        assert amount >= 0, "only add positive values to a loan"
        self.balance += amount


    def comes_out(self, amount):
        """
        someday we might just pay it off (using a PayOff)
        """
        assert amount >= 0, "only remove positive values from a loan"
        self.balance -= amount

        if self.balance == 0:
            print("paid off loan: {}".format(self.name))


    def __repr__(self):
        return "{}: {}".format(self.name, int(self.balance))


    def __call__(self, month, day):
        """
        this gets called once a month. we can set it to compound every n months.
        """
        if self.balance and day == self.day:
            if self.payment > self.balance:
                self.account.comes_out(self.balance)
                expenditure = self.balance
                self.balance = 0
            else:
                self.account.comes_out(self.payment)
                self.balance -= self.payment
                expenditure = self.payment
            if self.balance == 0:
                utils.print_year_month(month)
                print("paid off loan: {}".format(self.name))
        else:
            expenditure = 0

        return expenditure


class CompoundLoan(Loan):
    """
    compounds on the first day of the month (we'll call it day 1 to be safe)
    """
    def __init__(self, account, payment, day, balance, apr, name):
        self.account = account
        self.payment = payment
        self.day = day
        self.balance = balance
        self.coupon_factor = 1 + change_period_of_rate(apr, 1, 12)
        self.name = name

    def __call__(self, month, day):
        """
        ye
        """

        if day == 1:
            self.balance *= self.coupon_factor

        if self.balance and day == self.day:
            if self.payment > self.balance:
                self.account.comes_out(self.balance)
                expenditure = self.balance
                self.balance = 0
            else:
                self.account.comes_out(self.payment)
                self.balance -= self.payment
                expenditure = self.payment
            if self.balance == 0:
                utils.print_year_month(month)
                print("paid off loan: {}".format(self.name))
        else:
            expenditure = 0

        return expenditure


class StudentLoan(Loan):
    """
    compounds daily
    """

    def __init__(self, account, payment, day, balance, apr, name):
        self.account = account
        self.payment = payment
        self.day = day
        self.balance = balance
        self.coupon_factor = 1 + change_period_of_rate(apr, 1, 365)
        self.name = name

    def __call__(self, month, day):
        """
        something always happens! (assuming there is a balance)
        """
        self.balance *= self.coupon_factor

        if self.balance and day == self.day:
            if self.payment > self.balance:
                self.account.comes_out(self.balance)
                expenditure = self.balance
                self.balance = 0
            else:
                self.account.comes_out(self.payment)
                self.balance -= self.payment
                expenditure = self.payment
            if self.balance == 0:
                utils.print_year_month(month)
                print("paid off loan: {}".format(self.name))
        else:
            expenditure = 0

        return expenditure



def pay_a_loan(loan, account, year, month):
    """
    convenience/ constructor thing for PayOff class
    """
    pay_month = utils.year_month_to_months(year, month)
    pay_it = PayOff(loan, account, pay_month, 15)
    return pay_it


def change_period_of_rate(rate, periods_per_year, new_periods_per_year):
    """
    a 5% rate is 0.05, for instance
    """
    return rate * (periods_per_year / new_periods_per_year)


def monthly_rate(principal, apr, months):
    """
    compute the monthly rate
    """
    mpr = change_period_of_rate(apr, 1, 12)
    return (mpr * principal) / (1 - (1 + mpr)**-months)



class PayOff(object):
    """
    attempts to pay off a loan using an account that might not be the usual account it gets paid
    out of
    """

    def __init__(self, loan, account, month, day):
        self.loan = loan
        self.account = account
        self.month = month
        self.day = day

    def __call__(self, month, day):
        """
        one and done
        """
        if self.month == month and self.day == day:
            balance = self.loan.balance
            self.account.comes_out(balance)
            utils.print_year_month(month)
            self.loan.comes_out(balance)
            expenditure = balance
        else:
            expenditure = 0
        return expenditure


class StartLoan(object):
    """
    put a balance on a loan
    """

    def __init__(self, loan, amount, month, day):
        self.loan = loan
        self.amount = amount
        self.month = month
        self.day = day

    def __call__(self, month, day):
        """
        money for nothin
        """
        if self.month == month and self.day == day:
            self.loan.goes_in(self.amount)
        # this is not an expenditure
        return 0


class Account(object):
    """
    a place where money accumulates before it inevitably vanishes
    """

    def __init__(self, name, starting_balance=0):
        self.name = name
        self.balance = starting_balance

    def goes_in(self, amount):
        assert amount >= 0, "only add positive values to an account"
        self.balance += amount

    def comes_out(self, amount):
        assert amount >= 0, "only remove positive values from an account"
        self.balance -= amount
        if self.balance <= 0:
            utils.print_year_month(month)
            raise utils.Overdrawn("account {} has balance: ${}".format(self.name, self.balance))

    def __repr__(self):
        return "{}: {}".format(self.name, int(self.balance))



class RepeatingTransfer(object):
    """
    monthly transfer of funds from account A to account B.
    """
    def __init__(self, a, b, payment, day):
        self.a = a
        self.b = b
        self.payment = payment
        self.day = day

    def __call__(self, _, day):
        if day == self.day:
            self.a.comes_out(self.payment)
            self.b.goes_in(self.payment)
        # putting money into an account does not count as an expenditure
        return 0




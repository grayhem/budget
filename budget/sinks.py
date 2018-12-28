"""

"""

class InstantSink(object):
    """
    same
    """
    def __init__(self, account, value, month, day):
        self.account = account
        self.value = value
        self.month = month
        self.day = day

    def __call__(self, month, day):
        if month == self.month and day == self.day:
            self.account.comes_out(self.value)
            expenditure = self.value
        else:
            expenditure = 0
        return expenditure




class RepeatingSink(object):
    """
    same
    """
    def __init__(self, account, value, day):
        self.account = account
        self.value = value
        self.day = day

    def __call__(self, _, day):
        if day == self.day:
            self.account.comes_out(self.value)
            expenditure = self.value
        else:
            expenditure = 0
        return expenditure





class InstantSource(object):
    """
    happens once and goes away
    """
    def __init__(self, account, value, month, day):
        self.account = account
        self.value = value
        self.month = month
        self.day = day

    def __call__(self, month, day):
        if month == self.month and day == self.day:
            self.account.goes_in(self.value)
        return 0



class RepeatingSource(object):
    """
    happens once a month
    """
    def __init__(self, account, value, day):
        self.account = account
        self.value = value
        self.day = day

    def __call__(self, _, day):
        if day == self.day:
            self.account.goes_in(self.value)
        return 0

"""
stuff around the edges.
the months <-> (year, month) isomorphism isn't. since it isn't bijective.
(1, 0) == 12 == (0, 12)
we coerce it to something aesthetically pleasing in print_year_month, but it's all just a damn lie.
"""

from matplotlib import pyplot as plt


class Overdrawn(Exception):
    def __init__(self, message):
        self.message = message


def months_to_year_month(months):
    year = months // 12
    month = months % 12
    return year, month


def print_year_month(months):
    year, month = months_to_year_month(months)
    if month == 0:
        year -= 1
        month = 12
    print ("{}/{}".format(year, month))


def year_month_to_months(year, month):
    return year * 12 + month


def concatenate_dictionary_values(*dictionaries):
    """
    given some number of dictionaries, concatenate all the values from each into one list
    """
    output = []
    for this_dictionary in dictionaries:
        output += list(this_dictionary.values())
    return output

def plot_expenditures(output, ylim=(0, 3500)):
    """
    """
    plt.figure()
    for name, array in output.items():
        if "expenditure" in name:
            plt.plot(array[:, 0], array[:, 1], label=name)
    plt.legend()
    # plt.yscale("log")
    plt.ylim(ylim)
    plt.grid(True)
    plt.show()

def plot_accounts(output):
    """
    """
    plt.figure()
    for name, array in output.items():
        if "expenditure" not in name:
            plt.plot(array[:, 0], array[:, 1], label=name)

    plt.legend()
    plt.grid(True)
    plt.show()


def get_results(some_model, duration):
    """
    dff
    """
    output = some_model.some_steps(duration)

    plot_accounts(output)
    plot_expenditures(output)


    print()
    print("--------------")
    print("loans:")
    print("----")
    for this_loan in some_model.loans:
        print(this_loan)

    print()
    print("--------------")
    print("accounts:")
    print("----")
    for this_static in some_model.statics:
        print(this_static)
    print("----")

    print()
    print("net worth: {}".format(int(some_model.net_worth())))
    return output


def sequencer(x, f, n):
    if n == 0:
        return x
    else:
        return f(sequencer(x, f, n-1))



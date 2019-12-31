"""
run this every day. enters information into expenditures objects.
"""

from pathlib import Path
import time

import numpy as np
from matplotlib import pyplot as plt

from capture import data



RECORDS_PATH = Path("../records")

def get_filepath(struct_time):
    """
    returns the path to where the file is and makes the parent directory if it doesn't exist yet
    """
    path = RECORDS_PATH / str(struct_time.tm_year) / str(struct_time.tm_mon)
    path.parent.mkdir(exist_ok=True)
    return path


def main(struct_time):
    """
    
    """
    filepath = get_filepath(struct_time)
    if filepath.exists():
        print("loaded expenditures:", filepath.absolute().as_posix())
        expenditures = data.unpickle(filepath.as_posix())
    else:
        print("creating new expenditures: ", filepath.absolute().as_posix())
        expenditures = data.Expenditures()

    day = struct_time.tm_mday
        
    done = False
    while not done:
        choice = capture_choice()
        if choice == "x":
            done = True
        elif choice == "o":
            print("one off expenditure")
            cost = capture_cost()
            explanation = capture_string()
            expenditures.add_one_off(day, cost, explanation)
        else:
            print(data.SINKS[choice])
            cost = capture_cost()
            sink = data.SINKS[choice]
            expenditures.add_sink(day, cost, sink)
    
    plot(expenditures)
    print("ok bye")
    expenditures.pickle(filepath.as_posix())
            


def plot(expenditures):
    """
    cumulative plot of expenditures in each category
    """
    days = np.arange(1, 32)
    total_values = np.zeros(31)
    fig, ax = plt.subplots(nrows=4, ncols=1)

    ax[0].set_title("daily by category")
    for sink in data.SINKS:
        raw = expenditures.data[sink]
        values = np.zeros(31)
        for a in raw:
            values[int(a[0]-1)] += a[1]
        values = np.cumsum(values)
        total_values += values
        ax[0].plot(days, values, label=sink)
    ax[0].legend()

    ax[1].set_title("daily across all categories")
    ax[1].plot(days, total_values)

    ax[2].set_title("daily one-offs")
    off_values = np.zeros(31)
    for a in expenditures.one_offs:
        off_values[int(a[0]-1)] += a[1]
    off_values = np.cumsum(off_values)
    ax[2].plot(days, off_values)

    ax[3].set_title("daily including one-offs")
    ax[3].plot(days, total_values + off_values)

    plt.show()
        

def capture_cost():
    """
    collect cost input for any expense
    """
    print("enter cost")
    value = None
    while value is None:
        value = input(">>> ")
        try:
            value = float(value)
        except ValueError:
            value = None
            print("what")
    return value


def capture_string():
    """
    probably for explaining one off costs
    """
    print("enter explanation")
    return input(">>> ")
        



def capture_choice():
    """
    decide what to do 
    """
    for n, sink in enumerate(data.SINKS):
        print(n, ":" , sink)
    print("o : one off")
    print("x : exit") 
    choice = None
    while choice is None: 
        choice = input(">>> ")
        try:
            choice = int(choice)
        except ValueError:
            if choice != "x" and choice != "o":
                choice = None
                print("what")
        else:
            if choice >= len(data.SINKS):
                choice = None
                print("what")
    return choice
    


if __name__ == "__main__":
    struct_time = time.localtime()
    main(struct_time)
    


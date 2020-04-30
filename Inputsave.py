"""Simple example showing how to get gamepad events."""

from __future__ import print_function
from inputs import get_gamepad
from matplotlib import pyplot as plt
import ast

def main():
    """Just print out some event infomation when the gamepad is used."""
    computeruser = input("What is your computer username in the filesystem? ")
    file = str("C:/Users/" + computeruser + "/AppData/Local/RLBotGUI/SavedOutput.txt")
    boi = open(file, "r")
    savedict = ast.literal_eval(boi.read())
    savedict["Time"][0] = 0
    keylist = list(savedict.keys())[0:-1]
    outlist = []
    for a in range(0, len(savedict["Time"])):
        inlist = []
        for i in keylist:
            inlist.append(str(savedict[i][a]))
        outlist.append(inlist)
    timelist = []

    for a in savedict["Time"]:
        timelist.append(str(a))

    plt.table(cellText=outlist,colLabels=keylist,rowLabels=timelist)
    plt.axis('off')
    plt.savefig("./Bruh.pdf", bbox_inches='tight',dpi=1200,loc='center')
    plt.close()


def record():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            if event.state != 0:
                print("Button " + event.code)
                print(event.state)


if __name__ == "__main__":
    main()
import json
from numpy import*
import matplotlib.pyplot as plt

y = raw_input("Write the name of the file to plot (without .txt) : ")
data = json.load(open(y+'.txt'))

for key, value in data.iteritems() :
    plt.figure()
    print key
    plt.plot(array(value)*180/pi)
    plt.savefig("plot/"+key+'.png')

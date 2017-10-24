from numpy import*
from numpy.linalg import*
from types import MethodType
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from nep_dynamics import*

t0 = 0 #Initial time
tf = 15 #Final time
n = (tf - t0)*100 #Ten samples per second

m = 80 #Mass
g = 9.81 # acceleration of gravity
h = 1 #radius of gyration of the subject
I = 100 #Inertia of the whole body with respect the ankle
k = 1000 # stiffness
ks = k - m*g*h # First parameter
b = (I*ks)**.5 # Second parameter
states_number = 2
print "ks = ", ks
print "b = ", b

#State equations for second orden biomechanical system
def xdot_calc(self,x):
    xdot = zeros((states_number,1))
    xdot[0] = x[1]
    xdot[1] = (-b*x[1] - ks*x[0])/I
    return xdot

#New object for simulation of a dynamic system
sim =  simulation(t0,tf,n,[-.1,0])

#Dynamic class method addition
setattr(simulation, 'xdot_calc', xdot_calc)

#Simulation
xs = sim.simulate('rk4')

t = linspace(t0, tf, n)

#Add process noise
xm = sim.addNoise(xs,0.0001,1)
#Add measurement noise
xm = sim.addNoise(xm,0.000,1)

#Plot result
plt.plot(t, xm[0],label="Data with noise",linewidth=1)
plt.xlim([0,tf])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
plt.show()

#Data for state and parameters estimation
step = 10
zm = sim.getData(xm,step)

#Plot result
plt.plot(t[::step], zm[0],label="Samples for parameter estimation",linewidth=1)
plt.xlim([0,tf])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
plt.show()

from numpy import*
from numpy.linalg import*
from types import MethodType
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from nep_dynamics import*

t0 = 0 #Initial time
tf = 15 #Final time
n = (tf - t0)*100 #Ten samples per second

m = 1; #mass of the pendulum 
g = 9.81; #gravitational acceleration
l = 1; #radius of the pendulum
b = .3; #coefficient of friction at the pivot point
states_number = 2

#State equations for second orden biomechanical system
def xdot_calc(self,x):
    xdot = zeros((states_number,1))
    xdot[0] = x[1]
    xdot[1] =((-g/l)*sin(x[0])-(b*x[1])/(m*l))
    return xdot

#New object for simulation of a dynamic system
sim =  simulation(t0,tf,n,[1, .2])

#Dynamic class method addition
setattr(simulation, 'xdot_calc', xdot_calc)

#Simulation
xs = sim.simulate('rk4')
t = linspace(t0, tf, n)

#Add process noise
xm = sim.addNoise(xs,0.01,1)


#Plot result
plt.plot(t, xm[0],label="Data with noise",linewidth=1)
plt.xlim([0,tf])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
plt.show()

step = 1
zm = sim.getData(xm,step)

#Plot result
plt.plot(t[::step], zm[0],label="Data with noise",linewidth=1)
plt.xlim([0,tf])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)


MeasNoise = 1
ControlNoise = 0.0001
#L = array([[0, 0],[ 1/I,0]])

R = [[MeasNoise, 0], [0 , MeasNoise]] # Measurements covariance
Q = array([[ControlNoise, 0],[ 0, ControlNoise]]) # Process covariance

#H = array([[1, 0],[0, 1]])

def Jacobian(self,xhat,T):
    F0 = [1,T]
    F1 = [(-g/l)*cos(xhat[0])*T, 1-b/(m*l)*T]
    F = array([F0,F1])
    
    H = array([[1, 0],[ 0,1]])
    return F,H


P_init = P_init = eye((2))*2 # Initial estimation error covariance.
kl = discrete_kalman(.01,[-.1,0],P_init)

#Dynamic class method addition
setattr(discrete_kalman, 'xdot_calc', xdot_calc)
setattr(discrete_kalman, 'Jacobian', Jacobian)

#Estate estimation method
story = kl.estateEstimation(zm,Q,R,'euler')


#Plot result
plt.plot(t[::step],story[0],label="Position estimation",linewidth=1)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
plt.show()



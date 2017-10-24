# Discrete Extender Kalman Filter (DEKF) class
# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

from numpy import*
from numpy.linalg import*
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time

from numpy import *

class discrete_kalman:
    """ Discrete Extender Kalman Filter class

        Parameters
        ----------
        T : float
            Period of the sampled data

        x_init: list of floats values, example: [2.0,3.5]
            initial state vector m x 1, where m is the number of states

        P_init: numpy.ndarray or float
            Initial estimation error covariance.
            If type == numpy.ndarray, then this must be of m x m, where m is the number of states
            If type == float, the a m x m matrix will be created as P_init = eye((self.state_number))*P_init
            
    """ 
    def __init__(self,T,x_init,P_init, num_parameters = 0):                       
        self.T = T                       
        self.x_init = x_init
        self.states_number = size(x_init)
        if type(P_init) == float or type(P_init) == int:
            P_init = eye((self.state_number))*P_init
            print ("Initial estimation error covariance = ")
            print (str(P_init))
        self.P_init = P_init
        self.num_parameters = num_parameters
        

    def discrete_ekf(self,xhat,Phat,z,Q,R, method = 'euler'):
        T = self.T

        # Calculate xhatdot form the discrete time state equations
        xhatdot = self.xdot_calc(xhat)

        # Euler integration
        if(method == 'euler'):
            delta = xhatdot * T
        if(method == 'rk2'):
        # Runge-Kutta 2 orden
            k0 = xhatdot*dt
            k1 = self.xdot_calc(xhat + k0/2)*T
            delta = k1
        if(method == 'rk4'):
        # Runge-Kutta 4 orden
            k0 = xhatdot*dt
            k1 = self.xdot_calc(xhat + k0/2)*T
            k2 = self.xdot_calc(xhat + k1/2)*T
            k3 = self.xdot_calc(xhat + k2)*T
            delta = (k0 + 2*k1 + 2*k2 + k3)/6.

        # Discretization
        xhat = xhat + delta;

        #Calculate jacobians for estate estimation
        JF, H = self.Jacobian(xhat,T);

        # Perform the time update of the state and estimation error covariance
        # Apriori values
        Phat = dot(dot(JF,Phat),transpose(JF)) + Q

        # Compute the mesurement update of the state and estimation error covariance
        S = dot(dot(H,Phat),transpose(H)) +R
        K = dot(dot(Phat,transpose(H)),inv(S))
        xhat = xhat + dot(K , (z - dot(H, xhat)))
        n,m = shape(K)
        Phat = dot((eye((n))- dot(K,H)),Phat)
        return xhat,Phat

    def estateEstimation(self,zm,Q,R,method):
        x_init = self.x_init                                    # Copy Initial state estimation
        P_init = self.P_init                                    # Copy initial estimation error covariance

        xhat = zeros((self.states_number,1))                     # Current state
        for i in range(self.states_number):                                     # Copy to numpy.darray
            xhat[i] = x_init[i]
        Phat = P_init                                           # Current covariance value

        n,samples_number = zm.shape                             # Get  number of samples of the simulate data
        story = zeros((self.states_number,samples_number))      # Create matrix where to save the kalman estimations through time
        P_trace = zeros((1,samples_number))                     # Matrix of the trace of P through time
        
        for i in range(int(samples_number)):

            # Copy current states and covariance trace
            for j in range (self.states_number):
                story[j,i] = xhat[j]
                P_trace[0,i] = trace(Phat)

            if(i<samples_number-1):
                z = zeros((self.states_number - self.num_parameters,1))                # Get measurements vector (z) in sample i
                for k in range(self.states_number - self.num_parameters):
                    z[k] = zm[k,i+1]
                       
                xhat, Phat = self.discrete_ekf(xhat,Phat,z,Q,R,method) # Update states and covariance matrix
               
                
        return story


    

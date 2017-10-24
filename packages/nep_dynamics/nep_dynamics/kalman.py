# Extender Kalman Filter Class
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

class kalman:
    """ Kalman filter class

        Parameters
        ----------
        T : float
            period

        dt: float
            Integration time

        L : int
            number of samples

        x_init: list of floats values, example: [2.0,3.5]
            initial state vector m x 1, where m is the number of states
    """
        
    def __init__(self,T,dt,L,R,Q,H,state_number,param_number = '0'):
        self.T = T #time between samples
        self.dt = dt # time integration between samples
        self.L = L
        self.R = R
        self.Q = Q
        self.H = H
        self.state_number = state_number #Number of states of the dynamic system
        self.param_number = param_number #Number of unknown parameters
        

    def ekf_hybrid(self,xhat,P,z,method = 'rk4'):
        R = self.R
        Q = self.Q
        L = self.L
        H = self.H
        dt = self.dt
        T = self.T
        n = T/dt
        
        for i in range(int(n)):
            xhatdot = self.xdot_calc(xhat)
            if(method == 'euler'):
                delta = xhatdot * dt
            if(method == 'rk2'):
            #Runge-Kutta 2 orden
                k0 = xhatdot*dt
                k1 = self.xdot_calc(xhat + k0/2)*dt
                delta = k1
            if(method == 'rk4'):
            #Runge-Kutta 4 orden
                k0 = xhatdot*dt
                k1 = self.xdot_calc(xhat + k0/2)*dt
                k2 = self.xdot_calc(xhat + k1/2)*dt
                k3 = self.xdot_calc(xhat + k2)*dt
                delta = (k0 + 2*k1 + 2*k2 + k3)/6.

            xhat = xhat + delta;
            F = self.Jacobian(xhat);
            Pdot = dot(F,P) + dot(P,transpose(F)) + dot(dot(L,Q),transpose(L))
            P = P + Pdot*dt
        
        K = dot(dot(P,transpose(H)),inv(dot(dot(H,P),transpose(H))+R))
        xhat = xhat + dot(K , (z - dot(H, xhat)));
        n,m = shape(K)
        P = dot((eye((n))- dot(K,H)),P)
        return xhat,P

    def estateEstimation_hybrid(self,ini,P_ini,zm,method,state_error = 0):
        xhat = zeros((self.state_number,1))
        ni = size(ini)
        
        P = P_ini
        for i in range(ni):
            xhat[i] = ini[i]

        diff = 0
        n,m = zm.shape
        story = zeros((self.state_number,m))
        for i in range(int(m)):
            for j in range (self.state_number):
                story[j,i] = xhat[j]
            if(i<m-1):
                z = zeros((self.state_number,1))
                for k in range(self.state_number):
                    z[k] = zm[k,i+1]
                xhat, P = self.ekf_hybrid(xhat,P,z,method)
                if (i<m-1):
                    diff = diff + abs( zm[state_error,i+1] - xhat[state_error])**2
                
        return diff,story


    def parameterEstimation_hybrid(self,ini,P_ini,zm,method,state_error = 0):
        xhat = zeros((self.state_number+ self.param_number,1))
        ni = size(ini)
        
        P = eye((self.state_number+self.param_number))

        npi = self.state_number
        while (npi < self.state_number+self.param_number):
            P[npi,npi] = P_ini
            npi = npi + 1
        
        for i in range(ni):
            xhat[i] = ini[i]
        
        diff = 0
        n,m = zm.shape
        story = zeros((self.state_number+ self.param_number,m))
        for i in range(int(m)):
            z = zeros((self.state_number,1))
            for k in range(self.state_number):
                z[k] = zm[k,i]
            xhat, P = self.ekf_hybrid(xhat,P,z,method)
            diff = diff + abs( z[state_error] - xhat[state_error])**2
            for j in range (self.state_number + self.param_number):
                story[j,i] = xhat[j]
                
        return diff,story

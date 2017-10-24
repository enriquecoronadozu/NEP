# Class for simulation of a dynamic system without input control signal
# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


from numpy import*
from numpy.linalg import*

class simulation (object):
    """ Simulation class of dynamic systems. It is needed to set the initial and final time of the simulation, the number of samples and the initial state

        Parameters
        ----------
        t0 : int
            initial time

        tf: int
            final time, tf must be > than t0

        n : int
            number of samples

        x_init: list of floats values, example: [2.0,3.5]
            initial state vector m x 1, where m is the number of states
    """
    def __init__(self,t0,tf,n,x_init):
        self.t0 = t0 # Initial time
        self.tf = tf # Final time
        self.n = n # Number of samples
        self.dt = float((tf - t0))/n #Time between samples
        #print ("dt =" +  str(self.dt))
        self.states_number = size(x_init) #Number of states of the dynamic system
        self.x_init = x_init

    #  -------- Integration function for simulation ------------
    # x -- state vector
    # method -- "euler", "rk2" or "rk4"

    def integration(self, x, method = 'rk4'):
        """ Integration function

            Parameters
            ----------

            x: numpy.ndarray
                Current state

            method : string
                Can be "euler", "rk2" or "rk4" (Runge-Kutta)

            Returns
            -------

            x : numpy.ndarray
                New state value
        """
        dt = self.dt
        xdot = self.xdot_calc(x)
        delta = 0
        #Euler
        if(method == 'euler'):
            delta = xdot * dt
        if(method == 'rk2'):
        #Runge-Kutta 2 order
            k0 = xdot*dt
            k1 = self.xdot_calc(x + k0/2)*dt
            delta = k1
        if(method == 'rk4'):
        #Runge-Kutta 4 order
            k0 = xdot*dt
            k1 = self.xdot_calc(x + k0/2)*dt
            k2 = self.xdot_calc(x + k1/2)*dt
            k3 = self.xdot_calc(x + k2)*dt
            delta = (k0 + 2*k1 + 2*k2 + k3)/6.
        x = x + delta
        return x


    def simulate(self,method = 'rk4'):
        """ Perform the simulation function

            Parameters
            ----------

            method : string
                Can be "euler", "rk2" or "rk4" (Runge-Kutta)

            Returns
            -------

            xs : numpy.ndarray
                State values through time, shape = m x n = number of states x number of samples (or use xs.shape)
        """
        # Current state value
        x = zeros((self.states_number,1))
        # Matrix of state values through time
        xs = x
        # Copy initial state in x
        for i in range(self.states_number):
            x[i] = self.x_init[i]
        # Calculate the next states in each iteration
        for i in range(int(self.n)-1):
            x = self.integration(x,method)
            # Save the current state in the matrix of states
            xs = concatenate((xs ,x),axis=1)
        return xs

    # ---------  Add normal noise function --------
    # xs -- array with the signal without noise
    # level -- level of noise
    # seed -- random noise numpy seed
    # xm -- return array with guassian noise
    def addNoise(self,xs,sigma2,seed = 1):
        """ Add random noise to the measurements

            Parameters
            ----------

            xs : numpy.ndarray
                Simulated data, shape = m x n = number of states x number of samples

            sigma2:
                Covariance value

            seed:int
                Python random seed


            Returns
            -------

            xm : numpy.ndarray
                Simulated data +  noise, shape = m x n = number of states x number of samples (or use xs.shape)
        """
        # Copy simulated data to xm
        xm = xs
        # Use a random seed
        random.seed(seed)

        ni , mi = xs.shape
        for j in range(mi):
            for i in range(ni):
                xm[i,j] = xm[i,j] + sigma2**.5*random.randn(1)
        return xm

    def getData(self,xm,step):
        """ Sample data from an array of simulated values

            Parameters
            ----------

            xm : numpy.ndarray
                Simulated data, shape = m x n = number of states x number of samples

            step: int
                 Obtain n/step samples from xm, where n is the number of samples of xm

            seed:int
                Python random seed


            Returns
            -------

            zm : numpy.ndarray
                Data sampled from the array of simulated values, use zm.shape to know the number of samples of zm
        """
        zm = zeros((self.states_number,1))
        n,m = xm.shape
        for i in range(int(self.n)):
            if mod(i,step) == 0:
                z = zeros((self.states_number,1))
                for k in range(self.states_number):
                    z[k] = xm[k,i]
                zm = concatenate((zm ,z),axis=1)
        return zm[:,1:]

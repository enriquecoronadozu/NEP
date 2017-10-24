#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

"""@See preprocessed data
"""
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.patches as patches
from numpy import*
from numpy.linalg import*
from scipy import interpolate
from scipy.signal import filtfilt, lfilter
from scipy.signal import medfilt
from scipy.signal import filter_design as ifd
from scipy.stats import multivariate_normal
import scipy.spatial
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
from sklearn.mixture import GMM


class newModel():

    """
    Generate a new GMM model from a dataset
    """

    def __init__(self):
        
        # List of files in the dataset
        self.lista = []

        # List of components for each file
        self.datafiles = []
        

    def ReadFiles(self,names, pfilter = True, tfilter = "median"):
        """ Read the data from a list of files

            :param names: name of the files in the dataset
            :param pfilter: selct if perform a filter operation in the data
            :param tfilter: type of filter used to reduce noise in the data

        """
    
        self.num = 0
        for name in names:
            # Read the data from files
            components = []
            self.data = genfromtxt(name, delimiter=' ')
            self.lista.append(self.data)
            ni,mi = self.data.shape

            #Filter the data for each component
            for i in range(mi):
                noisy_component = self.lista[self.num].transpose()[i]

                if(tfilter == 'median'):
                    n = 3  #order of the median filter
                    data_filtered = medfilt(noisy_component,n)
                    components.append(data_filtered)
                    
            #Add each list of components into a list of datafiles
            self.numSamples,m = self.lista[0].shape
            self.num = self.num + 1
            self.datafiles.append(components)
            
            #print shape(self.datafiles), x1 -> nfile, x2-> n_components, x3 -> n_data


        try:
            self.nfiles,self.n_components, self.n_data = shape(self.datafiles)
        except:
            print("Error: The datafile can have diferent number of samples")

        print "Data correctly read and filtered"
  


    def IMU2matrix(self):
        """ Transform the list self.datafiles with size=(self.nfiles,self.n_components, self.n_data) to a numpy matrix"""

        n = self.n_data
        time = ones((1,n))*arange(0,self.n_data,1)
        g_x_s = ones((1,n))*self.datafiles[0][0].transpose()
        g_y_s = ones((1,n))*self.datafiles[0][1].transpose()
        g_z_s = ones((1,n))*self.datafiles[0][2].transpose()


        i = 1
        while(i < self.num):
            # CREATE THE DATASETS FOR THE GMMs
            timec = ones((1,n))*arange(0,self.n_data,1)
            time = concatenate((time,timec),axis=1)
            g_x_s = concatenate((g_x_s,ones((1,n))*self.datafiles[i][0].transpose()),axis=1)
            g_y_s = concatenate((g_y_s,ones((1,n))*self.datafiles[i][1].transpose()),axis=1)
            g_z_s = concatenate((g_z_s,ones((1,n))*self.datafiles[i][2].transpose()),axis=1)
            i = i +1

        acc = concatenate((time,g_x_s), axis = 0);
        acc = concatenate((acc, g_y_s), axis = 0);
        self.acc = concatenate((acc, g_z_s), axis = 0);

        
    
    def extract3D_acceleration_features(self):
        """ CreateDatasets computes the gravity and body acceleration components of the trials given in the [dataset]s by calling the function GetComponents for each trial and reshapes the results into one set of gravity components and one set of body acceleration components according to the requirements of Gaussian Mixture Modelling.
        """

        #% SEPARATE THE GRAVITY AND BODY-MOTION ACCELERATION COMPONENTS

        #Obtain the number of files
        numFiles = self.nfiles
        
        gravity_trial,body_trial = self.GetComponents(self.datafiles[0][0], self.datafiles[0][1], self.datafiles[0][2])
        self.shortNumSamples, m = gravity_trial.shape
        #print self.shortNumSamples
        #initial values of the dataset arrays
        n = self.shortNumSamples

        time = ones((1,n))*arange(0,self.shortNumSamples,1)
        g_x_s = ones((1,n))*gravity_trial[0:self.shortNumSamples,0].transpose()
        g_y_s = ones((1,n))*gravity_trial[0:self.shortNumSamples,1].transpose()
        g_z_s = ones((1,n))*gravity_trial[0:self.shortNumSamples,2].transpose()
        b_x_s = ones((1,n))*body_trial[0:self.shortNumSamples,0].transpose()
        b_y_s = ones((1,n))*body_trial[0:self.shortNumSamples,1].transpose()
        b_z_s = ones((1,n))*body_trial[0:self.shortNumSamples,2].transpose()

        i = 1
        while(i < self.num):
            gravity_trial,body_trial = self.GetComponents(self.datafiles[i][0], self.datafiles[i][1], self.datafiles[i][2])
            # CREATE THE DATASETS FOR THE GMMs
            timec = ones((1,n))*arange(0,self.shortNumSamples,1)
            time = concatenate((time,timec),axis=1)
            g_x_s = concatenate((g_x_s,ones((1,n))*gravity_trial[0:self.shortNumSamples,0].transpose()),axis=1)
            g_y_s = concatenate((g_y_s,ones((1,n))*gravity_trial[0:self.shortNumSamples,1].transpose()),axis=1)
            g_z_s = concatenate((g_z_s,ones((1,n))*gravity_trial[0:self.shortNumSamples,2].transpose()),axis=1)
            b_x_s= concatenate((b_x_s,ones((1,n))*body_trial[0:self.shortNumSamples,0].transpose()),axis=1)
            b_y_s = concatenate((b_y_s,ones((1,n))*body_trial[0:self.shortNumSamples,1].transpose()),axis=1)
            b_z_s = concatenate((b_z_s,ones((1,n))*body_trial[0:self.shortNumSamples,2].transpose()),axis=1)
            i = i +1



        gravity = concatenate((time,g_x_s), axis = 0);
        gravity = concatenate((gravity, g_y_s), axis = 0);
        self.gravity = concatenate((gravity, g_z_s), axis = 0);

        body = concatenate((time,b_x_s), axis = 0);
        body = concatenate((body,b_y_s), axis = 0);
        self.body = concatenate((body,b_z_s), axis = 0);

    #2.1
    def GetComponents(self, x_axis, y_axis, z_axis):
        """ GetComponents discriminates between gravity and body acceleration by
            applying an infinite impulse response (IIR) filter to the raw
            acceleration data (one trial) given in input.

            :param x_axis: acceleration data in the axis x
            :param y_axis: acceleration data in the axis y
            :param z_axis: acceleration data in the axis z
            :return gravity: gravity component of the acceleration data
            :return body: body component of the acceleration data

            """

        #APPLY IIR FILTER TO GET THE GRAVITY COMPONENTS
        #IIR filter parameters (all frequencies are in Hz)
        Fs = 32;            # sampling frequency
        Fpass = 0.25;       # passband frequency
        Fstop = 2;          # stopband frequency
        Apass = 0.001;      # passband ripple (dB)
        Astop = 100;        # stopband attenuation (dB)
        match = 'pass';     # band to match exactly
        delay = 64;          # delay (# samples) introduced by filtering
        #Create the IIR filter



        # iirdesign agruements
        Wip = (Fpass)/(Fs/2)
        Wis = (Fstop+1e6)/(Fs/2)
        Rp = Apass             # passband ripple
        As = Astop            # stopband attenuation

        # The iirdesign takes passband, stopband, passband ripple,
        # and stop attenuation.
        bb, ab = ifd.iirdesign(Wip, Wis, Rp, As, ftype='cheby1')

        g1 = lfilter(bb,ab,x_axis)
        g2 = lfilter(bb,ab,y_axis)
        g3 = lfilter(bb,ab,z_axis)

        #COMPUTE THE BODY-ACCELERATION COMPONENTS BY SUBTRACTION  (PREGUNTA)
        gravity = zeros((self.numSamples -delay,3));
        body = zeros((self.numSamples -delay,3));

        i = 0
        while(i < self.numSamples-delay):
            #shift & reshape gravity to reduce the delaying effect of filtering
            gravity[i,0] = g1[i+delay];
            gravity[i,1] = g2[i+delay];
            gravity[i,2] = g3[i+delay];

            body[i,0] = x_axis[i] - gravity[i,0];
            body[i,1] = y_axis[i] - gravity[i,1];
            body[i,2] = z_axis[i] - gravity[i,2];
            i = i + 1

        #COMPUTE THE BODY-ACCELERATION COMPONENTS BY SUBTRACTION
        return gravity, body


    #3

    def ObtainNumberOfCluster(self, dtype = "3IMU_acc", feature_extraction = True, algorithm = "KMeans", save = True, path = "", th = 0.69):
        """Compute the expected curve for each dataset

            :param dtype: Type of data
            :param algorithm: algorithm used to obtain the number of clusters
            :param save: bool parameter that indicates if the plots are saved
            :param path: path where the plots will be saved

        """

        #Determine the number of Gaussians to be used in the GMM
        if (dtype == "3IMU_acc"):
            if feature_extraction:
                self.K_gravity = self.TuneK(self.gravity,100,'gravity',save,path)
                print "K gravity = ", self.K_gravity, "\n"
                self.K_body = self.TuneK(self.body,100,'body',save,path,th)
                print "K body = ", self.K_body, "\n"

            else:
                self.K_acc = self.TuneK(self.acc,100,'acceleration',save,path)



    def TuneK(self,set_, maxK, name, save = True, path = ''):
        """ TuneK determines the optimal number of clusters to be used to cluster
            the given [set] with K-means algorithm. It cycles from K = 2 to [maxK].
            The optimization criterion adopted is a variant of the elbow method: at
            each iteration TuneK computes the silhouette values of the clusters
            determined by the K-means algorithm and compares them with the values
            obtained at the previous iteration. When the quality of the
            clustering falls below a fixed threshold, TuneK stops.

            :param set_: either the gravity or the body acc. dataset retrived from
                CreateDatasets
            :param maxK: maximum number of clusters to be used to cluster the given
                dataset.
            :param name: component name (gravity or body)
            :param save: bool parameter that indicates if the plots are saved
            :param path: path where the plots will be saved
            :param th:threshold on the FITNESS of the current clustering
            :return Koptimal: optimal number of clusters to be used to cluster the data
                of the given dataset"""

        # DETERMINE THE OPTIMAL NUMBER OF CLUSTERS (K) FOR THE GIVEN DATASET
        # tuning parameters
        minK = 2         # initial number of clusters to be used
        #first step is outside of the loop to have meaningful initial values
        data = set_.transpose()#[:,1:]
        n_samples, n_features = data.shape
        print   "samples= ", n_samples, "features", n_features
        #n_digits = len(unique(digits.target))
        #labels = digits.target

        print(79 * '_')
        print(name + '\n')
        return self.bench_k_means(data,name,save, path)

    def bench_k_means(self, data, name, save = False, path = '', plot = True):
        """ Silhouette analysis

            :param data: dataset trasposed
            :param name: component name (gravity or body)
            :param save: bool parameter that indicates if the plots are saved
            :param path: path where the plots will be saved
            :return Koptimal: optimal number of clusters to be used to cluster the data of the given dataset"""

        #In this example the silhouette analysis is used to choose an optimal value for n_clusters.
        #Bad pick for the given data due to the presence of clusters with
        #below average silhouette scores and also due to wide fluctuations in the size of the silhouette plots.

        threshold = self.th_cluster;

        #t0 = time()
        X = data
        cmin = 2
        cmax = 50


        for n_clusters in range(cmin,cmax):
            # Create a subplot with 1 row and 2 columns

            if(plot == True):

                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.set_size_inches(18, 7)


                # The 1st subplot is the silhouette plot
                # The silhouette coefficient can range from -1, 1 but in this example all
                # lie within [-0.1, 1]
                ax1.set_xlim([-0.1, 1])
                # The (n_clusters+1)*10 is for inserting blank space between silhouette
                # plots of individual clusters, to demarcate them clearly.
                ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

            # Initialize the clusterer with n_clusters value and a random generator
            # seed of 10 for reproducibility.
            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)
            #cluster_labels = clusterer.fit(X)

            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(X, cluster_labels, metric='sqeuclidean')
            print("For n_clusters =", n_clusters,
                  "The average silhouette_score is :", silhouette_avg)

            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(X, cluster_labels)
            #print sample_silhouette_values

            Koptimal = n_clusters
            #if (Koptimal == maxK):
                #print('MATLAB:noConvergence','Failed to converge to the optimal K: increase maxK.')

            if(silhouette_avg < threshold):
                return (Koptimal)


            y_lower = 10
            for i in range(n_clusters):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = \
                    sample_silhouette_values[cluster_labels == i]

                ith_cluster_silhouette_values.sort()

                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.spectral(float(i) / n_clusters)

                if(plot == True):
                    ax1.fill_betweenx(arange(y_lower, y_upper),
                                      0, ith_cluster_silhouette_values,
                                      facecolor=color, edgecolor=color, alpha=0.7)

                    # Label the silhouette plots with their cluster numbers at the middle
                    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                    # Compute the new y_lower for next plot
                    y_lower = y_upper + 10  # 10 for the 0 samples

            if(plot == True):
                ax1.set_title("The silhouette plot for the various clusters.")
                ax1.set_xlabel("The silhouette coefficient values")
                ax1.set_ylabel("Cluster label")

                # The vertical line for average silhoutte score of all the values
                ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

                ax1.set_yticks([])  # Clear the yaxis labels / ticks
                ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

                # 2nd Plot showing the actual clusters formed
                colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
                ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                            c=colors)

                # Labeling the clusters
                centers = clusterer.cluster_centers_
                # Draw white circles at cluster centers
                ax2.scatter(centers[:, 0], centers[:, 1],
                            marker='o', c="white", alpha=1, s=200)

                for i, c in enumerate(centers):
                    ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)

                ax2.set_title("The visualization of the clustered data.")
                ax2.set_xlabel("Feature space for the 1st feature")
                ax2.set_ylabel("Feature space for the 2nd feature")

                plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                              "with n_clusters = %d" % n_clusters),
                             fontsize=14, fontweight='bold')
                plt.savefig(path +'/' +str(name) + "_c_"+ str(n_clusters) + '.png')

        return Koptimal

    def runGMM(self,dataset,K):
        """ Execute GMM in a data set given a K number of clusters
            :param dataset: either the gravity or the body acc. dataset retrived from CreateDatasets
            :param K: number of clusters
            :return priors: apriori probavbility
            :return mu: mean
            :return sigma: covariance
        """

        gmm = GMM(n_components=K,covariance_type='full')
        gmm.fit(dataset.transpose())

        priors = gmm.weights_
        mu = gmm.means_
        sigma = gmm.covars_

        return priors, mu, sigma


    def GetExpected(self,set_,K,numGMRPoints):
        """GetExpected performs Gaussian Mixture Modeling (GMM) and Gaussian Mixture
        Regression (GMR) over the given dataset. It returns the expected curve
        (expected mean for each point, computed over the values given in the
        [set]) and associated set of covariance matrices defining the "model"
        of the given dataset.

        :param set: either the gravity or the body acc. dataset retrived from CreateDatasets
        :param K: optimal number of clusters to be used to cluster the data of the given dataset retrieved from TuneK
        :param numGMRPoints: number of data points composing the expected curves to be computed by GMR

        :return expData: expected curve obtained by modelling the given dataset with the GMM+GMR procedure
        :return expSigma: associated covariance matrices obtained by modelling the given dataset with the GMM+GMR procedure
        """

        # PARAMETERS OF THE GMM+GMR PROCEDURE
        numVar = 4;            # number of variables in the system (time & 3 accelerations)
        m,numData = set_.shape;# number of points in the dataset

        priors, mu, sigma = self.runGMM(set_,K)

        #APPLY GAUSSIAN MIXTURE REGRESSION TO FIND THE EXPECTED CURVE
        #define the points to be used for the regression
        #(assumption: CONSTANT SPACING)

        expData1 = np.linspace(1,numGMRPoints+1, num=numGMRPoints+1);
        expMeans, expSigma =  self.RetrieveModel(K,priors,mu,sigma,expData1,0,np.arange(1,numVar),numVar)
        return expMeans.transpose(), expSigma



    def RetrieveModel(self,K,priors,mu,sigma,points,in_,out,numVar):
        """ Performs Gaussian Mixture Regression (GMR) over the GM model defined by its parameters. By providing temporal values as inputs, it returns a smooth generalized version of the data encoded in the GMM and the associated constraints expressed by the covariance matrices.

            :param K: number of clusters
            :param priors: apriori probavbility
            :param mu: mean
            :param sigma: covariance
            :param points: input data (starting points to be used for GMR)
            :param in: input dimension
            :param out: output dimension
            :param numVar: axis number, ex: if we use x,y,z then this parameters must be = 3

            :return expMeans: set of expected means for the given GM model
            :return expSigma: covariance matrices of the expected points in expMeans
        """
        numData = size(points)
        pdf_point = zeros((numData,K))
        beta = zeros((numData,K))
        exp_point_k = zeros((numVar-1,numData,K))
        exp_sigma_k = {}

        for i in range(K):
            # compute the probability of each point to belong to the actual GM
            # model (probability density function of the point) --> p(point)
            pdf_point_temp = multivariate_normal.pdf(points,mu[i,in_],sigma[i,in_,in_])

            #compute p(Gaussians) * p(point|Gaussians)
            pdf_point[:,i] = priors[i]* pdf_point_temp

        #estimate the parameters beta
        for i in range(K):
            beta[:,i] = pdf_point[:,i]/sum(pdf_point,1)


        for j in range (K):
            temp = (ones((numData,1))*mu[j,out]).transpose()+(ones((1,numVar-1))*(sigma[j,out,in_]*1/(sigma[j,in_,in_]))).transpose()*(points-tile(mu[j,in_],[1,numData]))
            exp_point_k[:,:,j] = temp

        beta_tmp = reshape(beta,(1,numData,K))
        #print tile(beta_tmp,[size(out),1,1]).shape
        exp_point_k2 = tile(beta_tmp,[size(out),1,1])*exp_point_k;
        #compute the set of expected means
        expMeans = sum(exp_point_k2,2)

        for j in range (K):
            temp = sigma[j,1:numVar,1:numVar] -(ones((1,numVar-1))*(sigma[j,out,in_]*1/(sigma[j,in_,in_]))).transpose()*sigma[j,in_,out]
            exp_sigma_k[j] = temp


        expSigma_temp = {}
        for i in range (numData):
            expSigma_temp[i] =  zeros((numVar-1,numVar-1))
            for j in range (K):
                        expSigma_temp[i] = expSigma_temp[i] + beta[i,j]* beta[i,j]*exp_sigma_k[j]

        expSigma = expSigma_temp[0]
        for i in range (1,numData):
            expSigma = concatenate((expSigma, expSigma_temp[i]), axis=0)

        return expMeans, expSigma

if __name__ == "__main__":
    import doctest
    doctest.testmod()

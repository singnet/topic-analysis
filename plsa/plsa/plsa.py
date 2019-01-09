# Copyright (C) 2010 Mathieu Blondel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Implementation of probabilistic Latent Semantic Analysis/Indexing as described
in

"Probabilistic Latent Semantic Indexing", Hofmann, SIGIR99

Notation:

    w: word
    d: document
    z: topic

    V: vocabulary size
    D: number of documents
    Z: number of topics

"""

import psutil
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import pandas as pd
import inspect
# import _plsa


# beta2 = 0.75
beta2 = 1
# HAVE_EXT = True
HAVE_EXT = True
min_iteration2 = 10 # 10 was the previous value
init_with_seed = False




frame = inspect.stack()[1]
file_name = str(inspect.getfile((frame[0])))


logL_pic = ''


try:
    import _plsa
    if HAVE_EXT == True:
        print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx. There is _plsa')
    else:
        HAVE_EXT = False
        print ('^^^^^^^^^^^^^^^^^^^^^^^^^^^. No _plsa')
except:
    HAVE_EXT = False
    print ('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&. No _plsa')

# print 'HAVE_EXT =',HAVE_EXT


def normalize_1d(a, out=None):
    if out is None: out = np.empty_like(a)
    s = np.sum(a)
    if s != 0.0 and len(a) != 1:
        np.divide(a, s, out)
    return out

def normalize(M, axis=0, out=None):
    if len(M.shape) == 1: return normalize_1d(M, out)
    if out is None: out = np.empty_like(M)
    if axis == 0:
        M = M.T #M.swapaxes(0,1)
        out = out.T

    for i in range(len(M)):
        normalize_1d(M[i], out[i])

    if axis == 0: out = out.T

    return out

def loglikelihood(td, p_z, p_w_z, p_d_z):
    """
    Compute the log-likelihood that the model generated the data.
    """
    V, D = td.shape
    L = 0.0
    for w,d in zip(*td.nonzero()):
        # p_d_w = np.sum(p_z * p_w_z[w,:] * p_d_z[d,:])
        p_d_w = np.sum(p_z * p_w_z[w,:] * p_d_z[d,:]/(np.sum(p_z*p_d_z[d,:])))
        if p_d_w > 0: L += td[w,d] * np.log(p_d_w)
    return L

def train(td,
          p_z, p_w_z, p_d_z,
          p_z_old, p_w_z_old, p_d_z_old,
          maxiter, eps,
          folding_in, debug,logL_c):

    logL = []

    R = td.sum() # total number of word counts

    lik = loglikelihood(td, p_z, p_w_z, p_d_z)
    logL.append(lik)
    print ('Starting logL =',lik)
    # beta2 = 1
    for iteration in range(1, maxiter+1):
        # Swap old and new
        p_d_z_old, p_d_z = (p_d_z, p_d_z_old)
        p_w_z_old, p_w_z = (p_w_z, p_w_z_old)
        p_z_old, p_z = (p_z, p_z_old)

        # Set to 0.0 without memory allocation
        p_d_z *= 0.0
        if not folding_in:
            p_w_z *= 0.0
            p_z *= 0.0

        if (beta2 != 1):
            print ('tempering started')
            p_z_old = np.power(p_z_old, beta2)
            # print('Finished','p_z_old')
            # beta2 = 1
            p_d_z_old = np.power(p_d_z_old, beta2)
            # print('Finished','p_d_z_old')
            p_w_z_old = np.power(p_w_z_old, beta2)
            # print('Finished','p_w_z_old')
            print ('tempering finished')


        for w,d in zip(*td.nonzero()):
            # E-step
            # beta2 = 0.75

            p_z_d_w = p_z_old * p_d_z_old[d, :] * p_w_z_old[w, :]

            # if (beta2 ==1):
            #     p_z_d_w = p_z_old * p_d_z_old[d,:] * p_w_z_old[w,:]
            # else:
            #     p_z_old_beta2 = np.power(p_z_old,beta2)
            #     # print('Finished','p_z_old_beta2')
            #     # beta2 = 1
            #     p_d_z_old_beta2 = np.power(p_d_z_old,beta2)
            #     # print('Finished','p_d_z_old_beta2')
            #     p_w_z_old_beta2 = np.power(p_w_z_old,beta2)
            #     # print('Finished','p_w_z_old_beta2')
            #     p_z_d_w = p_z_old_beta2 * p_d_z_old_beta2[d,:] * p_w_z_old_beta2[w,:]
            #     # print('Finished','p_z_d_w')
                

            normalize(p_z_d_w, out=p_z_d_w)
            # print('Finished normalizing')



            # M-step
            s = td[w,d] *  p_z_d_w
            p_d_z[d,:] += s

            if not folding_in:
                p_w_z[w,:] += s
                p_z += s

        # normalize
        normalize(p_d_z, axis=0, out=p_d_z)

        if not folding_in:
            normalize(p_w_z, axis=0, out=p_w_z)
            p_z /= R

        lik_new = loglikelihood(td, p_z, p_w_z, p_d_z)
        logL.append(lik_new)
        # lik_diff = lik_new - lik
        lik_diff = -(lik_new - lik)*100/lik
        # assert(lik_diff >= -1e-10)
        lik = lik_new


        if debug:
            print ("Iteration", iteration)

            # I commented this out to save computational time
            # print "Parameter change"
            # pz=np.abs(p_z - p_z_old).sum()
            # pwz=np.abs(p_w_z - p_w_z_old).sum()
            # pdz=np.abs(p_d_z - p_d_z_old).sum()
            # p_z_d= pz*p_d_z
            # print "P(z): ",pz
            # print "P(w|z): ",pwz
            # print "P(d|z): ",pdz
            # print "P(z,d):" , p_z_d
            #
            # print "L += %f" % lik_diff
            # print "Lik_new",lik
            print ("lik_diff =",lik_diff,'%')


        if iteration > min_iteration2 and lik_diff < eps :
            print ("No more progress, stopping EM at iteration", iteration)
            print ("LogL =", logL)
            axis1 = range(1,len(logL)+1)
            plt.plot(axis1, logL)
            plt.savefig(logL_pic)
            break



    # print 'p_z-----'
    # print p_z

    # ddf=pd.read_csv('/xxx/topic-by-Document.csv')
    # ddf = ddf.set_index('Unnamed: 0')
    # print ddf
    # for i in ddf.index:
    #     for j in ddf.columns:
    #          ddf.loc[i,j]=p_d_z.T[i,j]




# def power

class pLSA(object):

    def __init__(self, model=None):
        """
        model: a model, as returned by get_model() or train().
        """
        self.p_z = None
        self.p_w_z = None
        self.p_d_z = None
        self.p_z_d= None
        if model is not None: self.set_model(model)
        self.debug = False
        self.logL_c = np.zeros(503)
        self.logL_pic = ''

    def random_init(self, Z, V, D):
        """
        Z: the number of topics desired.
        V: vocabulary size.
        D: number of documents.
        """
        if init_with_seed:
            np.random.seed(0) # uncomment for deterministic init
        if self.p_z is None:
            self.p_z = normalize(np.random.random(Z))
            print(self.p_z)
            np.savetxt("pz.csv", self.p_z, delimiter=",")
        if self.p_w_z is None:
            self.p_w_z = normalize(np.random.random((V,Z)), axis=0)
            np.savetxt("pwz.csv", self.p_w_z, delimiter=",")
        if self.p_d_z is None:
            self.p_d_z = normalize(np.random.random((D,Z)), axis=0)
            np.savetxt("pdz.csv", self.p_d_z, delimiter=",")


    def train(self, td, Z, maxiter=500, eps=0.01, folding_in=False,beta=beta2,min_iteration = min_iteration2): # eps=0.01 is default value
        """
        Train the model.

        td: a V x D term-document matrix of term-counts.
        Z: number of topics desired.

        td can be dense or sparse (dok_matrix recommended).
        """
        V, D = td.shape

        self.random_init(Z, V, D)

        p_d_z_old = np.zeros_like(self.p_d_z)
        p_w_z_old = np.zeros_like(self.p_w_z)
        p_z_old = np.zeros_like(self.p_z)

        train_func = _plsa.train if HAVE_EXT else train
        print('RRRRRRRRRRRRRRRAM used just before training:', float(list(psutil.virtual_memory())[3]) / 1073741824.0, 'GB')
        train_func(td.astype(np.uint32),
                   self.p_z, self.p_w_z, self.p_d_z,
                   p_z_old, p_w_z_old, p_d_z_old,
                   maxiter, eps,beta,min_iteration,
                   folding_in, self.debug,self.logL_c)

        # self.P_D_Z = self.p_d_z
        # self.P_Z = self.p_z

        # print 'here????????????????????????????'

        if (HAVE_EXT == True):
            bound_logL = list(self.logL_c).index(0)
            logL_c_list = list(self.logL_c[:bound_logL])
            print ('logL =',logL_c_list)
            axis1 = range(1, logL_c_list.__len__() + 1)
            plt.clf()
            plt.plot(axis1, logL_c_list)
            # print('logL_pic=',self.logL_pic)
            plt.savefig(self.logL_pic)

        return self.get_model()

    def average_train(self, N):
        """
        Return a function compatible with train.
        This function executes the training N times and takes the average.
        """
        assert(N >= 1)

        def _wrap(*args, **kw):
            print ("pLSA 1")
            model = list(pLSA().train(*args, **kw))

            for i in range(1,N):
                print ("pLSA", i+1)
                model2 = pLSA().train(*args, **kw)
                for j in range(len(model)):
                    model[j] += model2[j]

            normalize(model[0], out=model[0])
            normalize(model[1], axis=0, out=model[1])
            normalize(model[2], axis=0, out=model[2])

            self.set_model(tuple(model))

            return self.get_model()

        return _wrap
    def topic_document(self):
        '''
        Compute the probabilities of topics belonging to document
        Retrun: P(z,d)
        '''
        self.p_z_d= self.p_z*self.p_d_z
        # print 'p_z_d-----'
        # print (self.p_z_d.shape)
        # print 'p_z_d.T-----'
        # print (self.p_z_d.T.shape)


        return self.p_z_d.T  # T is for transpose


    def document_topics(self):
        """
        Compute the probabilities of documents belonging to topics.

        Return: a Z x D matrix of P(z|d) probabilities.

        Note: This can be seen as a dimensionality reduction since a Z x D
        matrix is obtained from a V x D matrix, where Z << V.
        """
        return normalize((self.p_d_z * self.p_z[np.newaxis,:]).T, axis=0)

    def document_cluster(self):
        """
        Find the main topic (cluster) of documents.

        Return: a D-array of cluster indices.
        """
        return self.document_topics().argmax(axis=0)

    def word_topics(self):
        """
        Compute the probabilities of words belonging to topics.

        Return: a Z x V matrix of P(z|w) probabilities.
        """
        return normalize((self.p_w_z * self.p_z[np.newaxis,:]).T, axis=0)

    def word_cluster(self):
        """
        Find the main topic (cluster) of words.

        Return: a D-array of cluster indices.
        """
        return self.word_topics().argmax(axis=0)

    def topic_labels(self, inv_vocab, N=10):
        """
        For each topic z, find the N words w with highest probability P(w|z).

        inv_vocab: a term-index => term-string dictionary

        Return: Z lists of N words.
        """
        Z = len(self.p_z)
        ret = []
        for z in range(Z):
            ind = np.argsort(self.p_w_z[:,z])[-N:][::-1]
            ret.append([inv_vocab[i] for i in ind])
        return ret

    def unigram_smoothing(self):
        """
        Compute the smoothed probability P(w|d) by "back-projecting" the
        features from the latent space to the original space.

        Return: a V x D matrix of smoothed P(w|d) probabilities.
        """
        V, Z = self.p_w_z.shape
        D, Z = self.p_d_z.shape
        p_w_d = np.zeros((V,D), dtype=np.double)
        for d in range(D):
            for w in range(V):
                p_w_d[w,d] = np.sum(self.p_w_z[w,:] * self.p_d_z[d,:])
        return p_w_d

    def folding_in(self, d, maxiter=50, eps=0.01):
        """
        Compute the probabilities of a new document d belonging to topics.

        d: a V-array of term-counts.

        Return: a Z-array of P(z|d) probabilities.
        """
        V = d.shape[0]
        Z = len(self.p_z)
        plsa = pLSA()
        plsa.debug = self.debug
        plsa.p_z = self.p_z
        plsa.p_w_z = self.p_w_z
        plsa.p_z_d= self.p_z_d
        plsa.train(d[:,np.newaxis], Z, maxiter, eps, folding_in=True)
        return normalize(self.p_z * plsa.p_d_z[:,0])

    def global_weights(self, gw):
        """
        Compute global weight vector in latent space.

        gw: a V-array of global weights (e.g., idf).

        Return: a Z-array of global weights.
        """
        return np.sum(gw[:,np.newaxis] * self.p_w_z, axis=0)

    def get_model(self):
        return (self.p_z, self.p_w_z, self.p_d_z, self.p_z_d)

    def set_model(self, model):
        self.p_z, self.p_w_z, self.p_d_z,self.p_z_d = model

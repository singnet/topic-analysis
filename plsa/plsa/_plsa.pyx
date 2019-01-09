import numpy as np
cimport numpy as np

cdef extern void _train(unsigned int n_ele,
                        unsigned int n_z,
                        unsigned int n_w,
                        unsigned int n_d,
                        unsigned int *tdnz,
                        double *p_z,
                        double *p_w_z,
                        double *p_d_z,
                        double *p_z_old,
                        double *p_w_z_old,
                        double *p_d_z_old,
                        unsigned int maxiter,
                        double eps,
                        double beta,
                        unsigned int min_iteration,
                        unsigned int folding_in,
                        unsigned int debug,
                        double *logL_c)

def nonzero(td):
    """
    Convert a sparse matrix td to a Nx3 matrix where N is the number of non-zero
    elements. The 1st column is the word count, the 2nd is the word index
    and the 3rd column is the document index.
    """
    rows, cols = td.nonzero()
    vals = td[rows,cols]
    if "scipy.sparse" in str(vals.__class__): vals = vals.toarray()
    return np.asfortranarray(np.vstack((vals, rows, cols)).T)

def train(td,
          np.ndarray[np.float64_t, ndim=1, mode='c']p_z,
          np.ndarray[np.float64_t, ndim=2, mode='c']p_w_z,
          np.ndarray[np.float64_t, ndim=2, mode='c']p_d_z,
          np.ndarray[np.float64_t, ndim=1, mode='c']p_z_old,
          np.ndarray[np.float64_t, ndim=2, mode='c']p_w_z_old,
          np.ndarray[np.float64_t, ndim=2, mode='c']p_d_z_old,
          maxiter,
          eps,
          beta,
          min_iteration,
          folding_in,
          debug,
          np.ndarray[np.float64_t, ndim=1, mode='c']logL_c):

    cdef np.ndarray[np.uint32_t, ndim=2, mode='fortran'] tdnz

    tdnz = nonzero(td).astype(np.uint32)

    _train(<unsigned int>tdnz.shape[0],
           <unsigned int>p_z.shape[0],
           <unsigned int>p_w_z.shape[0],
           <unsigned int>p_d_z.shape[0],
           <unsigned int *>tdnz.data,
           <double *>p_z.data,
           <double *>p_w_z.data,
           <double *>p_d_z.data,
           <double *>p_z_old.data,
           <double *>p_w_z_old.data,
           <double *>p_d_z_old.data,
           <unsigned int>maxiter,
           <double> eps,
           <double> beta,
           <unsigned int> min_iteration,
           <unsigned int>folding_in,
           <unsigned int>debug,
           <double *>logL_c.data)



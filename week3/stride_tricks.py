# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Get our pylab mise en place going
import numpy as np
import matplotlib.pyplot as plt

# <codecell>

# I'll make up a time series of sequential data
# 
x = np.arange(8 * 16)

# And print it
print x

# <markdowncell>

# Let's say `x` holds sequential data, and we want to do some sliding window analysis.  This is common in time series modeling and signal processing.
# 
# If the windows are disjoint (i.e., no overlap) then we can get away with simply reshaping `x` into a matrix like so:

# <codecell>

frame_length = 8

x_framed = np.reshape(x, (-1, frame_length))

print x_framed

# <markdowncell>

# In the above example, `x_framed[i]` is a single window's worth of data.
# 
# But what if we want the windows to overlap?  Reshaping will not work, since we need multiple copies of most entries in the matrix.
# 
# The simple thing to do is allocate a new array, and iteratively populate each row with a properly advanced window, like so:

# <codecell>

hop_length = frame_length / 2

num_frames = 1 + (len(x) - frame_length) / hop_length

x_framed_overlap = np.zeros( (num_frames, frame_length), dtype=int )

for t in range(num_frames):
    x_framed_overlap[t, :] = x[t*hop_length:t*hop_length + frame_length]
    
print x_framed_overlap

# <markdowncell>

# What's wrong with this?  A few of things:
# 
# - It's *slow*, and requires lots of memory copies
# - The new array is much larger than the original time series
# - The smaller `hop_length` gets, the bigger the memory usage!
# 
# If we only need read-only access to the data, then this is a lot of overhead.
# 
# Of course, we could just use direct indexing, e.g., ``x[t * hop_length : t * hop_length + frame_length]``, but that gets ugly quickly.

# <markdowncell>

# ### Stride tricks
# 
# All we really want is a clear way to index windowed samples from `x` without incurring a lot of computational overhead.  
# 
# NumPy's *stride tricks* submodule provides exactly this.  We'll need to know a little about how numpy arrays are organized though.
# 
# An `ndarray` contains numerical data of some type, say `int8` or `float64`, and this `dtype` determines how many bytes in ram each entry occupies.  
# 
# Although `ndarray`s expose multi-dimensional indexing, their contents are actually stored in a linear index.  The default ordering of the dimensions is row-major (`order='C'`, as in *The C Programming Language*) or column-major (`order='F'`, as in *Fortran*).  Yes, it's confusing.
# 
# A two-dimensional row-major array `a` will be organized as follows:
# 
#   - `a[0, 0], a[0, 1], a[0, 2], ... a[0, n], a[1, 0], a[1, 1], a[1, 2], ...`
#   
# while a column-major array will look like
# 
#   - `a[0, 0], a[1, 0], a[2, 0], ... a[m, 0], a[0, 1], a[1, 1], a[2, 1], ...`
#   
# ### Why does this matter?
# 
# When you index an `ndarray` in python, say `M[i, j]`, it needs to translate the two-dimensional index `(i, j)` into a linear index:
# 
#   - `i * row_stride + j * column_stride`
#   
# So column- or row-major array indexing is merely an issue of setting up the strides appropriately.  Of course, this idea generalizes to `n` dimensional arrays by tacking on more indices and strides.
# 
# We're going to use stride tricks to fool numpy into thinking it has much more data than it actually does, while keeping the same underlying data in place.  How?  By manually setting the row and column strides!
# 
# The key idea here is that a row stride need not span the full shape of the array.
# 
# ### WARNING
# 
# Stride tricks can be dangerous.  Because we're digging into the guts of ndarrays, it's possible to violate memory protection if we're not careful.  
# 
# Ok, you've been warned.

# <codecell>

from numpy.lib import stride_tricks

# <codecell>

# Ok, it's a linear index, so it's both F- and C-contiguous
# Next, let's see how big each item in x is.  This is provided by the `itemsize` field
print x.itemsize, x.dtype

# <codecell>

# Now, we're ready to set up our fake frmaed data

# Each row advances by `hop_length` entries, times the number of bytes in each entry
row_stride = x.itemsize * hop_length

# Columns are still contiguous, and only advance by one entry
col_stride = x.itemsize

# as_strided will construct a new view of the data in x, using the shape and stride parameters we supply
x_framed_strided = stride_tricks.as_strided(x, 
                                            shape=(num_frames, frame_length), 
                                            strides=(row_stride, col_stride))

print x_framed_strided

# <codecell>

# What if we want our frames vertical instead?  Just swap the row and column strides

x_framed_strided_column = stride_tricks.as_strided(x, 
                                            shape=(num_frames, frame_length), 
                                            strides=(col_stride, row_stride))

print x_framed_strided_column


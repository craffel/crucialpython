# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import Image 
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600) 

# <codecell>

# Crucial imports
import numpy as np
import matplotlib.pyplot as plt

# <codecell>

# Let's say we have a (near) periodic signal
x = np.sin(np.arange(128))
plt.plot(x)

# <markdowncell>

# To analyze time-varying content, we want to process individual overlapping frames.
# 
# We can use the stride_tricks from last week to get overlapped windows on a linear vector 
# 
# (from  http://nbviewer.ipython.org/github/craffel/crucialpython/blob/master/week3/stride_tricks.ipynb )

# <codecell>

# Build a "framed" version of x as successive, overlapped sequences
# of frame_length points
from numpy.lib import stride_tricks
frame_length = 16
hop_length = 4
num_frames = 1 + (len(x) - frame_length) / hop_length
row_stride = x.itemsize * hop_length
col_stride = x.itemsize
x_framed = stride_tricks.as_strided(x, 
                                    shape=(num_frames, frame_length), 
                                    strides=(row_stride, col_stride))
plt.imshow(x_framed, interpolation='nearest', cmap='gray')

# <codecell>

# If we take the FFT of each row, we can see the short-time fourier transform
plt.imshow(np.abs(np.fft.rfft(x_framed)), interpolation='nearest')

# <codecell>

# Although there's a steady sinusoidal component, we see interference between the 
# window frame and the signal phase.  We need a tapered window applied to each frame.
window = np.hanning(frame_length)
plt.plot(window)

# <codecell>

# But what's the best way to multiply each frame of x_framed by window?
# Linear algebra way is to multiply by a diagonal matrix
diag_window = np.diag(window)
plt.imshow(diag_window, interpolation='nearest', cmap='gray')

# <codecell>

# Now apply it to each frame using matrix multiplication
x_framed_windowed = np.dot(x_framed, diag_window)
plt.imshow(x_framed_windowed, interpolation='nearest', cmap='gray')

# <codecell>

# Matlab way is to construct a matrix of repeating rows of the same size
window_repeated = np.tile(window, (num_frames,1))
plt.imshow(window_repeated, interpolation='nearest', cmap='gray')
# then pointwise multiplication applies it to each row
x_framed_windowed = x_framed * window_repeated

# <codecell>

# Numpy broadcasting implicitly (and efficiently) repeats singleton or missing dimensions
# to make matrices the same size, so tiling is unneeded
plt.imshow(x_framed*window, interpolation='nearest', cmap='gray')

# <codecell>

# Compare the timings:
%timeit np.dot(x_framed, np.diag(window))
%timeit x_framed*np.tile(window, (num_frames,1))
%timeit x_framed*window
# The big win is not having to allocate the second num_frames x frame_length array

# <codecell>

# What about if we had our data in columns?
x_framed_T = x_framed.T
plt.imshow(x_framed_T * window, interpolation='nearest', cmap='gray')

# <codecell>

# Broadcast works by starting at the last dimensions (the fastest-changing ones in 'C' ordering) 
# and promoting either one if it's one.  
# So we just have to make our window be frame_length x 1
# We can do this with slicing and np.newaxis:
plt.imshow(x_framed_T * window[:,np.newaxis], interpolation='nearest', cmap='gray')
# Now broadcasting works again

# <codecell>

# Broadcasting works across multiple dimensions.  
# It goes through each dimension from the last, looking for a match 
# or promoting singletons
a = np.random.rand( 3, 4, 5 )
b = np.random.rand( 3, 5 )
c = a*b

# <codecell>

# That didn't work because there was no singleton dimension to promote
# so we can introduce one, with reshape for instance:
b2 = np.reshape(b, (3, 1, 5))
c1 = a*b2
# or using slicing
c2 = a * b[:, np.newaxis, :]
print np.allclose(c1, c2)

# <markdowncell>

# For the full description of how broadcasting works, see the SciPy documentation:
# http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html

# <codecell>

# Remember why we wanted the windowing, to remove artefacts from the STFT?
plt.subplot(121)
plt.imshow(np.abs(np.fft.rfft(x_framed)), interpolation='nearest')
plt.subplot(122)
plt.imshow(np.abs(np.fft.rfft(x_framed * window)), interpolation='nearest')
# Windowing drastically reduces framing-related artefacts 
# (at the cost of a little frequency resolution)

# <codecell>



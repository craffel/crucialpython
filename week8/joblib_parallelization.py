# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CRÜCIAL PYTHON Week 8: Easy parallelization with joblib

# <codecell>

from IPython.core.display import Image
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600)

# <markdowncell>

# ## What is joblib?
# joblib is a python module which includes functionality for doing various useful tasks, like caching the output of functions given certain input, logging/tracing, and easy parallelization.  Today, we'll focus on the latter, which essentially is a wrapper around Python's built-in `multiprocessing` module.  It's essentially just an extremely easy way to write a parallelized `for` loop.

# <markdowncell>

# ## joblib.Parallel and joblib.delayed
# Two write a simple parallelized `for` loop using joblib, you need to use the `Parallel` class and the `delayed` function.  Together, they form a construct which looks a lot like list comprehension.  `delayed` is a [decorator](http://nbviewer.ipython.org/github/craffel/crucialpython/blob/master/week7/decorators.ipynbdecorator) which simply returns the function, its arguments, and its keyword arguments as a tuple.  `Parallel` constructs a class which can be called with a list of tuples, where each tuple includes a function and its arguments.  It subsequently calls each function from each tuple with the corresponding arguments.  But, what you really need to know in practice is simple:

# <codecell>

from joblib import Parallel, delayed
import numpy as np
print [np.power(i, 2) for i in xrange(10)]
print Parallel()(delayed(np.power)(i, 2) for i in xrange(10))

# <codecell>

# To parallelize, simply set the n_jobs argument!
Parallel(n_jobs=8)(delayed(np.power)(i, 2) for i in xrange(10))

# <markdowncell>

# ## Practical example
# `np.power` is not a function you'd need to parallelize calls to in general, because it's so fast and the overhead for parallelization makes it not worth while (we'll get to that later).  Here's a function which actually takes a while to compute:

# <codecell>

def convolve_random(size):
    ''' Convolve two random arrays of length "size" '''
    return np.convolve(np.random.random_sample(size), np.random.random_sample(size))

# <codecell>

# Time to run once with length-40000 arrays
%timeit convolve_random(40000)

# <codecell>

# Time to run sequentially for length 40000, 41000, 42000, ... 47000 arrays
%timeit [convolve_random(40000 + i*1000) for i in xrange(8)]
# In parallel, with 8 jobs
%timeit Parallel(n_jobs=8)(delayed(convolve_random)(40000 + i*1000) for i in xrange(8))

# <markdowncell>

# ## Other useful features of Parallel
# The `Parallel` class is meant to be more convenient to use than `multiprocessing`.  As such, it can dump out progress messages, cleanly report errors, and be interrupted with ctrl-C, all of which takes some effort to do in `multiprocessing`.

# <codecell>

# Use the verbose argument to display progress messages.
# The frequency of the messages increases with the verbosity level. 
result = Parallel(n_jobs=8, verbose=50)(delayed(convolve_random)(40000 + i*1000) for i in xrange(16))

# <markdowncell>

# ## When should you use Parallel?
# The easiest case (and the only case we'll cover here) is when you want to run the same process many times with different arguments, where each run of the process does not depend on any other runs.  This is the intended use of `joblib.Parallel`.
# 
# Furthermore, as mentioned above, there's some overhead to using parallelization in general.  As a simple rule, for very fast functions, it's not worth it, and for very slow functions, you'll get a speedup which levels off as you approach the number of cores you have.  The following code seeks to test this in a principled way using our `convolve_random` function.

# <codecell>

# Try convolution sizes [5000, 10000, 15000 ... 50000]
sizes = 5000*(1 + np.arange(10))
# Try n_jobs from [1, ..., max_jobs]
max_jobs = 8
n_jobs_values = 1 + np.arange(max_jobs)

# <codecell>

import time
# Store the timing for each setting
times = np.zeros((n_jobs_values.shape[0], sizes.shape[0]))
for n, n_jobs in enumerate(n_jobs_values):
    for m, size in enumerate(sizes):
        start = time.time()
        result = Parallel(n_jobs=n_jobs)(delayed(convolve_random)(size) for i in xrange(max_jobs))
        # Compute and store elapsed time
        times[n, m] = time.time() - start
# Save it out so we don't have to run it twice
np.savetxt('times.txt', times)

# <codecell>

import matplotlib.pyplot as plt
# Load in our pre-computed times
times = np.genfromtxt('times.txt')

# <codecell>

plt.figure(figsize=(10, 6))
for size_index in xrange(4):
    plt.subplot(2, 2, size_index + 1)
    # Plot the times for this size by n_jobs
    plt.plot(n_jobs_values, times[:, size_index], '.')
    # Set up axes and labels
    plt.xticks(n_jobs_values)
    plt.xlim([.8, max_jobs + .2])
    plt.title('Size = {}'.format(sizes[size_index]))
    plt.xlabel('n_jobs')
    plt.ylabel('Time (s)')
plt.tight_layout()

# <codecell>

plt.figure(figsize=(10, 6))
# Need as many colors as max_jobs!
colors = ['r', 'k', 'Purple', 'IndianRed', 'Chartreuse', 'DarkRed',  'Teal', 'b']
ax = plt.gca().set_color_cycle(colors)
# Plot each n_jobs setting as a different line
for job_results in times:
    plt.plot(sizes, job_results)
# Set up labels and legend
plt.xlabel('Convolution size')
plt.ylabel('Time (s)')
plt.legend(n_jobs_values, 'upper left', title='n_jobs')


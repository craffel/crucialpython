# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CRÜCIAL PŸTHON Week 5: Outers

# <codecell>

%pylab inline

# We'll be using some pretty-printing later on
from pprint import pprint

# <codecell>

from IPython.core.display import Image 
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600) 

# <markdowncell>

# ### Cast ye out, tight loops!
# 
# High-level programs sometimes have computational bottleneck at a tight loop, or even nested loops.  This comes up frequently when comparing two sets of objects, say to build a similarity matrix or do collision detection.
# 
# A common way to eliminate these bottlenecks is to implement the critical portion in a low-level language, such as C, so that the python interpreter doesn't have to work as hard.  Today we'll look at NumPy's `outer` functionality, which when used correctly, can replace many tight-loop patterns that occur in practice.
# 
# ## Example: point range search
# 
# Say we have two lists of numbers `a` and `b`, and we wish to find all the pairs `a[i], b[j]` such that `a[i]` is within some distance `r` of `b[i]`.  That is, find all $i$ and $j$ such that
# 
# $$
#     |a_i - b_i| \leq r
# $$
# 
# This can be done trivially by nested iteration, as seen below.

# <codecell>

# Let's make a function to generate some example data
def make_point_data(n, m):
    a = np.arange(-n/2.0, 1 + n / 2.0)
    b = np.random.randn(m)

    # For convenience, let's sort b
    b = np.sort(b)

    return a, b

# <codecell>

# Build a list and iterate over all pairs
def find_similar_points(a, b, r):
    '''Given two lists of numbers a and b, and a threshold r,
       returns a matrix `hits` such that:
       
       |a[ hits[i, 0] ] - b[ hits[j, 1] ]| <= r
       
    '''
    
    hits = []
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if np.abs(ai - bj) <= r:
                hits.append( (i, j) )
                
    # Return indices in ndarray format
    return np.asarray(hits)

# <codecell>

# Generate and display the example data
a, b = make_point_data(5, 10)
# And a threshold
r = 0.25

print 'a: ', a
print 'b: ', b
print 'r: ', r

# <codecell>

# What'd we get?
print 'Hits: '
print find_similar_points(a, b, r)

# <markdowncell>

# ---
# 
# # Example 2: interval intersection
# Let's consider a slightly more involved example.  Say we have a set of real line intervals $\{(s_i, t_i)\}$ where each ordered pair denotes the start and end of the interval.
# 
# One quantity of interest is the length of intersection between any two intervals:
# 
# $$
#     c(i, j) = |(s_i, t_i) \cap (s_j, t_j)| = \max\left(0, \min(t_i, t_j) - \max(s_i, s_j) \right)
# $$
# 
# Again, this can be computed by nested iteration, as seen below.

# <codecell>

def make_interval_data(n):
    # Generate random start times
    S = np.random.randn(n)
    
    # Sort it, for convenience
    S = np.sort(S)

    # Add a random positive length to each one
    T = S + np.abs(np.random.randn(n))
    
    return S, T

# <codecell>

def find_interval_overlap(S, T):
    '''S and T are vectors that encode intervals (S[i], T[i])
    
    Returns an n-by-n matrix C such that C[i, j] is the length of the overlap between intervals i and j.
    '''
    
    # Get the shape
    n = S.shape[0]
    
    # Build an output matrix.
    C = np.zeros( (n, n) )
    
    for i in range(n):
        for j in range(n):
            C[i, j] = max(0, min(T[i], T[j]) - max(S[i], S[j]))
            
    return C

# <codecell>

# Let's make up some test data
S, T = make_interval_data(5)

# What does it look like?
pprint( zip(S, T) )

# <codecell>

print find_interval_overlap(S, T)

# <markdowncell>

# ---
# In both of the examples above, we're doing an all-pairs comparison between two sets of objects.
# 
# While conceptually simple, the nested iteration approach leads to somewhat cumbersome code, which can also be computationally inefficient.
# 
# Fortunately, NumPy provides some tools to help us simplify and vectorize this kind of pairwise operation.  The secret ingredient is called [`outer`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ufunc.outer.html#numpy.ufunc.outer), and is a property of NumPy's unversal function [ufunc](http://docs.scipy.org/doc/numpy/reference/ufuncs.html) abstraction.
# 
# Quoth the manual,
# 
# > Universal functions (ufunc)
# >
# > A universal function (or ufunc for short) is a function that operates on ndarrays in an element-by-element fashion, supporting array  broadcasting, type casting, and several other standard features. That is, a ufunc is a “vectorized” wrapper for a function that takes a fixed number of scalar inputs and produces a fixed number of scalar outputs.
# 
# A ufunc `f(a, b)` implement the `outer` method, which returns a matrix `X[i, j] = f(a[i], b[j])`.  The benefit of this approach is that ufuncs are typically implemented in C, and are often much more efficient in practice than implementing the equivalent loop in python.
# 
# Some examples of potentially interesting ufuncs include:
# 
#   * add, subtract
#   * multiply, divide
#   * less, less_equal
#   * bitwise_and, bitwise_or,
#   * etc.
# 
# A list of [available ufuncs](http://docs.scipy.org/doc/numpy/reference/ufuncs.html#available-ufuncs) can be found in the `numpy` documentation.
# 
# ---

# <codecell>

# Here's how to write our similar_points function using the subtraction ufunc
def fast_similar_points(a, b, r):
    
    # subtract.outer builds a matrix of a[i] - b[j]
    # abs computes the absolute value
    difference = np.abs(np.subtract.outer(a, b))
    
    # <= r does a pointwise comparison against the threshold
    # argwhere finds all indices (i, j) such that hits[i, j] == True
    return np.argwhere(difference <= r)

# <codecell>

# Make some more test data, 5 points in a and 10 in b
a, b = make_point_data(5, 10)

# <codecell>

print a
print b
print r

# <codecell>

# For comparison purposes, our previous implementation
print find_similar_points(a, b, r)

# <codecell>

# And the new one
print fast_similar_points(a, b, r)

# <codecell>

# Timing benchmark
%timeit find_similar_points(a, b, r)

# <codecell>

%timeit fast_similar_points(a, b, r)

# <codecell>

# How does it scale? Let's increase the size of our data
a, b = make_point_data(500, 1000)

# <codecell>

%timeit find_similar_points(a, b, r)

# <codecell>

%timeit fast_similar_points(a, b, r)

# <codecell>

# Similarly, our interval-overlap calculator can be simplified by using outers to compute the intermediate steps
def fast_interval_overlap(S, T):
    
    # For each pair of intervals, find the later start: max(S[i], S[j])
    max_start = np.maximum.outer(S, S)
    
    # And the earlier end: min(T[i], T[j])
    min_end   = np.minimum.outer(T, T)
    
    # Subtract min_end[i, j] - max_start[i, j]
    # If the result is negative, then the intersection is 0
    return np.maximum(0, min_end - max_start)

# <codecell>

S, T = make_interval_data(5)
pprint( zip(S, T) )

# <codecell>

print fast_interval_overlap(S, T)

# <codecell>

%timeit find_interval_overlap(S, T)

# <codecell>

%timeit fast_interval_overlap(S, T)

# <codecell>

# Scaling up?
S, T = make_interval_data(1000)

# <codecell>

%timeit find_interval_overlap(S, T)

# <codecell>

%timeit fast_interval_overlap(S, T)

# <markdowncell>

# ---
# # Note:
# 
# Outers are great for relatively small comparison sets and simple operations.  However, they require $\Theta(nm)$ storage for an $n$-by-$m$ comparison, which can quickly eat up memory if you're not careful.  
# 
# For many applications, though, the speedup due to vectorization is worth the increased memory complexity.


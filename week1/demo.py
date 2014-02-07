# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CRÜCIAL PŸTHON: IPython Notebook Demo

# <codecell>

from IPython.core.display import Image 
Image(filename='logo.png', width=600) 

# <markdowncell>

# ## Cells
# IPython Notebook is a cell-based development environment.  Each block of code (or text) can be run independently, and all cells share the same kernel.  Each evaluated cell is stored in the ```In``` array, and the corresponding output is stored in ```Out```.

# <markdowncell>

# Given $a \in \mathbb{R}^D$, compute $\sum_{i = 1}^D a[i]^2$.

# <codecell>

def sum_of_squares(a):
    return np.sum(a**2)

# <codecell>

foo = np.array([1, 3, 5])
sum_of_squares(foo)

# <codecell>

print Out[3] + 4

# <codecell>

# With the --pylab inline option, matplotlib plots are inline as cell output
w = np.linspace(0, 4*pi, 1000)
plt.plot(w, np.sin(w))

# <markdowncell>

# ## Tab Completion and documentation
# IPython will keep track of the members of all of the modules you import and give you tab-completion.  It will also tab-complete function arguments and provide help() documentation inline.

# <codecell>

import scipy.signal

# <codecell>

scipy.signal.fi

# <codecell>

help(scipy.signal.firwin)

# <markdowncell>

# ## %magics
# 
# IPython includes "magics", which are provide bonus useful functionality in IPython only.  

# <codecell>

# %timeit runs a single line a bunch of times and reports the average run time
%timeit np.arange(1000)
%timeit xrange(1000)

# <codecell>

%%prun
# prun runs Python's profiler on the current cell
N = 1e5
scipy.signal.fftconvolve(np.random.rand(N), np.random.rand(N))

# <codecell>

# Not a magic, but IPython also allows for running shell commands
!ls -lh

# <codecell>

# The Python-Matlab bridge can be used as a magic
import pymatbridge as pymat
ip = get_ipython()
pymat.load_ipython_extension(ip)

# <codecell>

# Python variable - a filter cutoff
Wn = .2

# <codecell>

%%matlab -i Wn -o b
b = fir1(30, Wn);

# <codecell>

import scipy.signal
w, h = scipy.signal.freqz(b);
plt.plot(w, np.abs(h))

# <markdowncell>

# ## Output
# * .ipynb files - human-readable json with all output cached
# * Autosaving
# * .py files with --script option
# * HTML, PDF, LaTeX, etc.
# * nbviewer to view notebooks without IPython installed
# http://nbviewer.ipython.org/github/craffel/crucialpython/blob/master/week1/demo.ipynb


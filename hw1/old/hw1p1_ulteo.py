
"""



"""

from __future__ import division
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as ss
#import statsmodels.api as sm
from statsmodels.robust.scale import mad


def calc_median(x):
    """ """
    #x.sort_values(inplace=True)  # for pd Series; but indices follow...
    x = np.array(x)
    x.sort()
    n = x.size
    
    if n % 2 == 0:
        i1 = int(n/2)
        i2 = int((n+1)/2)
        median = (x[i1]+x[i2]) / 2
    else:
        i = int((n+1)/2)
        median = x[i]

    return median


def calc_std(x):
    """Calculate corrected sample standard deviation $s$"""
    n = x.size
    xbar = x.mean()

    ssqd = 1/(n+1)*np.sum((x-xbar)**2)
    s = np.sqrt(ssqd)

    return s

    
def calc_iqr(x):
    """Calculate IQR using fn calc_median"""
    #x.sort_values(inplace=True)
    x = np.array(x)
    x.sort()
    n = x.size
    
    if n % 2 == 0:
        i = int(n/2)
        x1 = x[:i]
        x2 = x[i:]
    else:
        i = int((n+1)/2)
        x1 = x[:i]
        x2 = x[(i-1):]

    q1 = calc_median(x1)
    q3 = calc_median(x2)

    return q3 - q1


def calc_iqr_pd(x):
    """Calculate IQR using Pandas quantile df method"""
    try:
        q1 = x.quantile(0.25)
        q3 = x.quantile(0.75)
        return q3 - q1
    
    except AttributeError:
        print('requires pd.Series input')



def calc_mad(x):
    """Calculate median absolute deviation using fn calc_median

    MAD := the median of the absolute deviations from the data's median
    """
    #x.sort_values()
    x_median = calc_median(x)

    absdevs = np.abs(x-x_median)
    
    return calc_median(absdevs)


def calc_skew(x):
    """Calculate skewness using fn calc_std"""
    n = x.size
    xbar = x.mean()
    m3 = 1/n * np.sum( (x-xbar)**3 )  # 3rd moment
    s3 = calc_std(x)**3

    return m3/s3


def summary_stats(x, save_table=False):
    """Create descriptive stats table for input np array or pd series x
    save table if desired
    """

    mean = x.mean()  # using array method (Numpy) / Series method (Pandas)
    assert(np.isclose( mean, x.sum()/x.size ))

    median = x.median()  # using array method (Numpy) / Series method (Pandas)
    assert(np.isclose( median, calc_median(x) ))

    std = x.std()  # using array method (Numpy) / Series method (Pandas)
    assert(np.isclose( std, calc_std(x) ))

    iqr = ss.iqr(x)  # using Scipy Stats
    assert(np.isclose( iqr, calc_iqr(x) ))
    assert(np.isclose( iqr, calc_iqr_pd(x) ))

    # c is a normalization constant
    # that we only if we are relating MAD to the standard deviation
    # https://en.wikipedia.org/wiki/Median_absolute_deviation#Relation_to_standard_deviation
    mad = mad(x, c=1)  # using StatsModels (Pandas only has *mean* absolute dev)
    assert(np.isclose( mad, calc_mad(x) ))
    
    skew = ss.skew(x)  # using Scipy Stats; Series also have skew() method
    assert(np.isclose( skew, calc_skew(x) ))
    



# ------------------------------------------------------------------------------
# part 1

#> load data

dfname = './data/SC_data.xlsx'

#Tmin, Tmax, PCP = np.loadtxt(dfname, 

convert_dateint = lambda d: pd.to_datetime(str(d))

df = pd.read_excel(dfname,
    header=None, 
    #index_col=0, 
    #names=['Tmin', 'Tmax', 'PCP', '5', '6'],
    names=['date', 'Tmin', 'Tmax', 'PCP', '5', '6'],
    converters={0: convert_dateint},
    )

#df.index = df.index.astype
#df.date = pd.to_datetime(df.date.astype(str))


#> correct for missing values

varnames = ['Tmin', 'Tmax', 'PCP']
for varname in varnames:  # probably can do without loop
    df.loc[df[varname] == -99.0] = 0

df.loc[df.PCP == -1.0] = 0.


#> plot data time series

f1, [a1, a2, a3] = plt.subplots(3, 1)

df.plot(x='date', y='Tmin', ax=a1) 
df.plot(x='date', y='Tmax', ax=a2) 
df.plot(x='date', y='PCP', ax=a3) 


#> plot boxplots

f2, a1 = plt.subplots(1, 1)

df.boxplot(column=['Tmin', 'Tmax', 'PCP'], ax=a1)





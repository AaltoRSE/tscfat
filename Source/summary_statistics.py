#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:56:55 2020

@author: ikaheia1

Calculate the following summary statistics for the given timeseries and plot
the results:
    - Histogram
    - Lag plot with lag 1
    - Autocorrelation
    - Partial autocorrelation function
    - Autocorrelation function
    
"""
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from setup import setup_ps, setup_pd
import pytest
from plot_decorator import plot_decorator

@plot_decorator
def __Plot_summary(series,
                   title,
                   savepath=False,
                   savename=False,
                   test=False):
    """
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.

    Returns
    -------
    None.

    """
    
    fig,ax = plt.subplots(3,2,figsize=(8,8))
    fig.suptitle(title,fontsize=20,y=1.05)
    
    ax[0,0].plot(series)
    ax[0,0].set_title('Original timeseries')
    ax[0,0].set_xticklabels(ax[0,0].get_xticks(),Rotation= 45) 
    
    ax[0,1].hist(series,20)
    ax[0,1].set_title("Histogram")

    
    pd.plotting.lag_plot(series,lag=1,ax=ax[1,0])
    ax[1,0].set_title('Lag plot / lag 1')
    
    
    pd.plotting.autocorrelation_plot(series,ax=ax[1,1])
    ax[1,1].set_xlim([0,240])
    ax[1,1].set_title('Autocorrelation')
    
    sm.graphics.tsa.plot_pacf(series,lags=48,ax=ax[2,0])
    
    sm.graphics.tsa.plot_acf(series,lags=24,ax=ax[2,1])
    
    fig.tight_layout(pad=1.0)
    
    if test:
        return fig
    else:
        return None


def Summary_statistics(series,
                       title = "Time series summary",
                       savepath = False,
                       savename = False,
                       test = False):
    """
    

    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.
    test : Boolean, optional
        Flag for test function. The default is False.

    Returns
    -------
    None.

    """
    
    assert isinstance(series, pd.Series), "Series is not a pandas Series."
    
    sf = __Plot_summary(series,title,savepath,savename)
    return sf

def test_Summary_statistics():
    """
    Test Summary_statistics function. Test that returned fig is not None, and 
    Pandas data frame as an argument raises an error.

    Returns
    -------
    None.

    """
    test_fig = Summary_statistics(setup_ps(), savepath = False, savename = False, test = True)
    assert test_fig is not None
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        Summary_statistics(setup_pd(),'Test title', savepath = False, savename = False, test = True)
    expected_error_msg = "Series is not a pandas Series."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
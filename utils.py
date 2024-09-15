from matplotlib import pyplot as plt
from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf

def forceodd(i: int, plus=True):
    if i % 2 == 0:
        if plus:
            return i+1
        else:
            return i-1
    else:
        return i

def medfilt(x: np.array, kernelsize: int):
    if kernelsize < 3:
        return x
    kernelsize = forceodd(kernelsize)
    
    # Pad the input array with edge values to handle borders
    pad = kernelsize // 2
    if x.shape[0] < kernelsize:
        diff = kernelsize - x.shape[0]
        pad += ((diff // 2)+1)
    xpad = np.pad(x, (pad, pad), mode='edge')
    
    xfilt = []
    
    # Slide the window over the input array
    for i in range(len(x)):
        # Extract the window of values
        window = xpad[i:i + kernelsize]
        # Compute the median of the window and append to the result
        xfilt.append(np.median(window))
    
    return np.array(xfilt)

def hist_prob_plots(df, col):
    # function to plot a histogram and a Q-Q plot
    # side by side, for a certain variable
    plt.subplot(1, 2, 1)
    plt.title(col)
    df[col].hist()
    plt.subplot(1, 2, 2)
    stats.probplot(df[col], dist="norm", plot=plt)
    plt.show()

def find_best_kernel(df, col, ref):
    kernel_sizes = [0,7,11,21,31,51,71,101,201,301,501,701,901,1001,3001]
    res = []
    for k in kernel_sizes:
        data = df.copy()
        if k > 0:
            data.loc[:,col] = medfilt(data[col].to_numpy(), kernelsize=k)
        corr = abs(data.corr()[ref][col])
        res.append((k,corr))
    res = sorted(res, key=lambda x: -x[1])
    print(f"{col} best kernel: {res[0]}")
    return res[0][0]

def derivative_computer(df, col, dt, dx_colname="dx"):
    DEFAULT = 2
    if dt < 1 or dt >= df.shape[0]:
        print("dt must be non-zero positive integer < rows in df")
        print(f"dt = {dt} is not supported, defaulting to {DEFAULT}")
        dt = DEFAULT
    dx_list = []
    for _, data in df.groupby(["unit"]):
        x = data.loc[:,col].to_numpy().reshape((data.shape[0],))
        dx = np.zeros(shape=(data.shape[0],))
        if dt < x.shape[0]:
            for i in range(dt, x.shape[0]):
                dx[i] = (x[i] - x[i-dt]) / dt
        dx_list.append(dx)
    
    df[dx_colname] = np.concatenate(dx_list)
    return df

def find_best_dt(df, col, target):
    dts = np.linspace(start=2, stop=200, num=100)
    res = []
    for dt in dts:
        dt = int(dt)
        data = df.loc[:,["unit",col,target]]
        dx_colname = col+"_dx"+str(dt) 
        data = derivative_computer(data, col, dt, dx_colname)
        corr = abs(data.corr()[target][dx_colname])
        res.append((dt,corr))
        del data
    res = sorted(res, key=lambda x: -x[1])
    print(f"{col} best dt: {res[0]}")
    return res[0][0]

def graph_ts(df, cols):
    plots = len(cols)
    for i in range(1, plots+1):
        plt.subplot(plots,1,i)
        plt.ylabel(cols[i-1])
        plt.plot(df.index.to_pydatetime(), df[cols[i-1]].values)
    plt.tight_layout()
    plt.show()

def acf_plot(df, col):
    plot_acf(df[col])
    plt.xlabel('Lag')
    plt.ylabel('ACF')
    plt.show()

def plot_diff_smooth(df, col, window):
    plt.subplot(2,1,1)
    plt.plot(df[col], label=col, color="gray", alpha=0.75)
    plt.plot(df[col].rolling(window=window).mean(), 
             linestyle="--", color="green", 
             label="Smoothed")
    plt.legend()
    plt.ylabel(col)
    plt.subplot(2,1,2)
    plt.plot(df[col].diff())
    plt.ylabel("Difference")
    plt.show()
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

from utils import medfilt, forceodd

class OsRenamer(BaseEstimator, TransformerMixin):
    MAP = {"OS1": "altitude_kft", "OS2": "mach", "OS3": "temperature_F"}
    def __init__(self):
        self.map = {}
        self.inverse_map = {}
    def fit(self, X, _=None):
        for col in OsRenamer.MAP:
            if col in X.columns.values:
                self.map[col] = OsRenamer.MAP[col]
                self.inverse_map[OsRenamer.MAP[col]] = col
        return self
    def transform(self, X, _=None):
        X = X.rename(columns=self.map)
        return X
    def inverse_transform(self, X, _=None):
        X = X.rename(columns=self.inverse_map)
        return X

class DateTimeIndexer(BaseEstimator, TransformerMixin):
    def __init__(self, start: pd.Timestamp = "1900-01-01 12:00:00", 
                 step: pd.Timedelta = pd.Timedelta("5m")):
        self.start = start
        self.step = step
        self.og_index = None
    def fit(self, X, _=None):
        return self
    def transform(self, X, _=None):
        self.og_index = X.index.copy()
        k = X.shape[0]
        X = X.set_index(pd.date_range(start=self.start, periods=k, freq=self.step))
        return X
    def inverse_transform(self, X, _=None):
        X = X.set_index(self.og_index)
        return X
    
class MedianFilter(BaseEstimator, TransformerMixin):
    def __init__(self, filtcols, refcol, groupkey, kmax=9, kstep=2, verbose=0):
        self.filtcols = filtcols
        self.refcol = refcol
        self.groupkey = groupkey
        self.kmax = kmax
        self.kstep = kstep
        self.verbose = verbose
        self.kernels = {c: 0 for c in filtcols}
        self.ksizes = np.arange(start=3, stop=kmax, step=kstep)
    def fitgroup(self, df, col):
        ref = df[self.refcol].values
        res = [(0,abs(np.corrcoef(df[col].values,ref)[0,1]))]
        for k in self.ksizes:
            x = df[col].values.copy()
            if k > 0:
                x = medfilt(x, kernelsize=k)
            corr = abs(np.corrcoef(x,ref)[0,1])
            res.append((k,corr))
        res = sorted(res, key=lambda x: -x[1])
        print(f"{col} best kernel: {res[0]}")
        return res[0][0]
    def fit(self, X, _=None):
        ngroups = X[self.groupkey].nunique()
        for _, df in X.groupby(self.groupkey):
            for col in self.filtcols:
                self.kernels[col] += self.fitgroup(df[[col,self.refcol]], col)
        for col, k in self.kernels.items():
            self.kernels[col] = forceodd(k // ngroups)
        if self.verbose > 0:
            print(f"kernels: {self.kernels}")
    def transform(self, X, _=None):
        for _, df in X.groupby(self.groupkey):
            for col in self.filtcols:
                X.loc[df.index,col] = medfilt(df[col], self.kernels[col])
        return X

class DiffCalc(BaseEstimator, TransformerMixin):
    def __init__(self, cols, groupkey):
        self.cols = cols
        self.groupkey = groupkey
    def fit(self, X, _=None):
        return self
    def transform(self, X, _=None):
        for col in self.cols:
            newname = f"prev_{col}"
            X.loc[:,newname] = np.zeros((X.shape[0],))
        for _, df in X.groupby(self.groupkey):
            for col in self.cols:
                newname = f"prev_{col}"
                X.loc[df.index,newname] = df[col].diff()
                X.loc[df.index,newname].iloc[0] = 0
        return X

class CustomScaler(BaseEstimator, TransformerMixin):
    def __init__(self, x_cols, scaler):
        self.x_cols = x_cols
        self.scaler = scaler
    def fit(self, X, y=None):
        X.loc[:,self.x_cols] = self.scaler.fit(X, y)
        return self
    def transform(self, X, y=None):
        X.loc[:,self.x_cols] = self.scaler.transform(X, y)
        return X
    def inverser_transform(self, X, y=None):
        X.loc[:,self.x_cols] = self.scaler.inverse_transform(X, y)
        return X
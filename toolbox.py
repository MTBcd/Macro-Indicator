import pandas as pd
import numpy as np
import cvxpy
import scipy.sparse
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class Toolbox:

    @staticmethod
    def PCA_transform(df, num_comp=1):
        scaler = StandardScaler()
        X_std = scaler.fit_transform(df)
        pca = PCA(n_components=num_comp)
        X_pca = pca.fit_transform(X_std)
        return -pd.DataFrame(X_pca).set_index(df.index)

    @staticmethod
    def L1_trend_filter(df, regulation_param=0.5):
        y = df.values.reshape((-1, 1))
        n = len(y)
        # Form the second difference matrix.
        e = np.ones((1, n))
        D = scipy.sparse.spdiags(np.vstack((e, -2 * e, e)), range(3), n - 2, n)

        # L1 trend filtering
        x = cvxpy.Variable(shape=(n, 1))

        # Minimize the sum of squares and L1 norm
        obj = cvxpy.Minimize(np.dot(0.5, cvxpy.sum_squares(y - x)) + regulation_param * cvxpy.norm(np.dot(D, x), 1))
        cvxpy.Problem(obj).solve(solver="ECOS", verbose=True)  # Use your chosen solver

        return pd.DataFrame(np.array(x.value).flatten()).set_index(df.index)


    @staticmethod
    def Regime_identification(filtre: pd.DataFrame, macro_indicator: pd.DataFrame) -> pd.DataFrame:
        momentums = filtre.diff().fillna((filtre.iloc[1, 0] - filtre.iloc[0, 0])).iloc[:, 0]

        levels = macro_indicator.iloc[:, 0].apply(lambda x: 1 if x >= 0 else -1)

        conditions = [
            (levels < 0) & (momentums < 0),
            (levels < 0) & (momentums > 0),
            (levels > 0) & (momentums > 0),
            (levels > 0) & (momentums < 0)

        ]
        Regime_libs = np.select(conditions, ["Contraction", "Recovery", "Expansion", "Slowdown"])
        encodes = np.select(conditions, [0, 1, 2, 3])

        return pd.DataFrame(encodes, index=macro_indicator.index, columns=["encode regime"])

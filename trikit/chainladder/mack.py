"""
_MackChainLadder implementation.
"""
import numpy as np
import pandas as pd
from scipy.stats import norm, lognorm
from . import BaseChainLadder



class MackChainLadder(BaseChainLadder):
    """
    Perform Mack Chain Ladder method. The predicition variance is comprised
    of the estimation variance and the process variance. Estimation variance
    arises from the inability to accurately define the distribution from which
    past events have been generated. Process variance arises from the
    inability to accurately predict which single outcome from the distribution
    will occur at a given time. The predicition error is defined as the
    standard deviation of the forecast.

    References
    ----------
    - Mack, Thomas, (1993), *Distribution-Free Calculation of the Standard Error
      of Chain Ladder Reserve Estimates*, ASTIN Bulletin 23, no. 2:213-225.

    - Mack, Thomas, (1999), *The Standard Error of Chain Ladder Reserve Estimates:
      Recursive Calculation and Inclusion of a Tail Factor*, ASTIN Bulletin 29,
      no. 2:361-366.

    - England, P., and R. Verrall, (2002), *Stochastic Claims Reserving in General
      Insurance*, British Actuarial Journal 8(3): 443-518.

    - Murphy, Daniel, (2007), *Chain Ladder Reserve Risk Estimators*, CAS E-Forum,
      Summer 2007.
    """
    def __init__(self, cumtri):
        """
        Parameters
        ----------
        cumtri: triangle._CumTriangle
            A cumulative.CumTriangle instance
        """

        super().__init__(cumtri)

        self._mod_a2aind = None
        self._mod_tri = None


        # properties
        self._parameter_error = None
        self._process_error = None
        self._inverse_sums = None
        self._originref = None

        self._devpref = None
        self._devpvar = None
        self._mseptot = None
        self._rmsepi = None
        self._msepi = None


    # def __call__(self, alpha=1, tail=1.0):
    #     """
    #     Return a summary of ultimate and reserve estimates resulting from
    #     the application of the development technique over self.tri. Summary
    #     DataFrame is comprised of origin year, maturity of origin year, loss
    #     amount at latest evaluation, cumulative loss development factors,
    #     projected ultimates and the reserve estimate, by origin year and in
    #     aggregate.
    #
    #     Returns
    #     -------
    #     pd.DataFrame
    #         Summary with values by origin year for maturity, latest cumulative
    #         loss amount, cumulative loss development factor, projected
    #         ultimate loss and the reserve amount.
    #     """
    #     # Bind reference to class method return values.
    #     ldfs    = self._ldfs(alpha, tail=tail)
    #     cldfs   = self._cldfs(sel=sel, tail=tail)
    #     ults    = self._ultimates(cldfs=cldfs)
    #     ibnr    = self._reserves(ultimates=ults)
    #     sigma_i = np.log(1 + self.msepi / ibnr**2)
    #     mu_i    = np.log(ibnr - .50 * sigma_i)
    #
    #     summcols = ["maturity", "latest", "cldf", "ultimate", "reserve"]
    #     summDF   = pd.DataFrame(columns=summcols, index=self.tri.index)
    #     summDF["maturity"]  = self.tri.maturity.astype(np.str)
    #     summDF["latest"]    = self.tri.latest_by_origin
    #     summDF["cldf"]      = cldfs.values[::-1]
    #     summDF["ultimate"]  = ults
    #     summDF["reserve"]   = ibnr
    #     self._summary['RMSEP']        = self.rmsepi
    #     self._summary['CV']           = self.rmsepi/self.reserves
    #     self._summary["NORM_95%_LB"]  = self.reserves - (1.96 * self.rmsepi)
    #     self._summary["NORM_95%_UB"]  = self.reserves + (1.96 * self.rmsepi)
    #     self._summary["LNORM_95%_LB"] = np.exp(mu_i - 1.96 * sigma_i)
    #     self._summary["LNORM_95%_UB"] = np.exp(mu_i + 1.96 * sigma_i)
    #     self._summary.loc['TOTAL']    = self._summary.sum()
    #     summDF.loc["total"] = summDF.sum()
    #
    #     # Set to NaN columns that shouldn't be summed.
    #     summDF.loc["total", "maturity"] = ""
    #     summDF.loc["total", "cldf"]     = np.NaN
    #     summDF = summDF.reset_index().rename({"index":"origin"}, axis="columns")
    #
    #
    #
    #
    #         # # Populate self._summary with existing properties if available.
    #         # self._summary['LATEST']       = self.latest_by_origin
    #         # self._summary['CLDF']         = self.cldfs[::-1]
    #         # self._summary['EMERGENCE']    = 1/self.cldfs[::-1]
    #         # self._summary['ULTIMATE']     = self.ultimates
    #         # self._summary['RESERVE']      = self.reserves
    #         # self._summary['RMSEP']        = self.rmsepi
    #         # self._summary['CV']           = self.rmsepi/self.reserves
    #         # self._summary["NORM_95%_LB"]  = self.reserves - (1.96 * self.rmsepi)
    #         # self._summary["NORM_95%_UB"]  = self.reserves + (1.96 * self.rmsepi)
    #         # self._summary["LNORM_95%_LB"] = np.exp(mu_i - 1.96 * sigma_i)
    #         # self._summary["LNORM_95%_UB"] = np.exp(mu_i + 1.96 * sigma_i)
    #         # self._summary.loc['TOTAL']    = self._summary.sum()
    #         #
    #         # # Set CLDF Total value to `NaN`.
    #         # self._summary.loc["TOTAL","CLDF","EMERGENCE"] = np.NaN
    #
    #     return(self._summary)


    @staticmethod
    def get_quantile(*pctl):
        pass


    @property
    def mod_tri(self):
        """
        Return modified triangle-shaped DataFrame with same indices as
        self.tri.a2a.

        Returns
        -------
        pd.DataFrame
        """
        if self._mod_tri is None:
            self._mod_tri = self.tri.copy(deep=True)
            for ii in range(self.tri.latest.shape[0]):
                r_indx = self.tri.latest.loc[ii, "origin"].item()
                c_indx = self.tri.latest.loc[ii, "dev"].item()
                self._mod_tri.at[r_indx, c_indx] = np.NaN
            self._mod_tri = self._mod_tri.dropna(axis=0, how="all").dropna(axis=1, how="all")
        return(self._mod_tri)


    @property
    def mod_a2aind(self):
        """
        Return self.tri.a2aind with lower-right 0s replaced with NaN.

        Returns
        -------
        pd.DataFrame
        """
        if self._mod_a2aind is None:
            self._mod_a2aind = self.tri.a2aind.replace(0, np.NaN)
        return(self._mod_a2aind)



    def _ldfs(self, alpha=1):
        """
        Compute Mack loss development factors.

        Parameters
        ----------
        alpha: {0, 1, 2}
            * ``0``: Straight average of observed individual link ratios.
            * ``1``: Historical Chain Ladder age-to-age factors.
            * ``2``: Regression of $C_{k+1}$ on $C_{k}$ with 0 intercept.

        Returns
        -------
        pd.Series
        """
        C, w = self.mod_tri, self.mod_a2aind
        return((self.tri.a2a * w * C**alpha).sum(axis=0) / (w * C**alpha).sum(axis=0))


    def _devp_variance(self, alpha=1):
        """
        Compute the development period variance, usually represented as
        $\hat{\sigma}^{2}_{k}$ in the literature. For a triangle with
        ``n`` development periods, result will contain ``n-1`` elements.

        Parameters
        ----------
        alpha: {0, 1, 2}
            * ``0``: Straight average of observed individual link ratios.
            * ``1``: Historical Chain Ladder age-to-age factors.
            * ``2``: Regression of $C_{k+1}$ on $C_{k}$ with 0 intercept.

        Returns
        -------
        pd.Series
        """
        devpvar = np.zeros(self.tri.devp.size - 1)
        ldfs = self._ldfs(alpha=alpha)
        C, w, F = self.mod_tri, self.mod_a2aind, self.tri.a2a
        n = self.tri.origins.size
        for indx, jj in enumerate(self.tri.devp[:-2]):
            devpvar[indx] = \
                (w[jj] * (C[jj]**alpha) * (F[jj] - ldfs[jj])**2).sum() / (n - jj - 1)

        # Calculate development period variance for period n-1.
        devpvar[-1] = np.min((devpvar[-2]**2 / devpvar[-3], np.min([devpvar[-2], devpvar[-3]])))
        return(pd.Series(devpvar, index=self.tri.devp[:-1], name="devp_variance"))



    # @property
    # def originref(self):
    #     """
    #     Intended for internal use only. Contains data by origin year.
    #     """
    #     if self._originref is None:
    #         self._originref = pd.DataFrame({
    #             'reserve'      :self.reserves,
    #             'ultimate'     :self.ultimates,
    #             'process_error':self.process_error,
    #             'param_error'  :self.parameter_error,
    #             'msep'         :self.msepi,
    #             'rmsep'        :self.rmsepi}, index=self.tri.index)
    #         self._originref = \
    #             self._originref[
    #                 ["reserve","ultimate","process_error","param_error","msep","rmsep"]
    #                 ]
    #     return(self._originref)
    #
    #
    #
    # @property
    # def devpref(self):
    #     """
    #     Intended for internal use only. Contains data by development period.
    #     """
    #     if self._devpref is None:
    #         self._devpref = pd.DataFrame({
    #             "ldf"    :self.ldfs,
    #             "sse"    :self.devpvar.values,
    #             "ratio"  :(self.devpvar.values / self.ldfs ** 2),
    #             "dev"    :self.tri.columns[:-1],
    #             "inv_sum":self.inverse_sums},
    #             index=self.tri.columns[:-1]
    #             )
    #
    #         self._devpref["indx"] = \
    #             self._devpref["dev"].map(
    #                 lambda x: self.tri.columns.get_loc(x))
    #
    #         self._devpref = \
    #             self._devpref[["dev","indx","ldf","sse","ratio","inv_sum"]]
    #
    #     return(self._devpref)
    #
    #
    #
    # @property
    # def inverse_sums(self):
    #     """
    #     Convenience aggregation for use in parameter error
    #     calcuation.
    #     """
    #     if self._inverse_sums is None:
    #         devp_sums = \
    #             self.tri.sum(axis=0)-self.tri.latest_by_origin[::-1].values
    #         self._inverse_sums = pd.Series(
    #             data=devp_sums,index=devp_sums.index,name='inverse_sums')
    #         self._inverse_sums = (1 / (self._inverse_sums))[:-1]
    #     return(self._inverse_sums)



    # @property
    # def inverse_sums2(self):
    #     """
    #     Convenience aggregation for use in parameter error
    #     calcuation.
    #     """
    #     if self._inverse_sums is None:
    #         devp_sums = list()
    #         for devp in self.tri.columns[:-1]:
    #             iterep  = self.tri.index.get_loc(self.tri[devp].last_valid_index())
    #             devpos  = self.tri.columns.get_loc(devp)
    #             itersum = self.tri.iloc[:iterep,devpos].sum()
    #             devp_sums.append((devp,(1/itersum)))
    #         indx, vals = zip(*devp_sums)
    #         self._inverse_sums = \
    #             pd.Series(data=vals, index=indx, name='inverse_sums')
    #     return(self._inverse_sums)


    # @property
    # def devpvar(self) -> np.ndarray:
    #     """
    #     devpvar = `development period variance`. Return the variance
    #     of each n-1 development periods as a Series object.
    #     """
    #     if self._devpvar is None:
    #         n = self.tri.columns.size
    #         self._devpvar = np.zeros(n - 1, dtype=np.float_)
    #         for k in range(n - 2):
    #             iter_ses = 0  # `square of standard error`
    #             for i in range(n - (k + 1)):
    #                 c_1, c_2 = self.tri.iloc[i, k], self.tri.iloc[i,k+1]
    #                 iter_ses+=c_1*((c_2 / c_1) - self.ldfs[k])**2
    #             iter_ses = iter_ses/(n-k-2)
    #             self._devpvar[k] = iter_ses
    #
    #             # Calculate standard error for dev period n-1.
    #         self._devpvar[-1] = \
    #             np.min((
    #                 self._devpvar[-2]**2 / self._devpvar[-3],
    #                 np.min([self._devpvar[-2],self._devpvar[-3]])
    #                 ))
    #         self._devpvar = pd.Series(
    #             data=self._devpvar, index=self.tri.columns[:self._devpvar.size],
    #             name="sqrd_std_error")
    #     return(self._devpvar)
    #
    #
    #
    #
    # @property
    # def process_error(self):
    #     """
    #     Process error (forecast error) calculation. The process error
    #     component originates from the stochastic movement of the process.
    #     Returns a pandas Series containing estimates of process variance by
    #     origin year.
    #     """
    #     if self._process_error is None:
    #         lastcol, pelist = self.tri.columns.size-1, list()
    #         for rindx in self.tri.rlvi.index:
    #             iult = self.ultimates[rindx]
    #             ilvi = self.tri.rlvi.loc[rindx,:].col_offset
    #             ilvc = self.tri.rlvi.loc[rindx,:].dev
    #             ipe  = 0
    #             if ilvi<lastcol:
    #                 for dev in self.trisqrd.loc[rindx][ilvi:lastcol].index:
    #                     ipe+=(self.devpref.loc[dev,'RATIO'] / self.trisqrd.loc[rindx,dev])
    #                 ipe*=(iult**2)
    #             pelist.append((rindx,ipe))
    #
    #         # Convert list of tuples into Series object.
    #         indx, vals = zip(*pelist)
    #         self._process_error = \
    #             pd.Series(data=vals, index=indx, name="process_error")
    #     return(self._process_error)
    #
    #
    #
    #
    # @property
    # def parameter_error(self):
    #     """
    #     Estimation error (parameter error) reflects the uncertainty in
    #     the estimation of the parameters.
    #     """
    #     if self._parameter_error is None:
    #         lastcol, pelist = self.tri.columns.size-1, list()
    #         for i in enumerate(self.tri.index):
    #             ii, rindx = i[0], i[1]
    #             iult = self.ultimates[rindx]
    #             ilvi = self.tri.rlvi.loc[rindx,:].col_offset
    #             ilvc = self.tri.rlvi.loc[rindx,:].dev
    #             ipe  = 0
    #             if ilvi<lastcol:
    #                 for k in range(ilvi,lastcol):
    #                     ratio  = self.devpref[self.devpref['indx']==k]['ratio'].values[0]
    #                     invsum = self.devpref[self.devpref['indx']==k]['inv_sum'].values[0]
    #                     ipe+=(ratio * invsum)
    #                 ipe*=iult**2
    #             else:
    #                 ipe = 0
    #             pelist.append((rindx, ipe))
    #         # Convert list of tuples into Series object.
    #         indx, vals = zip(*pelist)
    #         self._parameter_error = \
    #             pd.Series(data=vals, index=indx, name="parameter_error")
    #     return(self._parameter_error)
    #
    #
    #
    #
    # @property
    # def covariance_term(self):
    #     """
    #     Used to derive the conditional mean squared error of total
    #     reserve prediction. MSE_(i,j) is non-zero only for cells
    #     in which i < j (i.e., the
    #     :return:
    #     """
    #     pass
    #
    #
    # @property
    # def msepi(self):
    #     """
    #     Return the mean squared error of predicition by origin year.
    #     Does not contain estimate for total MSEP.
    #     MSE_i = process error + parameter error
    #     """
    #     if self._msepi is None:
    #         self._msepi = self.process_error + self.parameter_error
    #     return(self._msepi)
    #
    #
    # @property
    # def rmsepi(self):
    #     """
    #     Return the root mean squared error of predicition by origin
    #     year. Does not contain estimate for total MSEP.
    #
    #         MSE_i = process error + parameter error
    #     """
    #     if self._rmsepi is None:
    #         self._rmsepi = np.sqrt(self.msepi)
    #     return(self._rmsepi)
    #
    #
    #
    #
    # @property
    # def summary(self):
    #     """
    #     Return a DataFrame containing summary statistics resulting
    #     from applying the development method to tri, in addition
    #     to Mack-generated range estimates.
    #     """
    #     if self._summary is None:
    #         self._summary = \
    #             pd.DataFrame(
    #                 columns=[
    #                     "LATEST","CLDF","EMERGENCE","ULTIMATE","RESERVE","RMSEP",
    #                     "CV","NORM_95%_LB","NORM_95%_UB","LNORM_95%_LB","LNORM_95%_UB"
    #                     ], index=self.tri.index
    #                 )
    #
    #         # Initialize lognormal confidence interval parameters.
    #         sigma_i = np.log(1 + self.msepi/self.reserves**2)
    #         mu_i    = np.log(self.reserves - .50 * sigma_i)
    #
    #         # Populate self._summary with existing properties if available.
    #         self._summary['LATEST']       = self.latest_by_origin
    #         self._summary['CLDF']         = self.cldfs[::-1]
    #         self._summary['EMERGENCE']    = 1/self.cldfs[::-1]
    #         self._summary['ULTIMATE']     = self.ultimates
    #         self._summary['RESERVE']      = self.reserves
    #         self._summary['RMSEP']        = self.rmsepi
    #         self._summary['CV']           = self.rmsepi/self.reserves
    #         self._summary["NORM_95%_LB"]  = self.reserves - (1.96 * self.rmsepi)
    #         self._summary["NORM_95%_UB"]  = self.reserves + (1.96 * self.rmsepi)
    #         self._summary["LNORM_95%_LB"] = np.exp(mu_i - 1.96 * sigma_i)
    #         self._summary["LNORM_95%_UB"] = np.exp(mu_i + 1.96 * sigma_i)
    #         self._summary.loc['TOTAL']    = self._summary.sum()
    #
    #         # Set CLDF Total value to `NaN`.
    #         self._summary.loc["TOTAL","CLDF","EMERGENCE"] = np.NaN
    #
    #     return(self._summary)
    #
    #
    # @staticmethod
    # def get_quantile(*pctl):
    #     pass
    #
    #
    #
    # def __repr__(self):
    #     """
    #     Override default numerical precision used for representing
    #     ultimate loss projections and age-to-ultimate factors.
    #     """
    #     summary_cols = [
    #         "LATEST","CLDF","EMERGENCE","ULTIMATE","RESERVE","RMSEP",
    #         "CV","NORM_95%_LB","NORM_95%_UB","LNORM_95%_LB","LNORM_95%_UB"
    #         ]
    #
    #     summ_specs = pd.Series([0, 5, 5, 0, 0, 0, 5, 0, 0, 0, 0], index=summary_cols)
    #     return(self.summary.round(summ_specs).to_string())
    #
    #

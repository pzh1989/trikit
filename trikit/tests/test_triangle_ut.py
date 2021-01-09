"""
trikit.triangle tests.
"""
import sys
import unittest
import pandas as pd
import numpy as np
import os
import os.path
import logging
import timeit
import trikit



# IncrTriangle unit tests -----------------------------------------------------

class IncrTriangleTestCase(unittest.TestCase):
    def setUp(self):
        data = trikit.load(dataset="raa")
        self.tri = trikit.totri(data=data, type_="incremental")
        self.latest_ref = pd.DataFrame({
            "origin":list(range(1981, 1991, 1)), "maturity":list(range(10, 0, -1)),
            "dev":list(range(10, 0, -1)),
            "latest":[
                172.0, 535.0, 603.0, 984.0, 225.0, 2917.0, 1368.0,
                6165.0, 2262.0, 2063.0
                ],
            }, index=list(range(0, 10, 1))
            )


    def test_nbr_cells(self):
        self.assertEqual(
            self.tri.nbr_cells, 55
            )

    def test_triind(self):
        triindprod = (self.tri.triind * self.tri).sum().sum()
        self.assertTrue(
            np.allclose(triindprod, 0)
            )

    def test_rlvi(self):
        ref = pd.DataFrame({
            "dev":list(range(10, 0, -1)),
            "col_offset":list(range(9, -1, -1)),
            }, index=list(range(1981, 1991, 1))
            ).sort_index()
        self.assertTrue(ref.equals(self.tri.rlvi))

    def test_clvi(self):
        ref = pd.DataFrame({
            "origin":list(range(1990, 1980, -1)),
            "row_offset":list(range(9, -1, -1)),
            }, index=list(range(1, 11, 1))
            ).sort_index()
        self.assertTrue(ref.equals(self.tri.clvi))

    def test_devp(self):
        ref = pd.Series(
            data=self.latest_ref.dev.values.tolist()[::-1],
            name="devp"
            ).sort_index()
        self.assertTrue(ref.equals(self.tri.devp))

    def test_origins(self):
        ref = pd.Series(
            data=self.latest_ref.origin.values.tolist(),
            name="origin"
            ).sort_index()
        self.assertTrue(ref.equals(self.tri.origins))

    def test_maturity(self):
        dfref = self.latest_ref[["origin", "maturity"]]
        dftri = self.tri.maturity.to_frame().reset_index(drop=False).rename(
            {"index":"origin", "maturity":"maturity_tri"}, axis=1)
        dfcomp = dfref.merge(dftri, on="origin", how="left")
        dfcomp["diff"] = dfcomp["maturity"] - dfcomp["maturity_tri"]
        self.assertEqual(dfcomp["diff"].sum(), 0)

    def test_latest(self):
        dfref = self.latest_ref[["origin", "dev", "latest"]].sort_index()
        dftri = self.tri.latest.sort_index()
        self.assertEqual((dfref - dftri).sum().sum(), 0)

    def test_latest_by_origin(self):
        dfref = self.latest_ref[["origin", "latest"]].sort_index()
        dftri = self.tri.latest_by_origin.reset_index(drop=False).rename(
            {"index":"origin", "latest_by_origin":"latest_tri"}, axis=1)
        dfcomp = dfref.merge(dftri, on="origin", how="left")
        dfcomp["diff"] = dfcomp["latest"] - dfcomp["latest_tri"]
        self.assertEqual(dfcomp["diff"].sum(), 0)

    def test_latest_by_devp(self):
        dfref = self.latest_ref[["dev", "latest"]].sort_index()
        dftri = self.tri.latest_by_devp.reset_index(drop=False).rename(
            {"index":"dev", "latest_by_devp":"latest_tri"}, axis=1)
        dfcomp = dfref.merge(dftri, on="dev", how="left")
        dfcomp["diff"] = dfcomp["latest"] - dfcomp["latest_tri"]
        self.assertEqual(dfcomp["diff"].sum(), 0)

    def test_to_tbl(self):
        self.assertTrue(isinstance(self.tri.to_tbl(), pd.DataFrame))

    def test_to_cum(self):
        self.assertTrue(isinstance(self.tri.to_cum(), trikit.triangle.CumTriangle))






# CumTriangle unit tests ------------------------------------------------------

class CumTriangleTestCase(unittest.TestCase):

    def setUp(self):

        raa  = trikit.load(dataset="raa")
        self.tri = trikit.totri(raa, type_="cumulative")

        self.latest_ref = pd.DataFrame({
            "origin":list(range(1981, 1991, 1)), "maturity":list(range(10, 0, -1)),
            "dev":list(range(10, 0, -1)),
            "latest":[18834.0, 16704.0, 23466.0, 27067.0, 26180.0, 15852.0, 12314.0, 13112.0, 5395.0, 2063.0],
            }, index=list(range(0, 10, 1))
            )

        self.a2aref = pd.DataFrame({
            1:[1.64984, 40.42453, 2.63695, 2.04332, 8.75916, 4.25975, 7.21724, 5.14212, 1.72199],
            2:[1.31902, 1.25928, 1.54282, 1.36443, 1.65562, 1.81567, 2.72289, 1.88743, np.NaN],
            3:[1.08233, 1.97665, 1.16348, 1.34885, 1.39991, 1.10537, 1.12498, np.NaN, np.NaN],
            4:[1.14689, 1.29214, 1.16071, 1.10152, 1.17078, 1.22551,  np.NaN, np.NaN, np.NaN],
            5:[1.19514, 1.13184, 1.1857 , 1.11347, 1.00867,np.NaN, np.NaN, np.NaN, np.NaN],
            6:[1.11297, 0.9934 , 1.02922, 1.03773,  np.NaN, np.NaN,np.NaN, np.NaN, np.NaN],
            7:[1.03326, 1.04343, 1.02637,np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
            8:[1.0029 , 1.03309,np.NaN, np.NaN, np.NaN, np.NaN,np.NaN, np.NaN, np.NaN],
            9:[1.00922,np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
            }, index=list(range(1981, 1990))
            )

    def test_a2adim(self):
        self.assertEqual(
            self.tri.shape[0]-1, self.tri.a2a.shape[0],
            "Number of age-to-age factors different than expected."
            )

    def test_a2a(self):
        self.assertTrue(
            np.abs((self.a2aref - self.tri.a2a).sum().sum())<.0001,
            "Age-to-age Factors not properly computed."
            )

    def test_latest(self):
        dfref = self.latest_ref[["origin", "dev", "latest"]].sort_index()
        dftri = self.tri.latest.sort_index()
        self.assertEqual((dfref - dftri).sum().sum(), 0)

    def test_latest_by_origin(self):
        dfref = self.latest_ref[["origin", "latest"]].sort_index()
        dftri = self.tri.latest_by_origin.reset_index(drop=False).rename(
            {"index":"origin", "latest_by_origin":"latest_tri"}, axis=1)
        dfcomp = dfref.merge(dftri, on="origin", how="left")
        dfcomp["diff"] = dfcomp["latest"] - dfcomp["latest_tri"]
        self.assertTrue(np.allclose(dfcomp["diff"].sum(), 0))

    def test_latest_by_devp(self):
        dfref = self.latest_ref[["dev", "latest"]].sort_index()
        dftri = self.tri.latest_by_devp.reset_index(drop=False).rename(
            {"index":"dev", "latest_by_devp":"latest_tri"}, axis=1)
        dfcomp = dfref.merge(dftri, on="dev", how="left")
        dfcomp["diff"] = dfcomp["latest"] - dfcomp["latest_tri"]
        self.assertTrue(np.allclose(dfcomp["diff"].sum(), 0))

    def test_to_incr(self):
        self.assertTrue(isinstance(self.tri.to_incr(), trikit.triangle.IncrTriangle))

    def test_to_tbl(self):
        self.assertTrue(isinstance(self.tri.to_tbl(), pd.DataFrame))




class ToTriTestCase(unittest.TestCase):

    def setUp(self):

        origin, dev, value = "origin", "dev", "value"
        incrtab = trikit.load(dataset="raa")

        # Create cumulative tabular data.
        cumtab = incrtab.copy(deep=True).sort_values(by=["origin", "dev"]).reset_index(drop=True)
        cumtab["cum"] = cumtab.groupby(["origin"], as_index=False)["value"].cumsum()
        cumtab = cumtab.drop("value", axis=1).rename({"cum":"value"}, axis=1)

        # Create incremental triangle data.
        incrtri = incrtab[[origin, dev, value]]
        incrtri = incrtri.groupby([origin, dev], as_index=False).sum()
        incrtri = incrtri.sort_values(by=[origin, dev])
        incrtri = incrtri.pivot(index=origin, columns=dev).rename_axis(None)
        incrtri.columns = incrtri.columns.droplevel(0)

        # Create cumulative triangle data.
        cumtri = incrtab[[origin, dev, value]]
        cumtri = cumtri.groupby([origin, dev], as_index=False).sum()
        cumtri = cumtri.sort_values(by=[origin, dev])
        cumtri = cumtri.pivot(index=origin, columns=dev).rename_axis(None)
        cumtri.columns = cumtri.columns.droplevel(0)

        self.incrtab = incrtab
        self.cumtab = cumtab
        self.incrtri = incrtri
        self.cumtri = cumtri

        self.incr_latest_ref = pd.DataFrame({
            "origin":list(range(1981, 1991, 1)), "maturity":list(range(10, 0, -1)),
            "dev":list(range(10, 0, -1)),
            "latest":[172.0, 535.0, 603.0, 984.0, 225.0, 2917.0, 1368.0,6165.0, 2262.0, 2063.0],
            }, index=list(range(0, 10, 1))
            )

        self.cum_latest_ref = pd.DataFrame({
            "origin":list(range(1981, 1991, 1)), "maturity":list(range(10, 0, -1)),
            "dev":list(range(10, 0, -1)),
            "latest":[18834.0, 16704.0, 23466.0, 27067.0, 26180.0, 15852.0, 12314.0, 13112.0, 5395.0, 2063.0],
            }, index=list(range(0, 10, 1))
            )

    def test_cumtab_2_incrtri(self):
        # Convert cumulative tabular data to incr triangle.
        tri = trikit.totri(self.cumtab, type_="incr", data_format="cum", data_shape="tabular")
        self.assertTrue(
            isinstance(tri, trikit.triangle.IncrTriangle),
            "Error converting cum tabular data to incr tri."
            )

    def test_cumtab_2_cumtri(self):
        # Convert cumulative tabular data to cum triangle.
        tri = trikit.totri(self.cumtab, type_="cum", data_format="cum", data_shape="tabular")
        self.assertTrue(
            isinstance(tri, trikit.triangle.CumTriangle),
            "Error converting cum tabular data to cum tri."
            )

    def test_incrtab_2_incrtri(self):
        # Convert incremental tabular data to incr triangle.
        tri = trikit.totri(self.incrtab, type_="incr", data_format="incr", data_shape="tabular")
        self.assertTrue(
            isinstance(tri, trikit.triangle.IncrTriangle),
            "Error converting incr tabular data to incr tri."
            )

    def test_incrtab_2_cumtri(self):
        # Convert incremental tabular data to cum triangle.
        tri = trikit.totri(self.incrtab, type_="cum", data_format="incr", data_shape="tabular")
        self.assertTrue(
            isinstance(tri, trikit.triangle.CumTriangle),
            "Error converting incr tabular data to cum tri."
            )

    def test_incrtri_2_incrtri(self):
        # Convert incremental DataFrame tri to incr triangle.
        tri = trikit.totri(self.incrtri, type_="incr", data_format="incr", data_shape="triangle")
        self.assertTrue(
            isinstance(tri, trikit.triangle.IncrTriangle),
            "Error converting incr tri data to incr tri."
            )

    def test_incrtri_2_cumtri(self):
        # Convert incremental DataFrame tri to cum triangle.
        tri = trikit.totri(self.incrtri, type_="cum", data_format="incr", data_shape="triangle")
        self.assertTrue(
            isinstance(tri, trikit.triangle.CumTriangle),
            "Error converting incr tri data to cum tri."
            )

    def test_cumtri_2_incrtri(self):
        # Convert cumulative DataFrame tri to incr triangle.
        tri = trikit.totri(self.cumtri, type_="incr", data_format="cum", data_shape="triangle")
        self.assertTrue(
            isinstance(tri, trikit.triangle.IncrTriangle),
            "Error converting cum tri data to incr tri."
            )

    def test_cumtri_2_cumtri(self):
        # Convert cumulative DataFrame tri to cum triangle.
        tri = trikit.totri(self.cumtri, type_="cum", data_format="cum", data_shape="triangle")
        self.assertTrue(
            isinstance(tri, trikit.triangle.CumTriangle),
            "Error converting cumtri data to cumtri."
            )

    def test_alt_colnames(self):
        # Create triangle with different origin, dev and value names.
        dfrnm = self.incrtab.rename(
            {"origin":"ay", "dev":"devp", "value":"loss_amt"}, axis=1
            )
        tri = trikit.totri(
            dfrnm, type_="cum", data_format="incr", data_shape="tabular",
            origin="ay", dev="devp", value="loss_amt"
            )
        self.assertTrue(
            isinstance(tri, trikit.triangle.CumTriangle),
            "Error converting cumtri data to cumtri."
            )



if __name__ == "__main__":

    unittest.main()


























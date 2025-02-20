"""
Various trikit utilities. Contains convenience functions in support of
the CAS Loss Reserving Database and other sample datasets.
"""
import sys
import os.path
import numpy as np
import pandas as pd



def _load(dataset, loss_type="incurred", lob="comauto", grcode=1767,
          grname=None, train_only=True, dataref=None):
    """
	Load the specified dataset, returning a DataFrame of incremental
	losses. If ``dataset`` ="lrdb", additional keyword arguments are used
	to subset the CAS Loss Reserving Database to the records of interest.
	Within the Loss Reserving Database, "loss_key" and "grname" uniquely
	partition losses into 100 record blocks if ``lower_right_ind`` =True,
	otherwise losses are partitioned into 55 record blocks. All available
	combinations of "loss_key" and "grcode" (referred to as "specs")
	can be obtained by calling ``get_lrdb_specs``.
	If ``dataset`` is something other than "lrdb", then only the name of
	the target dataset as a string is required.

	Parameters
	----------
	dataset: str
		Specifies which sample dataset to load. The complete set of sample
		datasets can be obtained by calling ``get_datasets``.

	lob: str
		At present, only option is "comauto". This will be expanded in a
		future release.

	grcode: str
		NAIC company code including insurer groups and single insurers.
		The complete mapping of available grcodes can be obtained by
		calling ``get_lrdb_groups``. Applies only when
		``dataset`` ="lrdb", otherwise parameter is ignored.

	grname: str
		NAIC company name (including insurer groups and single insurers).
		The complete mapping of available grcodes can be obtained by
		calling ``get_lrdb_groups``. Applies only when
		``dataset`` ="lrdb", otherwise parameter is ignored.

	loss_type: str
		Specifies which loss data to load. Can be one of "paid" or
		"incurred". Defaults to "incurred". Note that bulk losses
		have already been subtracted from schedule P incurred losses.
		Applies only when ``dataset`` ="lrdb", otherwise parameter is
		ignored.

	train_only: bool
		If True, the upper-left portion of the triangle will be returned.
		The upper-left portion of the triangle typically consists of
		actual loss experience. If False, the completed triangle, consisting
		of 100 observations is returned. Defaults to True. Applies only when
		``dataset`` ="lrdb", otherwise parameter is ignored.

	dataref: str
	    Location of dataset reference.

	Returns
	-------
	pd.DataFrame
    """
    try:
        dataset_  = dataset.lower()
        datapath = dataref[dataset_]
        loss_data_init = pd.read_csv(datapath, delimiter=",")

    except KeyError:
        print("Specified dataset does not exist: `{}`".format(dataset))

    # Additional filtering/subsetting if dataset="lrdb".
    if dataset=="lrdb":
        loss_field = "incrd_loss" if loss_type.lower().startswith("i") else "paid_loss"
        loss_data = loss_data_init[
            ["loss_key", "grcode", "grname", "origin", "dev", loss_field, "train_ind"]
            ]

        if lob is not None:
            if lob not in loss_data["loss_key"].unique():
                raise ValueError("`{}` is not a valid lob selection.".format(lob))
            loss_data = loss_data[loss_data.loss_key==lob].reset_index(drop=True)

        if grcode is not None:
            if grcode not in loss_data["grcode"].unique():
                raise ValueError("`{}` is not a valid grcode selection.".format(grcode))
            loss_data = loss_data[loss_data.grcode==grcode].reset_index(drop=True)

        if grname is not None:
            if grname not in loss_data["grname"].unique():
                raise ValueError("`{}` is not a valid grname selection.".format(grname))
            loss_data = loss_data[loss_data.grname==grname].reset_index(drop=True)

        if train_only:
            loss_data = loss_data[loss_data.train_ind==1].reset_index(drop=True)

        loss_data = loss_data.rename({loss_field:"value"}, axis=1)

    else: # Specified dataset is not "lrdb".
        loss_data = loss_data_init

    return(loss_data[["origin", "dev", "value"]].reset_index(drop=True))



# Loss Reserving Database utility functions.

def _get_datasets(dataref):
    """
    Generate a list containing the names of available sample datasets.

    Parameters
    ----------
    dataref: str
        Location of dataset reference.

    Returns
    -------
    list
        Names of available sample datasets.
    """
    return(list(dataref.keys()))



def _get_lrdb_lobs(lrdb_path):
    """
    Return the unique "loss_key" entries present in the CAS Loss
    Reserving Database (lrdb).

    Parameters
    ----------
    lrdb_path: str
        Location of CAS loss reserving database.

    Returns
    -------
    list
    """
    lrdb = pd.read_csv(lrdb_path, sep=",")
    lrdb = lrdb["loss_key"].unique()
    return(lrdb.tolist())



def _get_lrdb_groups(lrdb_path):
    """
    Return "grcode"-"grname" mapping present in the CAS Loss
    Reserving Database (lrdb).

    Parameters
    ----------
    lrdb_path: str
        Location of CAS loss reserving database.

    Returns
    -------
    dict
    """
    fields = ["grcode", "grname"]
    lrdb   = pd.read_csv(lrdb_path, sep=",")
    lrdb   = lrdb[fields].drop_duplicates().reset_index(drop=True)
    return({jj:ii for ii,jj in set(zip(lrdb.grname, lrdb.grcode))})



def _get_lrdb_specs(lrdb_path):
    """
    Return a DataFrame containing the unique combinations of "loss_key",
    "grname" and "grcode" from the CAS Loss Reserving Database (lrdb).

    Parameters
    ----------
    lrdb_path: str
        Location of CAS loss reserving database.

    Returns
    -------
    pd.DataFrame
    """
    fields = ["loss_key", "grcode", "grname"]
    lrdb = pd.read_csv(lrdb_path, sep=",")
    lrdb = lrdb[fields].drop_duplicates().reset_index(drop=True)
    lrdb = lrdb.sort_values(by=["loss_key","grcode"])
    return(lrdb)


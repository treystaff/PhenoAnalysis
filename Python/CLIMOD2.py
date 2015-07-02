def read_climod2(path):
    """
    Function for reading CLIMOD2 csv data into pandas dataframe.
    Missing data values are converted to NaN
    Trace values are converted to zero.

    Parameters:
        path: (string) path to climdo2 csv data file.
    Returns:
        A pandas dataframe containing CLIMOD2 data read from path.
            Columns  are labeled according to the first headerline.
            Trace values marked with 'T' are converted to 0.0
    """

    df = pd.read_csv(path, index_col=0, header=0, na_values=['m', 'M'],
                     parse_dates=True, skipinitialspace=True)

    # Get list of columns read
    # cols = list(df.columns.values)

    # Replace 'T' values with 0.0, for now. (T = trace amount)
    df = df.replace('T', 0.0)

    # Make sure all columns are suitable dtype (note, may want to change
    # so that specific cols have dtype best suited for them...)
    df = df.convert_objects(convert_numeric=True)

    # Return the data read from path as a pandas dataframe.
    return df

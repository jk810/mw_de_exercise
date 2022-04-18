import pandas as pd

if __name__ == "__main__":
    # load file into dataframe
    ppl_created_dt = pd.read_csv(
        "people.csv", usecols=["created_dt"], parse_dates=["created_dt"]
    )
    # parse calendar date and count acquisitions
    count = ppl_created_dt["created_dt"].dt.date.value_counts()
    # sort by index, set dtype, and save to csv
    count.sort_index(inplace=True)
    count.index = count.index.astype("datetime64[ns]")
    count.to_csv(
        "acquisition_facts.csv",
        index=True,
        index_label="acquisition_date",
        header=["acquisitions"],
    )

import pandas as pd

if __name__ == "__main__":
    # load files into dataframes
    cons = pd.read_csv(
        "data/cons.csv", usecols=["cons_id", "source", "create_dt", "modified_dt"]
    )
    emails = pd.read_csv(
        "data/cons_email.csv",
        usecols=["cons_id", "cons_email_id", "email", "is_primary"],
    )
    ch_sub = pd.read_csv(
        "data/cons_email_chapter_subscription.csv",
        usecols=["cons_email_id", "chapter_id", "isunsub"],
        dtype={"isunsub": "boolean"},
    )

    # select subsets by filtering primary emails and chapter_id
    emails = emails[emails["is_primary"] == 1.0]
    ch_sub = ch_sub[ch_sub["chapter_id"] == 1.0]

    # inner join by "cons_id" index to yield cons + primary email info
    agg_1 = cons.set_index("cons_id").join(emails.set_index("cons_id"), how="inner")
    # inner join by "cons_email_id" index to yield agg_1 + unsub info
    agg_2 = agg_1.join(
        ch_sub.set_index("cons_email_id"), on="cons_email_id", how="inner"
    )

    # remove, rename, reorder columns, and change dtype
    agg_2 = agg_2.drop(columns=["cons_email_id", "is_primary", "chapter_id"])
    agg_2.rename(
        columns={
            "isunsub": "is_unsub",
            "create_dt": "created_dt",
            "modified_dt": "updated_dt",
        },
        inplace=True,
    )
    agg_2 = agg_2[["email", "source", "is_unsub", "created_dt", "updated_dt"]]
    agg_2.created_dt = pd.to_datetime(agg_2.created_dt, format="%a, %Y-%m-%d %H:%M:%S")
    agg_2.updated_dt = pd.to_datetime(agg_2.updated_dt, format="%a, %Y-%m-%d %H:%M:%S")

    agg_2.to_csv("people.csv", index=False)

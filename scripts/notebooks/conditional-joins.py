# Import libraries
import pandas as pd
import duckdb

# Import `test_data` from `.csv` to a dataframe
test_data = pd.read_csv("data\\test_data.csv")

# Import `geology` from `.csv` to a dataframe
geology = pd.read_csv("data\\geology.csv")


# Write and execute the query
query = """SELECT *
        from test_data
        left join geology
        on test_data.BoreholeID = geology.BoreholeID
        and test_data.Depth >= geology.DepthTop
        and test_data.Depth < geology.DepthBase;"""

df = duckdb.sql(query).df()

# A column named `BoreholeID_2` is created as a copy
# of the original, remove this
df = df.drop(columns="BoreholeID_2")

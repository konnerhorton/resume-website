---
title: Conditional joins for geotechnical data
date: 2023-11-27
---

The geotechnical data management software I use at work has report templates that perform SQL joins to relate test data to geologic strata. For example, if a test is performed at 20 feet, it looks at the strata data (borelogs) and determines what code (like `sandstone` or `limestone`) to assign. Unfortunately, the software only provides reports for limited data types and offer zero customization of the output. And, they do not provide a way for me to write my own SQL queries. Thankfully, I have been learning a little python (specifically the [`pandas`](https://pandas.pydata.org/) library), and found a pretty good solution.

## The problem

If I was able to write a SQL query in the DB manager, it would be a straightforward join on a depth interval and look something like this:

```SQL
SELECT *
from test_data
left join geology
on test_data.BoreholeID = geology.BoreholeID
and test_data.Depth >= geology.DepthTop
and test_data.Depth < geology.DepthBase;
```

The above joins my `geology` table  to my `test_data` table where the `BoreholeID` value matches, and the `Depth` value in the `test_data` table is between `DepthTop` and `DepthBase` in the geology table. `Depth` values that are equal to `DepthTop` will be included, `Depth` values that are equal to `DepthBase` will not be included.

However, I cannot use SQL in the DB manager, but I can export `.csv` files. And since I like to work with the data in `pandas`, I elected to use python. I think this could be done with excel, but it would be a cumbersome set of `XLOOKUP()` functions, and less fun.

## The solution

The `pandas` library allows me to manipulate .csv files similarly to excel and has `.merge()` and `.join()` methods. Unfortunately, neither of these methods allow me to use conditions (everything after the `AND` in the SQL query).

The [`duckDB`](https://duckdb.org/docs/archive/0.9.2/guides/python/sql_on_pandas) library allows me to write SQL query as part of a python script and execute the script on `pandas` DataFrames (which are very similar to a database table). It looks something like this:

```python
# Import libraries
import pandas as pd
import duckdb

# Import `test_data` from `.csv` to a dataframe
test_data = pd.read_csv(test_data.csv)

# Import `geology` from `.csv` to a dataframe
geology = pd.read_csv(geology.csv)
```

`test_data` looks like this:

|Depth| BoreholeID| BulkDensity|
|-----|-----------|------------|
|22.86|BH-001|2.05|
|21.34|BH-001|2.35|
|27.43|BH-001|2.13|
|15.24|BH-002|2.22|

`geology` looks like this:

|BoreholeID|GeologyID|DepthTop|DepthBase|
|---|---|---|---|
|BH-001|Sandstone|23.93|25.45|
|BH-004|Limestone|14.80|17.80|
|BH-004|Sandstone|8.70|11.70|
|BH-005|Limestone|14.78|16.31|

```python
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
```

The resulting dataframe (`df`):

|Depth|BoreholeID|BulkDensity|GeologyID|DepthTop|DepthBase|
|---|---|---|---|---|---|
|18.29|BH-003|2.32|Limestone|17.83|19.35|
|5.33|BH-010|2.36|Limestone|4.57|7.16|
|9.14|BH-011|2.39|Limestone|5.33|11.73|
|2.29|BH-017|2.35|Limestone|0.90|3.05|

There are cases where I might need to join on two intervals (when my `test_data` also has a `DepthTop` and `DepthBase`), the query for this would be:

```SQL
SELECT *
from test_data
left join geology
on test_data.BoreholeID = geology.BoreholeID
and test_data.DepthTop >= geology.DepthTop
and test_data.DepthBase <= geology.DepthBase;
```

**A word of caution:** if your test intervals span a geologic contact (for instance, the upper portion is in `Sandstone` and the lower portion is in `Limestone`), this will not work and you'll need to clean up your data first to make sure test samples do not span a geologic contact. Typically that would be done by splitting the respective sample in two and renaming them `A` and `B` (or something similar).

## In Review

If you need to perform a SQL query on a `pandas` dataframe, use the straightforward solution provided by [`duckDB`](https://duckdb.org/docs/archive/0.9.2/guides/python/sql_on_pandas). The syntax:

```python
df = duckdb.sql(query).df()
```

Where the tables named in `query` are the variable names of the `pandas` dataframes on which you want to execute the query.

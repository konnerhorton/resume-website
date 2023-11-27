---
title: Conditional joins for geotechnical data
date: 2023-11-22
---

The geotechnical data management software I use at work has report templates that perform SQL joins to relate test data to geologic strata. For example, if a test is performed at 20 feet, it looks at the strata data (borelogs) and determines what code (like `sandstone` or `limestone`) to assign. Unfortunately, the software only provides reports for limited data types and offer zero customization of the output. And, they do not provide a way for me to write my own SQL queries. Thankfully, I have been learning a little python (specifically the [`pandas`](https://pandas.pydata.org/) library), and found a pretty good solution.

**The problem:**

If I was able to write a SQL query in the DB manager, it would be a straightforward join on a depth interval and look something like this:

```SQL
SELECT *
FROM test_data
LEFT JOIN geology
ON test_data.BoreholeID = geology.BoreholeID
AND test_data.Depth >= geology.DepthTop
AND test_data.Depth < geology.DepthBase
```

The above joins my `geology` table  to my `test_data` table where the `BoreholeID` value matches, and the `Depth` value in the `test_data` table is between `DepthTop` and `DepthBase` in the geology table. `Depth` values that are equal to `DepthTop` will be included, `Depth` values that are equal to `DepthBase` will not be included.

Since I can't use SQL in the DB manager, I elected to use python (I think this could be done with excel, but it would be a cumbersome set of `XLOOKUP()` functions, and less fun).

**The solution:**

The `pandas` library allows me to manipulate .csv files similarly to excel and has `.merge()` and `.join()` methods. Unfortunately, neither of these methods allow me to use conditions (everything after the `AND` in the SQL query).

The [`pandasql`](https://github.com/yhat/pandasql/) library allows me to write SQL query as part of a python script and execute the script on `pandas` DataFrames (the `pandas` table). It looks something like this:

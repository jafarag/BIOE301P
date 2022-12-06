# HW2

SQL & pandas

## Goals

The goal of this homework assignment is to:

* work with pandas DataFrames
* learn the basics of SQL
* work with sqlite database files
* work with Google BigQuery tables
* visualize data from SQL databases
* optimize data transfer bandwidth 

As before, homework must be completed in Markdown, pushed to a private GitLab repository, rendered to PDF, and then saved back into the repository. For any question involving code, either include the .py file used answer the question and indicate this filename in the markdown file for that question or directly include the code in the markdown file in a code block section for that question number. Do not include .ipynb files in your homework. A zip file of the repository (including markdown, PDF, any other work files, and excluding the .git directory) must be submitted for peer grading. Do not submit ipynb files, submit validated, working [code blocks](https://python-markdown.github.io/extensions/fenced_code_blocks) for specific questions within your Markdown file with appropriate [syntax highlighting](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks#syntax-highlighting).

This homework page may be updated later with more questions. Do not simply fork the repository. For this assignment, clone this repository directly, and then set up a second remote with which you push your changes to. This will allow you to pull changes from the originating repository and continue to push changes to your private repository. 

## Video Training

* [Pandas Essential Training](https://www.linkedin.com/learning/pandas-essential-training)
    * This entire tutorial is relevant
    * Don't install anaconda, just use Colab
    * Unzip the exercise files and rclone the directory to Google Drive so you can directly open up the ipynb files in Colab
* [SQL Essential Training](https://www.linkedin.com/learning/sql-essential-training-3)
    * Install and use [sqqlitestudio](https://sqlitestudio.pl), it is an excellent tool
    * Only sections 1-8 are necessary
    * Sections 9+ are concepts less commonly used in research
* [Using BigQuery](https://www.youtube.com/watch?v=qqbYrQGSibQ)
    * Older video with the older UI, but the ideas are the same
    * less critical to review if the prior SQL ideas understood
    * access BigQuery via [console.cloud.google.com](http://console.cloud.google.com)

## Relevant Documentation

* [Pandas](https://pandas.pydata.org)
* [SQLite](https://www.sqlite.org)
    * [SQLite Overview](https://www.sqlite.org/about.html)
    * [Python SQLite library](https://docs.python.org/3/library/sqlite3.html)
    * [W3Schools SQL Tutorial](https://www.w3schools.com/sql)
* [BigQuery](https://cloud.google.com/bigquery/docs)

## Questions

1. Epidemic visualization: tabular datasets
    - For this question, please work on your own and not with any partners.
    - Here, you will perform a visualization using pandas/SQL as the backend data source in a tabular format.
    - Many of the common plotting libraries ([seaborn](https://seaborn.pydata.org/index.html), [holoviews](https://holoviews.org/getting_started/Tabular_Datasets.html), [plotly express](https://plotly.com/python/plotly-express), etc) [work best](https://pyviz-dev.github.io/pyviz/tutorial/Working_with_Tabular_Data.html) when data is in [tidy format](https://vita.had.co.nz/papers/tidy-data.pdf) (note, [seaborn](https://seaborn.pydata.org/tutorial/data_structure.html#long-form-vs-wide-form-data) and [plotly express](https://plotly.com/python/wide-form) also support wide-form data).
    - Use the following function to generate a tidy pandas Dataframe for US data about the COVID-19 pandemic:
        ```python
        def tidy_jhu_raw(value_type='cases'):
    
            URLs = {'cases'  : 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', 
                    'deaths' : 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv' }
            id_var_idx = {'cases' : 11, 'deaths' : 12}
    
            df = pd.read_csv(URLs[value_type])
    
            # convert to tidy format by unpivoting data
            return pd.melt(df, id_vars = df.columns[0:id_var_idx[value_type]], var_name = 'date').assign(value_type = value_type).astype({'date': 'datetime64[ns]'})
        ```
    - Use the [split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html) operations of pandas to group counties up by state to aggregate state-level data.
    - Create a [seaborn](https://seaborn.pydata.org) [scatterplot or lineplot](https://seaborn.pydata.org/tutorial.html) of a given state's timeseries cases or death data. Save this as a PNG and include it in your repository as a rendered image in your homework markdown file.
    - Use Colab's support for [interact](https://colab.research.google.com/github/jupyter-widgets/ipywidgets/blob/master/docs/source/examples/Using%20Interact.ipynb) to create a similar timeseries plot, but now using a plotly [line chart](https://plotly.com/python/line-charts) or [scatter plot](https://plotly.com/python/line-and-scatter) for a given state that is controlled by an interactive dropdown menu to choose the state to plot.
        - Bonus challenge (ungraded): also use two checkboxes to define which value to plot: cases or/and deaths
    - Save these dataframes as separate tables in a single sqlite database file using panda's [`to_sql()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html)
        - The following code will help you set up an sqlite3 database:
            ```python
            import sqlite3
            con_sql3 = sqlite3.connect('</path/to/sqlite3.db>') # this database will be created if it does not exist
            ```
        - Verify that this was written down correctly using sqlitestudio and include a screenshot in your homework.
    - Upload this database file to Google Drive and your Google Storage bucket
    - Use the [`load_table_from_dataframe()`](https://googleapis.dev/python/bigquery/latest/usage/pandas.html#load-a-pandas-dataframe-to-a-bigquery-table) function from the BigQuery library to load both tables into BigQuery
        - This requires first [authenticating as an end user](https://cloud.google.com/docs/authentication/end-user) before you can use the [BigQuery Python API](https://googleapis.dev/python/bigquery/latest/index.html)
        - The following code sets up a working BigQuery client on FarmShare:
            ```python
            import os
            from google_auth_oauthlib import flow
            from google.cloud import bigquery
            appflow = flow.Flow.from_client_secrets_file(os.path.join(os.environ['BIOE301P_HOME'], 'google-oauth2.json'), scopes=["https://www.googleapis.com/auth/bigquery"], redirect_uri='https://web.stanford.edu/group/bil/cgi-bin/gauth_cb.py')
            print("Paste the following URL into a browser, choose your Stanford Google account, then copy the resulting code\n{}".format(appflow.authorization_url()[0]))
            code = input("Paste code from browser: ")
            appflow.fetch_token(code = code)
            client = bigquery.Client(project = 'soe-bioe-301p', credentials = appflow.credentials)
            ```
        - The following code sets up a working BigQuery client in Colab:
            ```python
            import os
            from google.colab import auth
            from google.cloud import bigquery
            os.environ['USE_AUTH_EPHEM'] = '0'
            auth.authenticate_user()
            client = bigquery.Client(project = 'soe-bioe-301p')
            ```
        - Bonus challenge (ungraded): Use [Google Data Studio](https://datastudio.google.com) to create a visualization of the data you uploaded to BigQuery.
    - Use [`df_to_sheet()`](https://gspread-pandas.readthedocs.io/en/latest/gspread_pandas.html#gspread_pandas.spread.Spread.df_to_sheet) of [gspread-pandas](https://gspread-pandas.readthedocs.io/en/latest/index.html) to upload the dataframes to separate sheets of a single Google Sheets spreadsheet and document this in your homework with a screenshot.
        - Note, this will require authenticating `gspread-pandas` with your Google account.
        - The following code sets up a working gspread-pandas client on FarmShare:
            ```python
            import os
            from google_auth_oauthlib import flow
            import gspread_pandas as gspd
            appflow = flow.Flow.from_client_secrets_file(os.path.join(os.environ['BIOE301P_HOME'], 'google-oauth2.json'), scopes=['openid', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/spreadsheets'], redirect_uri='https://web.stanford.edu/group/bil/cgi-bin/gauth_cb.py')
            print("Paste the following URL into a browser, choose your Stanford Google account, then copy the resulting code\n{}".format(appflow.authorization_url()[0]))
            code = input("Paste code from browser: ")
            appflow.fetch_token(code = code)
            client = gspd.Client(creds = appflow.credentials) # pass this client object in to all Spread() calls
           ``` 
        - The following code sets up a working gspread-pandas client on Colab:
            ```python
            !pip install gspread-pandas
            import os
            from google.colab import auth
            import google.auth
            import gspread_pandas as gspd
            os.environ['USE_AUTH_EPHEM'] = '0'
            auth.authenticate_user()
            credentials, project_id  = google.auth.default()
            client = gspd.Client(creds = credentials)
            ```
2. BigQuery Public Data
    - Choose an interesting dataset from the [BigQuery public dataset](https://cloud.google.com/bigquery/public-data)
    - Describe the general structure of the dataset
    - How many rows are there? How did you determine this?
    - What is the size of the dataset? How did you determine this?
    - Use the [`to_dataframe`](https://googleapis.dev/python/bigquery/latest/usage/pandas.html#retrieve-bigquery-data-as-a-pandas-dataframe) method to fetch some interesting portion of this data and then plot the result using [plotnine](https://datacarpentry.org/python-ecology-lesson/07-visualization-ggplot-python/index.html) and save it to a PNG in your homework.
    - Copy at least 100 rows of your dataset to sqlite and Google Sheets, screenshoting the results.
3. Understanding bandwidth
    - For this question, please work on your own and not with any partners.
    - This question is designed to help you think about data transfer rates and bandwidth
    - Before starting, redo your rclone Google Storage bucket remote to use the class OAuth tokens (if you are not already using them):
        - `client_id` : `496632253402-oukauk06a4mas3lje3hgs24eur832gi0.apps.googleusercontent.com`
        - `client_secret` : `WqA-m1Mj_z5kfMnwbtj3QuDO`
    - Create 11 random files on FarmShare. The first ten are 1G each, and the 11th is 10G. Place the 1G files in one directory and the 10G file in a different directory.
        - Files with random data can be creating using `/dev/urandom`
        - To create a 20M random file, use the following `dd` command: `dd if=/dev/urandom of=<file> bs=1M count=20`
        - Note: when using `dd`, it is generally best to keep the read/write parameters (the value of `bs`) less than 10M
    - Use rclone to upload the 10 1G files to Google Drive (as a single command), and then repeat with the 10G file. Is there a difference in data transfer rate? What if you use/set/change the [`--transfers`](https://rclone.org/docs/#transfers-n) flag?
    - Repeat, only now upload to your Google Storage bucket. Same set of questions.
    - Repeat some of these transfers, only this time copy the random files to your local computer and use rclone from your local computer. Is it faster or slower than FarmShare? Why do you think this may be the case?

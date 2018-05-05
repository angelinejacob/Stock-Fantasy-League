Data is collected via that NASDAQ website and the AlphaVantage API, and used to 
allow stock screening based on symbol and name. In the future, this data 
collection will be further automated and allow for technical screening using 
quantitative data.

To run the data collection setup script, first download the CSV file at the 
following link:
https://www.nasdaq.com/screening/companies-by-industry.aspx?&render=download

There is already a copy available in this folder. 

After you have done this, run ‘python update_stock_db.py’.

The process of fetching and storing data will fill the database table 
with stock symbols and associated company names. 

The above process only needs to be done once to initialize the data table. Once 
the table has been initialized, it will automatically be updated every day at midnight. In order to 
manually update the table, you can execute ‘python update_stock_db.py’. This 
process will take several minutes to complete. 

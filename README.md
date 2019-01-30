# Zerodha Task - Shivam Kohli

This repository contains python code for the task given.

## Description of the task
BSE publishes a "Bhavcopy" file every day here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx,
Download the Equity bhavcopy zip from the above page- Extract and parse the CSV file in it- The records were written into Redis.
A simple CherryPy python web application that:- Renders an HTML5 + CSS3 page that lists the top 10 stock entries from the Redis DB in a table and has a search box that lets you search the entries by the 'name' field in Redis and renders it in a table

## Installation

For the installation. download the required packages

```bash
pip3 install -r requirements.txt
```

## Usage

```python
python3 app.py
```

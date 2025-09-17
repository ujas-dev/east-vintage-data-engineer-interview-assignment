# Data Engineering Assignment - Company XYZ Sales Analysis

## Overview
This project analyzes sales data for Company XYZ's promotional campaign targeting customers aged 18-35. The solution provides two different approaches to extract and process the data: pure SQL and Pandas-based analysis.

## Assignment Requirements
- Connect to SQLite3 database
- Extract total quantities of items (x, y, z) bought by customers aged 18-35
- Provide both SQL and Pandas solutions
- Export results to CSV with semicolon delimiter
- Handle NULL quantities and zero purchases appropriately

## Database Schema
The database contains two tables:

### customers
- `customer_id` (INTEGER, PRIMARY KEY)
- `age` (INTEGER, NOT NULL)

### sales
- `sale_id` (INTEGER, PRIMARY KEY)
- `customer_id` (INTEGER, FOREIGN KEY)
- `item` (TEXT, NOT NULL)
- `quantity` (TEXT, can be NULL)

## Business Rules
1. A sales receipt can have multiple items in an order.
2. For every order, the clerk records all quantities for all items, including items not bought (which they denote with quantity=NULL).
3. Each customer can do multiple sales transactions, and has his/her age stored in a database.

## Test Case Verification
The solution includes a built-in test case with:
- Customer 1 (age 21): 10 units of Item X across multiple transactions
- Customer 2 (age 23): 1 unit each of Items X, Y, Z
- Customer 3 (age 35): 2 units of Item Z across two transactions
- Additional customers outside age range (excluded from results)

## Files Generated
- `sql_output.csv`: Results from pure SQL solution
- `pandas_output.csv`: Results from Pandas solution
- `company.db`: SQLite database with sample data

## Technical Notes
- Uses SQLite3 for database operations (built into Python)
- Pandas for data manipulation and analysis
- CSV output uses semicolon (';') as delimiter as specified
- Handles edge cases like NULL values and type conversions
- Integer quantities only (no decimals)

## Author
Created for Eastvantage Data Engineer Assignment

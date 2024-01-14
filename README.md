# Equal-Weight S&P 500 Screener

This Python script builds an equal-weight alternative to the S&P 500 index, assigning the same weight to each company in the index. The program retrieves real-time stock information, calculates the number of shares to buy for each stock based on a user-defined portfolio size, and generates a recommended trades Excel file.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python
- pandas
- requests
- xlsxwriter

### Installation

Install the required Python packages using:

```bash
pip install pandas requests xlsxwriter 
```

## Usage

1. Clone the repository.
2. Run the script: python equal_weight_sp500_screener.py.
3. Enter the value of your portfolio when prompted.
4. The program will generate a recommended trades Excel file (recommended_trades.xlsx).

## Features

- Real-Time Data: Utilizes the Yahoo Finance API to fetch real-time stock information.
- Equal-Weighting: Creates an equal-weight version of the S&P 500 index.
- Portfolio Recommendation: Calculates the number of shares to buy for each stock based on the user's portfolio size.
- Excel Output: Generates an Excel file with recommended trades.

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

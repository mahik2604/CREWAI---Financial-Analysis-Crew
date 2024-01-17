
# CREWAI - Financial Analysis Crew


## Overview

`crewai.py` is a Python script designed for financial analysis tasks, utilizing the CREWAI library. This script acts as a financial analysis crew, combining the expertise of different agents to provide comprehensive insights into a specified company's financial health, market performance, and investment recommendations.

## Features

- **Dynamic Financial Analysis:** Utilizes various tools to gather financial data, market trends, and historical stock performance.
- **Integration with APIs:** Connects with external APIs such as Google Search, Yahoo Finance, and OpenAI for comprehensive research.
- **Structured Workflow:** The script follows a structured workflow, with different agents assigned specific roles for in-depth analysis.

## Prerequisites

- Python 3.6 or higher
- CREWAI library (`pip install crewai pandas-ta unstructured yfinance`)

## Getting Started

1. Clone this repository:

    ```
    git clone https://github.com/your-username/crewai-financial-analysis.git
    cd crewai-financial-analysis
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Set `OPENAI_API_KEY` to your OpenAI API key.

4. Run the script:

    ```
    python crewai.py
    ```

5. Enter the company you want to analyze when prompted.

## Agents and Tools

- **Research Analyst:** Gathers and interprets data from news, company announcements, and market sentiments.
- **Financial Analyst:** Conducts a thorough analysis of the stock's financial health and market performance.
- **Investment Advisor:** Provides strategic investment advice based on various analytical insights.

## Tasks

- **Research:** Collect and summarize recent news articles, press releases, and market analyses.
- **Financial Analysis:** Examine key financial metrics and analyze the stock's performance in comparison to peers.
- **Filings Analysis:** Analyze key sections of filings, extract relevant data, and highlight significant findings.
- **Recommendation:** Combine insights to form a comprehensive investment recommendation.

## Tips Section

- **Incentive:** A $10,000 commission is offered for the best work.

## Example Usage

```
python crewai.py
```

Enter the company you want to analyze when prompted.

## License

This project is licensed under the [MIT License](LICENSE).

---

# -*- coding: utf-8 -*-
"""CREWAI
"""

!pip install crewai pandas-ta unstructured

import json
import os
import requests
from crewai import Agent, Task
from langchain.tools import tool
import yfinance as yf
from langchain.utilities import GoogleSearchAPIWrapper
from datetime import datetime, timedelta
from unstructured.partition.html import partition_html
from crewai import Crew
from textwrap import dedent
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] ='key'
openai_api_key = os.environ['OPENAI_API_KEY']

class HistData():
  @tool("Get Financial Info")
  def get_fin_info(ticker):
    """retrieves Financial info of a company based on ticker symbol"""
    if not ticker.endswith('.NS'):
        ticker = ticker + '.NS'
    tick = yf.Ticker(ticker)
    tick.info


  @tool("Get Historical data")
  def historical_data(ticker,period='1y'):
    """Retrieves historical stock data based on the ticker symbol."""
    if not ticker.endswith('.NS'):
        ticker = ticker + '.NS'

    ticker_data = yf.Ticker(ticker)
    recent = ticker_data.history(period=period)

    return recent

  @tool("Search current stock price")
  def get_current_stock_price(ticker,period='1mo'):
      """Method to get current stock price"""

      if not ticker.endswith('.NS'):
        ticker = ticker + '.NS'
      data = yf.Ticker(ticker)
      df = data.history(period=period)
      return {"price": df.iloc[0]["Close"], "currency": data.info["currency"]}

  @tool("Evaluate current performance of a stock")
  def stock_performance(ticker, period=30):
      """Method to get stock price change in percentage"""
      if not ticker.endswith('.NS'):
        ticker = ticker + '.NS'
      past_date = datetime.today() - timedelta(days=period)
      ticker_data = yf.Ticker(ticker)
      history = ticker_data.history(start=past_date)
      old_price = history.iloc[0]["Close"]
      current_price = history.iloc[-1]["Close"]
      return {"percent_change": ((current_price - old_price) / old_price) * 100}

class CalculatorTools():

  @tool("Make a calcualtion")
  def calculate(operation):
    """Useful to perform any mathematica calculations,
    like sum, minus, mutiplcation, division, etc.
    The input to this tool should be a mathematical
    expression, a couple examples are `200*7` or `5000/2*10`
    """
    return eval(operation)

class SearchTools():
  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet about a a given topic and return relevant results"""
    search_tool = GoogleSearchAPIWrapper(google_cse_id = 'google_cse_id', google_api_key='google_api_key',k=5)
    return search_tool.run(query)


  @tool("Search news on the internet")
  def search_news(query):
    """Useful to search news about a company, stock or any other
    topic and return relevant results"""""
    search_news_tool = GoogleSearchAPIWrapper(google_cse_id = 'google_cse_id', google_api_key='google_api_key',k=5)
    return search_news_tool.run(query)


from crewai import Agent

# from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
      llm=ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo", openai_api_key = 'key'),
      verbose=True,
      tools=[
        SearchTools.search_internet,
        CalculatorTools.calculate,
        HistData.historical_data,
        HistData.get_current_stock_price,
        HistData.stock_performance,
    ]
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements,
      and market sentiments. Now you're working on a super
      important customer""",
      llm=ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo", openai_api_key = 'key'),
      verbose=True,
      tools=[
        SearchTools.search_internet,
        SearchTools.search_news,
        # YahooFinanceNewsTool(),
        HistData.historical_data,
        HistData.get_current_stock_price,
        HistData.stock_performance
      ]
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      llm=ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo", openai_api_key = 'key'),
      verbose=True,
      tools=[
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
        # YahooFinanceNewsTool()
      ]
    )

from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
  def research(self, agent, company):
    return Task(description=dedent(f"""
        Collect and summarize recent news articles, press
        releases, and market analyses related to the stock and
        its industry.
        Pay special attention to any significant events, market
        sentiments, and analysts' opinions. Also include upcoming
        events like earnings and others.

        Your final answer MUST be a report that includes a
        comprehensive summary of the latest news, any notable
        shifts in market sentiment, and potential impacts on
        the stock.
        Also make sure to return the stock ticker.

        {self.__tip_section()}

        Make sure to use the most recent data as possible.

        Selected company by the customer: {company}
      """),
      agent=agent
    )

  def financial_analysis(self, agent):
    return Task(description=dedent(f"""
        Conduct a thorough analysis of the stock's financial
        health and market performance.
        This includes examining key financial metrics such as
        P/E ratio, EPS growth, revenue trends, and
        debt-to-equity ratio.
        Also, analyze the stock's performance in comparison
        to its industry peers and overall market trends.

        Your final report MUST expand on the summary provided
        but now including a clear assessment of the stock's
        financial standing, its strengths and weaknesses,
        and how it fares against its competitors in the current
        market scenario.{self.__tip_section()}

        Make sure to use the most recent data possible.
      """),
      agent=agent
    )

  def filings_analysis(self, agent):
    return Task(description=dedent(f"""
        Analyze the Stock.
        Focus on key sections like Management's Discussion and
        Analysis, financial statements, insider trading activity,
        and any disclosed risks.
        Extract relevant data and insights that could influence
        the stock's future performance.

        Your final answer must be an expanded report that now
        also highlights significant findings from these reports,
        including any red flags or positive indicators for
        your customer.{self.__tip_section()}
      """),
      agent=agent
    )

  def recommend(self, agent):
    return Task(description=dedent(f"""
        Review and synthesize the analyses provided by the
        Financial Analyst, Research Analyst and Private Investment Advisor.
        Combine these insights to form a comprehensive
        investment recommendation.

        You MUST Consider all aspects, including financial
        health, market sentiment, and qualitative data.

        Make sure to include a section that shows insider
        trading activity, and upcoming events like earnings.

        Your final answer MUST be a recommendation for your
        customer. It should be a full super detailed report, providing a
        clear investment stance and strategy with supporting evidence.
        Make it pretty and well formatted for your customer.
        {self.__tip_section()}
      """),
      agent=agent
    )

  def __tip_section(self):
    return "If you do your BEST WORK, I'll give you a $10,000 commision!"

class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  company = input(
    dedent("""
      What is the company you want to analyze?
    """))

  financial_crew = FinancialCrew(company)
  result = financial_crew.run()
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)




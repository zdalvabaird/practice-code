import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import yfinance as yf

def create_stock_data(stock_symbol, start_date, end_date, output_file):
    # Download historical stock data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Reset the index to include 'Date' as a column
    stock_data.reset_index(inplace=True)

    # Save the data to a CSV file
    stock_data.to_csv(output_file, index=False)


def preprocess_stock_data(stock_data):
    """
    Preprocess the stock price data for time series analysis.

    Parameters:
    stock_data (pd.DataFrame): A DataFrame containing stock price data.

    Returns:
    pd.Series: A time series of stock prices with 'Date' as the index.
    """
    # Convert data into series with the date as the index and the price as the value
    prices = stock_data['Close'].values
    dates = pd.to_datetime(stock_data['Date'])
    stock_data.dropna(subset=['Date', 'Close'], inplace=True)  # Cleans data, if any incomplete values it deletes them
    stock_series = pd.Series(prices, index=dates)

    return stock_series


def train_arima_model(stock_series, prq=(0,1,7)):
    """
    Train an ARIMA model for stock price forecasting.

    Parameters:
    stock_series (pd.Series): A time series of stock prices.
    order (tuple): ARIMA order parameters (p, d, q).

    Returns:
    statsmodels.tsa.arima.ARIMAResultsWrapper: Trained ARIMA model.
    """

    model = ARIMA(stock_series, order=prq)
    model_fit = model.fit()

    return model_fit

def plot_stock_forecast(stock_series, model_fit, forecast_period, end_date):
    """
    Plot historical and forecasted stock prices.

    Parameters:
    stock_series (pd.Series): A time series of historical stock prices.
    model (statsmodels.tsa.arima.ARIMAResultsWrapper): Trained ARIMA model.
    forecast_period (int): Number of time steps to forecast into the future.

    Returns:
    None
    """
    forecast = model_fit.get_forecast(steps=forecast_period)
    forecasted_values = forecast.predicted_mean

    forecast_dates = pd.date_range(start=end_date, periods=forecast_period + 1, closed='right')

    # Plot historical and forecasted stock prices
    plt.figure(figsize=(12, 6))
    plt.plot(stock_series.index, stock_series.values, label='Historical', color='blue')
    plt.plot(forecast_dates, forecasted_values, label='Forecasted', color='red')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title('Historical and Forecasted Stock Prices')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    stock_symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2022-01-01'
    output_file = 'stock_price_data.csv'
    forecast_period = 30  # Forecast stock prices for the next 30 days
    
    # Collect and save the stock data
    create_stock_data(stock_symbol, start_date, end_date, output_file)
    
    stock_data = pd.read_csv(output_file)  # Load the collected data

    stock_series = preprocess_stock_data(stock_data)  # Convert data into series with date as index and price as value
    # Test to plot data
    # plt.plot(dates, prices)
    # plt.show()
    model_fit = train_arima_model(stock_series)

    plot_stock_forecast(stock_series, model_fit, forecast_period, end_date)


if __name__ == "__main__":
    main()

import numpy as np
import pandas as pd
from skyfield.api import Topos, Loader
from datetime import datetime
import plotly.graph_objects as go
import yfinance as yf
from ipywidgets import interact, widgets, HBox, VBox, interactive, Layout

# (1) Solar System Functions (sky.py)
# ...

# (2) Stock Market Functions (stockmarket.py)
# ...

# Display solar system plot
def display_solar_system_plot(date):
    positions = compute_positions(date)
    stars = generate_stars()
    solar_system_fig = create_solar_system_plot(positions, stars)
    return solar_system_fig

# Display stock market plot
def display_stock_market_plot(symbols_input, date):
    symbols = [symbol.strip() for symbol in symbols_input.split(',')]
    stock_data = download_stock_data(symbols)
    date_range = (pd.Timestamp('1900-01-01'), date)
    stock_market_fig = create_stock_market_plot(stock_data, symbols, date_range)
    return stock_market_fig

# Input widgets
date_slider = widgets.DateSlider(min=start_date, max=end_date, value=start_date, description='Date:')
symbols_input = widgets.Text(value='AAPL,MSFT,GOOGL', description='Symbols:')

# Create interactive plots
solar_system_plot = interactive(display_solar_system_plot, date=date_slider)
stock_market_plot = interactive(display_stock_market_plot, symbols_input=symbols_input, date=date_slider)

# Set width and height of the plots
plot_layout = Layout(width='50%', height='600px')
solar_system_plot.layout = plot_layout
stock_market_plot.layout = plot_layout

# Layout
layout = HBox([solar_system_plot, stock_market_plot])
display(layout)

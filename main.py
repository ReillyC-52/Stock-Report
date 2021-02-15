import pandas as pd
import os
import numpy as np
import yfinance as yf
from Stock_Profile import Stock_Profile
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

Valid_Stocks_List = open("Valid_Stock_List.txt","r")
List = Valid_Stocks_List.read()
IO_Stock_List = List.split(",")
IO_Valid_Check = False

while not IO_Valid_Check:
    value = input('PLEASE ENTER ANY LIST OF VALID STOCK ABRRIVATIONS SEPERATED WITH A COMMA  \n\n')
    IO_Input_Text= value.split(",")
    IO_Input_Text = [x.upper() for x in IO_Input_Text]
    print(IO_Input_Text)
    for abbrv in IO_Input_Text:
        if abbrv in IO_Stock_List:
            IO_Valid_Check = True 
        else :
            IO_Valid_Check = False
            print(f"VALUE {abbrv} IS NOT A VALID STOCK\n")

for stock in IO_Input_Text:
    max_data = yf.download(stock, period="max")
    hourly_data = yf.download(stock, period="5d",interval="1h")
    market_time = [9,10,11,12,13,14,15]
    time_count = 0
    time_Stamp_Fix = []
    for index in hourly_data.index:
        Date = str(index)
        Date_Y, Date_M, Date_D = Date[0:4], Date[5:7], Date[8:10]
        Date_Y, Date_M, Date_D = int(Date_Y), int(Date_M), int(Date_D)
        time_Stamp_Fix.append(pd.Timestamp(year=Date_Y, month=Date_M, day=Date_D,
        hour=market_time[time_count], minute=30))

        if time_count == 6:
            time_count = 0
        else:
            time_count = time_count + 1

    hourly_data['TimeStamp'] = time_Stamp_Fix
    hourly_data = hourly_data.set_index('TimeStamp')
    ticker = yf.Ticker(stock)
    Current_Stock_Profile = Stock_Profile(max_data, hourly_data ,ticker)

    print(f"GRABBING DATA FOR STOCK {Current_Stock_Profile.shortName}\n")
    fig = make_subplots(rows=2, cols=2,
                    subplot_titles=("Daily", "Week To Date",
                                    "Month To Date", "Quarter To Date"),
                        )

    fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.',
                      yaxis2_tickprefix = '$', yaxis2_tickformat = ',.',
                      yaxis3_tickprefix = '$', yaxis3_tickformat = ',.',
                      yaxis4_tickprefix = '$', yaxis4_tickformat = ',.'
                     )


    CS_df_Daily   = Current_Stock_Profile.Daily_DateFrame
    CS_df_Month   = Current_Stock_Profile.MonthToDate_DataFrame
    CS_df_Weekily = Current_Stock_Profile.WeekToDate_DataFrame
    CS_df_Quarter = Current_Stock_Profile.QuarterToDate_DataFrame


    fig.add_trace(go.Candlestick(x=CS_df_Daily.index,
                open=CS_df_Daily['Open'],
                high=CS_df_Daily['High'],
                low=CS_df_Daily['Low'],
                close=CS_df_Daily['Close']),
                row = 1, col = 1)

    fig.add_trace(go.Candlestick(x=CS_df_Weekily.index,
                open=CS_df_Weekily['Open'],
                high=CS_df_Weekily['High'],
                low=CS_df_Weekily['Low'],
                close=CS_df_Weekily['Close']), row = 1, col = 2)


    fig.add_trace(go.Candlestick(x=CS_df_Month.index,
                open=CS_df_Month['Open'],
                high=CS_df_Month['High'],
                low=CS_df_Month['Low'],
                close=CS_df_Month['Close']),row = 2, col = 1)

    fig.add_trace(go.Candlestick(x=CS_df_Quarter.index,
                open=CS_df_Quarter['Open'],
                high=CS_df_Quarter['High'],
                low=CS_df_Quarter['Low'],
                close=CS_df_Quarter['Close']), row = 2, col = 2)

    fig.update_layout(height=750, width=1200,showlegend=False,
                  title_text=Current_Stock_Profile.shortName)

    fig.update_xaxes(rangeslider_visible=False)

    if not os.path.exists("images"):
        os.mkdir("images")
    fileName = "images/Chart_{}.png".format(Current_Stock_Profile.shortName)
    fig.write_image(fileName)

    CS_df_Historic =  Current_Stock_Profile._5YR_DataFrame
    CS_Close = CS_df_Historic["Close"].copy()
    CS_Open = CS_df_Historic["Open"].copy()
    CS_df_Historic['Percentage_Change'] = (CS_Close / CS_Open ) - 1
    CS_df_Historic['Percentage_Change'] = CS_df_Historic['Percentage_Change'] * 100
    # print(str(CS_df_Historic))


    print(CS_df_Historic["Percentage_Change"].describe())
    Temp_DF = CS_df_Historic["Percentage_Change"].iloc[-1:]
    compare_DF = CS_df_Historic[CS_df_Historic.Percentage_Change > Temp_DF[0]]
    percentile_Change = compare_DF["Percentage_Change"].count() / CS_df_Historic["Percentage_Change"].count()

    print("\n\n{} Percentage Change Today VS Historic\n".format(Current_Stock_Profile.shortName))
    print("Change On {} : {}".format(Current_Stock_Profile.Current_Date, Temp_DF[0]))
    print("This percentage change is in the {} percentile over the last 5 years\n".format(percentile_Change))

    ##Dividend Yield (Current Trailing vs 5 Year)
    # fiveYearAvgDividendYield
    # dividendRate -> 2.81
    ##Earnings Per Share Trailing and Forwar
    # 84  forwardEps -> 1.41
    # 96  trailingEps -> 1.201
    # Price / EPS
    # P/B
    # Value per Share / book Value
    # PEG
    # Price/EPS Divide that by earningsQuarterlyGrowth
    Div_Yield = Current_Stock_Profile.dividendYield
    Five_Yr_Div_Yield = Current_Stock_Profile.fiveYearAvgDividendYield
    For_EPS = Current_Stock_Profile.forwardEps
    Trail_EPS = Current_Stock_Profile.trailingEps
    EarnQuarter_Growth = Current_Stock_Profile.earningsQuarterlyGrowth
    current_Price = CS_df_Daily["Close"].iloc[-1]

    # print("\n\nCurrent Dividend Rate {} ||  5 Year Average Dividend Rate {}\n\n".format(Div_Rate,Five_Yr_Div_Rate))
    # For_PE = current_Price / For_EPS
    # Trail_PE = current_Price / Trail_EPS 
    # print("Forward EPS {} || Trailing EPS {} \n\n".format(For_PE, Trail_PE))
    # PEG = For_PE / EarnQuarter_Growth

    # print("PEG : {} \n\n".format(PEG))



    print("\n\n{} Dividend Rate \n".format(Div_Yield))
    print("\n\n{} fiveYearAveDividendYield\n".format(Five_Yr_Div_Yield))
    print("\n\n{} forwardEPS \n".format(Current_Stock_Profile.forwardEps))
    print("\n\n{} trailingEPS\n".format(Current_Stock_Profile.trailingEps))
    print("\n\n{} earningsQuaterkyGrowth \n".format(Current_Stock_Profile.earningsQuarterlyGrowth))

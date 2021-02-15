from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class Stock_Profile:

    def __init__(self, max_df, hourly_df,ticker=[]):
        
        self.Max_DataFrame = max_df
        self.Hourly_DataFrame = hourly_df
        self.Valid_Dates = []
        self.Info_Dict = ticker.info
        timeStamps = self.Max_DataFrame.index.tolist()
        for time in timeStamps:
            self.Valid_Dates.insert(0,"{}-{}-{}".format(time.strftime("%Y"),time.strftime("%m"),time.strftime("%d")))
        
        self.Latest_DataFrame = self.Hourly_DataFrame.tail(1)
        Current_timeStamp = self.Latest_DataFrame.index.tolist()
        Current_timeStamp = Current_timeStamp[0]

        self.Current_Date = pd.Timestamp(year = int(Current_timeStamp.strftime("%Y")), month=int(Current_timeStamp.strftime("%m")), day= int(Current_timeStamp.strftime("%d")))
        self.Daily_DateFrame = self.Hourly_DataFrame.loc[self.Current_Date :]
       
        _5yr_timeStamp = Current_timeStamp - timedelta(weeks=260)
        _5Yr_Date = "{}-{}-{}".format(_5yr_timeStamp.strftime("%Y"),_5yr_timeStamp.strftime("%m"),_5yr_timeStamp.strftime("%d"))
        self._5YR_DataFrame = self.Max_DataFrame.loc[_5Yr_Date :]
        
        Quarter_Check = {}
        Quarter_Check.update(dict([i, ["01","01"]] for i in ["01","02","03"]))
        Quarter_Check.update(dict([i, ["04","01"]] for i in ["04","05","06"]))
        Quarter_Check.update(dict([i, ["07","01"]] for i in ["07","08","09"]))
        Quarter_Check.update(dict([i, ["10","01"]] for i in ["10","11","12"]))
        QTD_Array = Quarter_Check.get(Current_timeStamp.strftime("%m"))
        QTD_Month,QTD_Day = QTD_Array[0],QTD_Array[1]
        
        QTD_Date = "{}-{}-{}".format(Current_timeStamp.strftime("%Y"),QTD_Month,QTD_Day)
        self.QuarterToDate_DataFrame = self.Max_DataFrame.loc[QTD_Date :]
        
        MTD_Date = "{}{}{}".format(Current_timeStamp.strftime("%Y"),Current_timeStamp.strftime("%m"),"01")
        self.MonthToDate_DataFrame = self.Max_DataFrame.loc[MTD_Date :] 
        
        WeekStart_timeStamp = Current_timeStamp - timedelta(days=Current_timeStamp.weekday())
        WTD_Date = "{}-{}-{}".format(WeekStart_timeStamp.strftime("%Y"),WeekStart_timeStamp.strftime("%m"),WeekStart_timeStamp.strftime("%d"))
        
        self.WeekToDate_DataFrame = self.Hourly_DataFrame.loc[WTD_Date : ]
        self.WeekToDate_DataFrame  = self.WeekToDate_DataFrame.sort_index() 
        for key, val in self.Info_Dict.items():
            setattr(self, key, val)
            # print("{} -- {}".format(key,val)) UNCOMMENT ME IF YOU WANT TO CHECK THE DICTIONARY INFO COMING IN WITH KEY TERMS!!!

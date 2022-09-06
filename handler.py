import json
import numpy as np
import talib
import pandas as pd
from datetime import date
import requests

def get_asset_data(ticker, startDate, endDate, interval):
  URL = "https://data.messari.io/api/v1/assets/"+ ticker +"/metrics/price/time-series"
  PARAMS = {'start': startDate,'end':  endDate, 'interval': interval, 'timestamp-format': "rfc3339"}
  HEADERS = {'x-messari-api-key': 'da886de0-a0ba-45e3-9a8e-416810a2627e'}
  r = requests.get(url = URL, params = PARAMS, headers = HEADERS)
  data = r.json()

  # print(data)
  df = pd.DataFrame(data['data']['values'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
  if df.size == 0:
    raise NameError('The Messari does not have data for the this asset')
  return df

def get_ema_percentage(current_price, current_EMA):
  return (current_EMA - current_price)/current_EMA

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class trade_asset(object):
    def __init__(self, asset, percentage, pattern, direction):
        self.name = asset
        self.percentageToEma = percentage
        self.pattern = pattern
        self.direction = direction

def getAssetInfo(event, context):
    asset = event["asset"]
    today = date.today()
    lastYear = date(today.year - 1, 1, 1)  
    dailyData = get_asset_data(asset, lastYear.strftime("%m/%d/%Y"), today.strftime("%m/%d/%Y"), '1d')
    weeklyData = get_asset_data(asset, lastYear.strftime("%m/%d/%Y"), today.strftime("%m/%d/%Y"), '1w')
    

    print(asset)
    #Get weekly 8 weeks EMA on daily chart
    weeklyData['shortEMA'] = talib.EMA(weeklyData['close'], timeperiod=8)

    #Calculation of the EMA
    currentPrice = dailyData.iloc[-1]['close']
    currentEMA = weeklyData.iloc[-1]['shortEMA']
    calc_ema = get_ema_percentage(currentPrice, currentEMA)
    percentage = 0.15

    print(currentEMA, currentPrice, calc_ema)
    
    #check if the assets is close to the EMA
    if calc_ema <= abs(percentage) and calc_ema >= (percentage * -1):
        dailyData['morning star'] = talib.CDLMORNINGDOJISTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
        dailyData['evening star'] = talib.CDLEVENINGDOJISTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
        dailyData['shooting star'] = talib.CDLSHOOTINGSTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
        dailyData['hammer'] = talib.CDLHAMMER(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
        dailyData['engulfing'] = talib.CDLENGULFING(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])

        #Checking the candles stick patterns
        lastDay = dailyData.tail(5)
        isMorningStar = len(lastDay[lastDay['morning star'] != 0].index)
        isEveningStar = len(lastDay[lastDay['evening star'] != 0].index)
        isShootingStar = len(lastDay[lastDay['shooting star'] != 0].index)
        isHammer = len(lastDay[lastDay['hammer'] != 0].index)
        isEngulfing = len(lastDay[lastDay['engulfing'] != 0].index)

        percentage_ema = abs(calc_ema * 100)
        pattern = ""
        direction = ""
        status = ""
        #check if the assets is close to the EMA
        if calc_ema <= abs(percentage) and calc_ema >= (percentage * -1):
            dailyData['morning star'] = talib.CDLMORNINGDOJISTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
            dailyData['evening star'] = talib.CDLEVENINGDOJISTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
            dailyData['shooting star'] = talib.CDLSHOOTINGSTAR(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
            dailyData['hammer'] = talib.CDLHAMMER(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])
            dailyData['engulfing'] = talib.CDLENGULFING(dailyData['open'], dailyData['high'], dailyData['low'], dailyData['close'])

            #Checking the candles stick patterns
            lastDay = dailyData.tail(1)
            isMorningStar = len(lastDay[lastDay['morning star'] != 0].index)
            isEveningStar = len(lastDay[lastDay['evening star'] != 0].index)
            isShootingStar = len(lastDay[lastDay['shooting star'] != 0].index)
            isHammer = len(lastDay[lastDay['hammer'] != 0].index)
            isEngulfing = len(lastDay[lastDay['engulfing'] != 0].index)

            percentage_ema = abs(calc_ema * 100)
            pattern = "NA"
            direction = "NA"
            status = "keep"
            message = f"{asset} at {percentage_ema}% of the eight weekly exponential average"
            #Sending the alert
            if isMorningStar >=1:
                direction = "Bull" if lastDay.iloc[0]['morning star'] > 0 else "Bearish"
                pattern = "Morning Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                message = f"{direction}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Morning Star pattern"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a {bcolors.OKGREEN}Morning Star pattern{bcolors.ENDC}")
            elif isEveningStar >=1:
                direction = "Bull" if lastDay.iloc[0]['evening star'] > 0 else "Bearish"
                pattern = "Evening Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                message = f"{direction}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Evening Star pattern"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Evening Star pattern{bcolors.ENDC}")
            elif isShootingStar >=1:
                direction = "Bull" if lastDay.iloc[0]['shooting star'] > 0 else "Bearish"
                pattern = "Shooting Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                message = f"{direction}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Shooting Star pattern"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a {bcolors.OKGREEN}Shooting Star pattern{bcolors.ENDC}")
            elif isHammer >=1:
                direction = "Bull" if lastDay.iloc[0]['hammer'] > 0 else "Bearish"
                pattern = "Hammer"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                message = f"{direction}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Hammer pattern"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a {bcolors.OKGREEN}Hammer pattern{bcolors.ENDC}")
            elif isEngulfing >=1:
                direction = "Bull" if lastDay.iloc[0]['engulfing'] > 0 else "Bearish"
                pattern = "Engulfing"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                message = f"{direction}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a Engulfing pattern"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {asset} at {percentage_ema}% of the eight weekly exponential average and it has a {bcolors.OKGREEN}Engulfing pattern{bcolors.ENDC}")
            

    body = {
        "calc_ema": calc_ema,
        "pattern": pattern,
        "direction": direction,
        "status": status,
        "message": message,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

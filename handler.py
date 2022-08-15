import json
import numpy as np
import talib
import pandas as pd

def get_eth_daily_data():
    with open('./data/ETH_DAILY.json') as f:
        data = json.load(f)
        df = pd.DataFrame(data['data']['values'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

def get_eth_weekly_data():
    with open('./data/ETH_WEEKLY.json') as f:
        data = json.load(f)
        df = pd.DataFrame(data['data']['values'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

def get_ema_percentage(current_price, current_EMA):
  return (current_EMA - current_price)/current_EMA

class trade_asset(object):
    def __init__(self, asset, percentage, pattern, direction):
        self.name = asset
        self.percentageToEma = percentage
        self.pattern = pattern
        self.direction = direction

def hello(event, context):
    dailyData = get_eth_daily_data()
    weeklyData = get_eth_weekly_data()

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
            #Sending the alert
            if isMorningStar >=1:
                direction = "Bull" if lastDay.iloc[0]['morning star'] > 0 else "Bearish"
                pattern = "Morning Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {current_asset} is closing about {percentage_ema}% to the EMA 8 weekly and it has a {bcolors.OKGREEN}Morning Star pattern{bcolors.ENDC}")
            elif isEveningStar >=1:
                direction = "Bull" if lastDay.iloc[0]['evening star'] > 0 else "Bearish"
                pattern = "Evening Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {current_asset} is closing about {percentage_ema}% to the EMA 8 weekly and it has a {bcolors.OKGREEN}Evening Star pattern{bcolors.ENDC}")
            elif isShootingStar >=1:
                direction = "Bull" if lastDay.iloc[0]['shooting star'] > 0 else "Bearish"
                pattern = "Shooting Star"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {current_asset} is closing about {percentage_ema}% to the EMA 8 weekly and it has a {bcolors.OKGREEN}Shooting Star pattern{bcolors.ENDC}")
            elif isHammer >=1:
                direction = "Bull" if lastDay.iloc[0]['hammer'] > 0 else "Bearish"
                pattern = "Hammer"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {current_asset} is closing about {percentage_ema}% to the EMA 8 weekly and it has a {bcolors.OKGREEN}Hammer pattern{bcolors.ENDC}")
            elif isEngulfing >=1:
                direction = "Bull" if lastDay.iloc[0]['engulfing'] > 0 else "Bearish"
                pattern = "Engulfing"
                status = "buy" if lastDay.iloc[0]['engulfing'] > 0 else "sell"
                print(f"{bcolors.FAIL}{direction}{bcolors.ENDC}: {current_asset} is closing about {percentage_ema}% to the EMA 8 weekly and it has a {bcolors.OKGREEN}Engulfing pattern{bcolors.ENDC}")
            

    body = {
        "calc_ema": calc_ema,
        "pattern": pattern,
        "direction": direction,
        "status": status
    }

    return {"statusCode": 200, "body": json.dumps(body)}

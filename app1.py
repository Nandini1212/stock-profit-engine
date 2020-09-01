import os
import pprint

import requests
import json
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

# Define an instance of Flask object
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Investing strategy groups and the corresponding tickers.
ethicalInvesting = ["GOOG", "AMZN", "FB"]
growthInvesting = ["TSLA", "AAPL", "ADBE"]
indexInvesting = ["BABA", "NFLX", "TWTR"]
qualityInvesting = ["VMW", "UBER", "OKTA"]
valueInvesting = ["NTNX", "ZM", "NVDA"]

# Ratio of total amount to be invested
ratios = [.5, .3, .2]

def GetData(ticker):
    url = 'https://cloud.iexapis.com/stable/stock/{}/quote{}&token=pk_e86ef555ac2a46f28680850ec7401d56'.format(ticker, '?filter=symbol,companyName,latestPrice,latestTime,change,changePercent')
    response = requests.get(url)
    return response.json()

def GetStrategyData(strategy):
    if strategy == "Ethical Investing":
        return [GetData(ethicalInvesting[0]),
                GetData(ethicalInvesting[1]),
                GetData(ethicalInvesting[2])]
    elif strategy == "Growth Investing":
        return [GetData(growthInvesting[0]),
                GetData(growthInvesting[1]),
                GetData(growthInvesting[2])]
    elif strategy == "Index Investing":
        return [GetData(indexInvesting[0]),
                GetData(indexInvesting[1]),
                GetData(indexInvesting[2])]
    elif strategy == "Quality Investing":
        return [GetData(qualityInvesting[0]),
                GetData(qualityInvesting[1]),
                GetData(qualityInvesting[2])]
    elif strategy == "Value Investing":
        return [GetData(valueInvesting[0]),
                GetData(valueInvesting[1]),
                GetData(valueInvesting[2])]
    else:
        return "Invalid Strategy"

def GetHistory(ticker):
    url = 'https://cloud.iexapis.com/stable/stock/{}/chart?range=5d&filter=symbol,close&token=pk_e86ef555ac2a46f28680850ec7401d56'.format(ticker, '?filter=companyName,latestPrice,latestTime,change,changePercent')
    response = requests.get(url)
    return response.json()

def GetStrategyHistory(strategy):
    if strategy == "Ethical Investing":
        return [GetHistory(ethicalInvesting[0]),
                GetHistory(ethicalInvesting[1]),
                GetHistory(ethicalInvesting[2])]
    elif strategy == "Growth Investing":
        return [GetHistory(growthInvesting[0]),
                GetHistory(growthInvesting[1]),
                GetHistory(growthInvesting[2])]
    elif strategy == "Index Investing":
        return [GetHistory(indexInvesting[0]),
                GetHistory(indexInvesting[1]),
                GetHistory(indexInvesting[2])]
    elif strategy == "Quality Investing":
        return [GetHistory(qualityInvesting[0]),
                GetHistory(qualityInvesting[1]),
                GetHistory(qualityInvesting[2])]
    elif strategy == "Value Investing":
        return [GetHistory(valueInvesting[0]),
                GetHistory(valueInvesting[1]),
                GetHistory(valueInvesting[2])]
    else:
        return "Invalid Strategy"

@app.route('/StrategyRetriever', methods=['POST'])
@cross_origin(origin='*')
def StrategyRetriever():
    try:
        if request.method == "POST":
            strategies = request.form['Strategies']
            amount = request.form['Amount']
            strategyData = []
            strategyHistory = []
            for strategy in strategies:
                strategyData.append(GetStrategyData(strategy))
                strategyHistory.append(GetStrategyHistory(strategy))
            returnData = {"StrategiesResponse": strategyData,
                          "StrategyHistory": strategyHistory,
                          "AmountResponse": [amount*ratios[0], amount*ratios[1], amount*ratios[2]]}
            response=Response(json.dumps(returnData), mimetype='application/json')
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
    except Exception as e:
        returnData = {"Error": "Unable to retrieve strategy data and history"}
        response = Response(json.dumps(returnData), mimetype='application/json')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


def TestStrategyRetriever(strategies, amount):
    strategyData = []
    strategyHistory = []
    for strategy in strategies:
        strategyData.append(GetStrategyData(strategy))
        strategyHistory.append(GetStrategyHistory(strategy))
    returnData = {"StrategiesResponse": strategyData,
                  "StrategyHistory": strategyHistory,
                  "AmountResponse": [amount * ratios[0], amount * ratios[1], amount * ratios[2]]}
    prettyPrint = pprint.PrettyPrinter(indent=4)
    prettyPrint.pprint(returnData)


if __name__ == "__main__":
    TestStrategyRetriever(["Growth Investing", "Quality Investing"], 10000)
    #app.run(debug=True, host='5000')


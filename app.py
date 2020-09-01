import ticker as ticker
from flask import Flask, request, json
from pip._vendor import requests
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ethicalInvesting = ["GOOGL", "AMZN", "FB"]
growthInvesting = ["TSLA", "AAPL", "ADBE"]
indexInvesting = ["BABA", "NFLX", "TWTR"]
qualityInvesting = ["VMW", "UBER", "OKTA"]
valueInvesting = ["NTNX", "ZM", "NVDA"]

def getStockQuote(stockList):
    param_filter = '?filter=companyName,latestPrice,latestTime,change,changePercent'
    stockData = []
    for stock in stockList:
        dataResult = requests.get('https://api.iextrading.com/1.0/stock/{}/quote/{}'.format(ticker, param_filter))
        statusCode = dataResult.statusCode
        success = True
        if statusCode == 200:
            stockData.append(dataResult.json())
        else :
            success = False
        for x in range(len(stockData)):
            print (stockData[x],)
    return stockData

'''
@app.route('/', methods=['GET', 'POST'])
def hello_world(stockList):

    if request.method == 'POST':
        try :
            investmentAmount = request.form['investAmount']
            if investmentAmount < 5000:
                return json.dumps({"error" : "Amount should be more than $5000"}), 500
            strategyOne = (request.form['strategyOne'])
            strategyTwo = (request.form['strategyTwo'])
            strategies = [strategyOne, strategyTwo]
            
            stockData = []

            for strategy in strategies :
                if strategy == "Ethical Investing" :
                    stockData.append(getStockQuote(ethicalInvesting))
                elif strategy == "Growth Investing":
                    stockData.append(getStockQuote(growthInvesting))
                elif strategy == "Index Investing":
                    stockData.append(getStockQuote(indexInvesting))
                elif strategy == "Quality Investing":
                    stockData.append(getStockQuote(qualityInvesting))
                elif strategy == "Value Investing":
                    stockData.append(getStockQuote(valueInvesting))
                elif strategy == "None":
                    """Only one investment strategy wanted"""

            amountOne = investmentAmount * 0.2
            amountTwo = investmentAmount * 0.3
            amountThree = investmentAmount * 0.5



    except:
    print("Something went wrong")




    return 'Hello World!'

'''
if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    getStockQuote(ethicalInvesting)
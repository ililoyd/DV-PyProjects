from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
api = Api(app)

app.config['JSON_AS_ASCII'] = False

class OddsGames(Resource):
    
    def get(self):


        url = "https://projects.fivethirtyeight.com/soccer-predictions/ligue-1/"

        page = requests.get(url).content
        soup = BeautifulSoup(page, "lxml")
        matchesTable = soup.select('#matches-table-wrapper > .upcoming')[0]
        games = matchesTable.select('.initial-view > table')[:10]
        result = []
        def computeOdd(percentString):
            percent = int(percentString[:-1])/100
            odd = round(1 / percent,2)*2
            return odd

        for game in games:
            dictOdds = {}
            for i, tr in enumerate(game.find_all("tr")):
                tds = tr.find_all("td")
                if i == 0 :
                    dictOdds["date"] = tds[0].text
                    dictOdds["Opponent 1"] = tds[1].text
                    dictOdds["Odds Win 1"] = computeOdd(tds[2].text)
                    dictOdds["Odds Draw"] = computeOdd(tds[3].text)
                else :
                    dictOdds["Opponent 2"] = tds[0].text
                    dictOdds["Odds Win 2"] = computeOdd(tds[1].text)

            result.append(dictOdds)
        return jsonify(result)
    
api.add_resource(OddsGames, '/odds') 

if __name__ == '__main__':
     app.run(port='5002')
import json

class team:
    
    def __init__(self, teamName="", group="", countryCode="", ranking="1"):
        self.name = teamName
        self.group = group
        self.countryCode = countryCode
        self.ranking = ranking

    def __str__(self):
        return "{} - {} - {}{}".format(self.name, self.countryCode, self.group,self.ranking)

dataset = {"Manchester United" : {

}


}       
A1 = team("Manchester United", "A", "England", "1")
B1 = team("PSG", "B", "France", "1")
C1 = team("AS Roma", "C", "Italy", "1")
D1 = team("FC Barcelona", "D", "Spain", "1")
E1 = team("Liverpool FC", "E", "England", "1")
F1 = team("Man City", "F", "England", "1")
G1 = team("BJK", "G", "Turkey", "1")
H1 = team("Spurs", "H", "England", "1")

A2 = team("Basel", "A", "Switzerland", "2")
B2 = team("Bayern", "B", "Germany", "2")
C2 = team("Chelsea", "C", "England", "2")
D2 = team("Juve", "D", "Italy", "2")
E2 = team("Sevilla", "E", "Spain", "2")
F2 = team("Donetsk", "F", "Ukraine", "2")
G2 = team("Porto", "G", "Portugal", "2")
H2 = team("Real Madrid", "H", "Spain", "2")

with open('clubs.json') as json_data_file:
    data = json.load(json_data_file)

for club in data:
    temp = team(club, **data[club])
    print(temp)

print(temp.countryCode, temp.group)
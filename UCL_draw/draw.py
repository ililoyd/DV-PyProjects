# coding:utf-8

'''
Module: uclDrawCal
Created on 2016-12-8
@author: Ring
'''


import itertools


class team:
    
    def __init__(self, teamName="", teamGroup="", teamCountry="", teamRanking="1"):
        self.name = teamName
        self.group = teamGroup
        self.country = teamCountry
        self.ranking = teamRanking
    
    def printTeam(self):
        print (self.name, "-",  self.country, "-", self.group+self.ranking)
    

def isDrawCorrect(list1, list2):
    for i in range(0,8):
        if (list2[i].group == list1[i].group) or (list2[i].country == list1[i].country):
            return False
    return True


def getProbabilityByTeam(list1, list2, allResult2, index):
    print ('\n',list1[index].name)
    totalCount = 0
    proList = {
               list2[0].name:0, list2[1].name:0, list2[2].name:0, list2[3].name:0, \
               list2[4].name:0, list2[5].name:0, list2[6].name:0, list2[7].name:0
               }

    for someResult in allResult2:
        if isDrawCorrect(list1, someResult):
            totalCount += 1
            proList[someResult[index].name] += 1
        else:
            pass
    for i in range(0, 8):
        print ("draw: ", list2[i].name+": ", proList[list2[i].name]*1.0/totalCount)


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

listFirst = [A1, B1, C1, D1, E1, F1, G1, H1]
listSecond = [A2, B2, C2, D2, E2, F2, G2, H2]
firstAllResult = list(itertools.permutations(listFirst, len(listFirst)))
secondAllResult = list(itertools.permutations(listSecond, len(listSecond)))


def main():
    for i in range(0, 8):
        getProbabilityByTeam(listFirst, listSecond, secondAllResult, i)
        
    for j in range(0, 8):
        getProbabilityByTeam(listSecond, listFirst, firstAllResult, j)


main()
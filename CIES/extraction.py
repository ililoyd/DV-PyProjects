import time, requests, json

from datetime import datetime
from bs4 import BeautifulSoup

from tqdm import tqdm

import pandas as pd
import numpy as np

#Scrapping Transfermarkt to get all the players names

def get_scrapped_names_tfmarkt(url, log=False):
    if log:
        print("Scrapping Transfermarkt for players of target club")
        
    page = requests.get(url,  headers={'User-Agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(page, "lxml")

    names = []
    
    soup_table = soup.find("div", {"id" : "yw1"}).find("table")
    
    for td in soup_table.findAll("td", {"class" : "hauptlink"}):
        if 'rechts' not in td.attrs['class']:
            names.append(td.find("div").text)
        
    return names

#Using CIES hook to get player estimated values from last 12 months

def get_report_from_cies(names, match_club, delay=1, log=False):
    hook = "http://prod.fo-pfpo.iad-informatique.com/ratings/web/services?method=searchPlayers&key={}"

    tuples = []
    if log:
        print("Associating each player from {} with its id in CIES database".format(match_club))
    for _ , name in enumerate(tqdm(names)):
        url = hook.format(name)
        response = requests.get(url).content

        ids = json.loads(response)

        #if name is not found using complete name
        if(isinstance(ids, list)):

            #Use only a partial name
            for split in reversed(name.split()):
                url = hook.format(split)
                response = requests.get(url).content 

                ids = json.loads(response)

                if not isinstance(ids, list):
                    break
                
            #If name is still not found, it needs human intervention to rework the file
            if isinstance(ids, list):
                #raise the flag that indicates a rework needed
                tuples.append((name, None, None, response , False))
                time.sleep(delay)
                continue

        response_ids = list(ids.keys())

        response_clubs = []
        response_names = []

        #splitting string "name (club)" into two lists of names and clubs
        for val in ids.values():
            response_clubs.append(val[val.find("(")+1:val.find(")")])
            response_names.append(val[:val.find("(")-1])

        #if expected club if found then remove all the options
        if match_club in response_clubs:
            index = response_clubs.index(match_club) 

            response_clubs = response_clubs[index]
            response_names = response_names[index]
            response_ids = response_ids[index]
            match_found = True

        #else it needs human intervention to rework the file
        else:
            #rework needed flag
            match_found = False


        tuples.append((name,response_clubs, response_names, response_ids, match_found))
        #delay to avoid DDOS and overuse of CIES server
        time.sleep(delay)
    
    return pd.DataFrame(tuples, columns=["Nom", "json_clubs", "json_names", "json_ids", "NoIssue"])

def get_all_team_values_cies(df_json, delay=1, log=False, **kwargs):
    #hook
    hook = "http://prod.fo-pfpo.iad-informatique.com/widget/transfertValuesView/en/{}?P_change=P1"

    #settings
    # period = kwargs.get('period', '4')
    period_array = kwargs.get('period_array', np.array([4])) 
    mr_value_array = []
    target_value_array = []

    pd_mr_label = None
    pd_target_label = None

    none_array = []

    
    if log:
        print("Getting all the CIES values for each player")

    #For each player
    for idx in tqdm(df_json['json_ids']):
        url  = hook.format(idx)
        page = requests.get(url).content
        soup = BeautifulSoup(page, "lxml")


        #extract all data from CIES json graph
        div =  soup.find("div", {"id" : "content"})
        graph_data = json.loads(div["graph-data"])
        cies_values = graph_data["data"]
        cies_labels = graph_data["labels"][:-1]
        
        #period_array = np.array(filter(lambda x : x>, period_array))

        period_array = period_array[period_array <= (len(cies_values) - 1)]
        month_start = int(cies_labels[-1].split("/")[0]) if int(cies_labels[-1].split("/")[0]) != 1 else 0

        

        target_label = ["{:02d}/{}".format((month_start - period) % 12 + 1,
                                        int(cies_labels[-1].split("/")[1]) + (month_start - period) // 12 ) for period in period_array]

        #target_value = [cies_values[max(-1-period,-len(cies_values))] for period in period_array]
        target_value = [cies_values[-1-period] for period in period_array]
        
        #Check if at least one value is stored
        none_bool = not(np.all(np.array(target_value) == None))
        
        # #if key : date (old format)
        # else :

        #     target_label = "{:02d}/{}".format(int(cies_labels[-1].split("/")[0])-period,
        #                                     int(cies_labels[-1].split("/")[1]) - period // 12 )
        #     target_value = cies_values[-1-period]

        #     #Check if targeted value is stored
        #     none_bool = False if (target_value is None) else True

        #Get last published values (current month)
        most_recent_value = cies_values[-1]
        most_recent_label = cies_labels[-1]

        #Check if player currently has a value
        none_bool &= not(most_recent_value is None) 

        if pd_mr_label is None :
            pd_mr_label = most_recent_label 
            pd_target_label = target_label 

        mr_value_array.append(most_recent_value)
        target_value_array.append(target_value)

        none_array.append(none_bool)

        time.sleep(delay)

    to_add = pd.DataFrame(data=target_value_array, columns=pd_target_label).assign(**{pd_mr_label : np.array(mr_value_array),"HasData": none_array})

    return pd.concat([df_json, to_add], axis=1)

    # else :    
        
    #     return df_json.assign(**{pd_target_label : np.array(target_value_array), 
    #                 pd_mr_label : np.array(mr_value_array),
    #                 "HasData" : none_array})

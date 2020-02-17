from extraction import get_all_team_values_cies,  get_report_from_cies, get_scrapped_names_tfmarkt

from datetime import datetime
import yaml

import numpy as np

#Drop unwanted columns for final report
def get_human_report(df_json):
    filtered_df = df_json[df_json["HasData"]]
    final_df = filtered_df.drop(["json_clubs", "json_names", "json_ids", "NoIssue", "HasData"], axis = 1)
        
    return final_df

"""  
Generate Dataframe with all the players from a club (with Transfermarkt as source)
Match these players with their internal id from CIES database using "API" hook

"""
def generate_pre_report_cies(target_club, url_tfmarkt, export = False, **kwargs):

    sep = kwargs.get('sep', ',') 
    delay= kwargs.get('delay', 0.5)  
    log_dir = kwargs.get('log_dir', "./log/") 


    names = get_scrapped_names_tfmarkt(url=url_tfmarkt, log=True)

    df_json = get_report_from_cies(names, match_club = target_club, log=True, delay=delay)

    #Export file as CSV (so that file can be reworked if needed)
    #logging
    filename =  datetime.now().strftime("%d-%m-%Y_%H%M%S-{}.csv").format(target_club)
    if(export):
        df_json.to_csv(log_dir + filename, index=False, encoding='utf-8-sig', sep=sep)
    
    return df_json

"""  
Generate Dataframe with all the players value using their CIES id
Access CIES values from their "API" hook and the json graph that's generated

"""
def generate_human_report_cies(df_json, target_club,  **kwargs ):
    sep = kwargs.get('sep', ',') 
    delay= kwargs.get('delay', 0.5)  
    report_dir = kwargs.get('report_dir', "./report/") 
    dates = kwargs.get('target_dates', None)

    if dates is None:
        period_array = None

    else:
        target_tuples = list(map(lambda x : (int(x[:2]),int(x[3:])), dates))

        curr_date = datetime.now().strftime("%m/%Y")
        curr_tuple = (int(curr_date[:2]),int(curr_date[3:]))

        period_array = np.apply_along_axis(lambda x: x[0] + 12 * x[1], 1, np.subtract(curr_tuple, target_tuples))

    df_copy = get_all_team_values_cies(df_json[df_json["NoIssue"]], period_array=period_array, log=True, delay=delay)

    final_df = get_human_report(df_copy)

    filename =  datetime.now().strftime("%d-%m-%Y_%H%M%S-{}.csv").format(target_club)
    final_df.to_csv(report_dir + filename, encoding='utf-8-sig', sep=sep, index=False)

    return final_df

if __name__ == "__main__":

    #Load congif.yml
    with open("conf.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    #main settings:
    dict_config = cfg["main"]

    #For earch task, generate a report
    #TODO: reload from log
    for section in cfg["objectives"]:

        task_name , dict_task = section.popitem()
        print("Task : ", task_name)

        df_json = generate_pre_report_cies(dict_task["cies_name"], dict_task["url"], **dict_config)

        generate_human_report_cies(df_json, dict_task["cies_name"], target_dates=dict_task["target_dates"], **dict_config)
        print("\n")
    
    
    



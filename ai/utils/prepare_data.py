"""TODO: Comment"""
import pandas as pd
import configparser
import os
import json


SETTINGS_PATH = "ai/config.ini"
RAW_DATA = "BD_Test.xlsx"
JSON_DATA = "variables_dataset_actualizado.json"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)


def read_excel(excel_path:str) -> pd.DataFrame :
    """_summary_

    Args:
        excel_path (_type_): _description_
    """
    df = pd.read_excel(excel_path, header=1, sheet_name=0)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def read_master(json_path:str) -> dict:
    """_summary_

    Args:
        json_path (str): _description_

    Returns:
        dict: _description_
    """
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
        
    def lower_keys(d):
        if isinstance(d, dict):
            return  {
                k.strip().lower().replace(" ", "_"): 
                    lower_keys(v) for k, v in d.items()
            }
            
    return lower_keys(data)
    

def main() :
    print("Llegue")
    excel = os.path.join(config["data_path"]["raw_path"], RAW_DATA)
    json_path = os.path.join(config["data_path"]["raw_path"], JSON_DATA)
    df = read_excel(excel_path=excel)
    dic = read_master(json_path=json_path)
    print(len(df.columns) == len(dic.keys()))
    print(set(df.columns).symmetric_difference(set(dic.keys())))
    
if __name__ == "__main__":
    print("llegue")
    main()
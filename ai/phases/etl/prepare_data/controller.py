"""TODO: Comment"""
import pandas as pd
import configparser
import os
import json
from docx import Document


from ai.agents.agent import Agent
from ai.phases.etl.prepare_data.prompts import EXTRACT_INFO_VARIABLES
from ai.phases.etl.prepare_data.schemas import Master

SETTINGS_PATH = "ai/config.ini"
RAW_DATA = "BD_Test.xlsx"
JSON_DATA = "variables_dataset_actualizado.json"
DOC_DATA = "descripcion.docx"

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

def read_master(file: str) -> str:
    """Reads the content of a Word (.docx) file and returns it as a string.

    Args:
        file (str): Path to the Word document.

    Returns:
        str: The extracted text from the document.
    """
    
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
    

            
"""
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
        
    def lower_keys(d):
        if isinstance(d, dict):
            return  {
                k.strip().lower().replace(" ", "_"): 
                    lower_keys(v) for k, v in d.items()
            }
    return lower_keys(data)
"""
def main() :
    doc_path = os.path.join(config["data_path"]["raw_path"], DOC_DATA)
    text = read_master(file=doc_path)
    agent = Agent()
    response = agent.call_llm(prompt=EXTRACT_INFO_VARIABLES.format(text=text), response_format=Master)
    print(response)
    
if __name__ == "__main__":
    main()
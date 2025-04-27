"""TODO: Comment"""
from dotenv import load_dotenv
import pandas as pd
import configparser
import os
import json
import sys
from docx import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.prepare_data.prompts import EXTRACT_INFO_VARIABLES
from ai.phases.etl.prepare_data.schemas import Master
from ai.phases.etl.prepare_data.agent import PrepareDataAgent

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")
RAW_DATA = "BD.xlsx"
JSON_DATA = "variables_dataset_actualizado.json"
DOC_DATA = "descripcion.docx"
MASTER_PATH = "master.json"

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
    
def process_master(master: str) -> None:
    """Call llm and make an structured master.

    Args:
        master (str): master path.
    """
    # Esto no estoy muy seguro de si esta correcto para la llamada a la API
    master = os.path.join(config["data_path"]["raw_path"], DOC_DATA)
    text = read_master(file=master)
    
    agent = Agent()
    response = agent.call_llm(model="gpt-4o", prompt=EXTRACT_INFO_VARIABLES.format(text=text), response_format=Master)
    
    
    if isinstance(response, str):
        parsed_response = json.loads(response)
    else:
        parsed_response = response.model_dump() if hasattr(response, "model_dump") else response

    # Transformar al nuevo formato
    new_master = {
        entry["column_name"]: entry["column_info"]
        for entry in parsed_response["column"]
    }

    # Guardar archivo JSON
    json_path=os.path.join(config["data_path"]["processed_path"], MASTER_PATH)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(new_master, f, ensure_ascii=False, indent=4)
    print(f"Master loaded in: {json_path}")
    
    
def process_excel(excel: str) -> None:
    """ Clean the dataset
    
    Args:
        excel (str): excel or csv path.
    """ 
    # No se si hay que hacer lo del config ini
    df = read_excel(excel)
    

def controller(master_path: str, excel_path: str) -> None:
    """Prepare Data API Controller.

    Args:
        master_path (str)
        excel_path (str)
    """
    
    process_master(master=master_path)
    process_excel(excel=excel_path)


def execute(max_turns: int) -> list:
    """Execute the agent workflow.

    Args:
        max_turns (int): Maximum number of turns.

    Returns:
        list: List of results.
    """
    # process_master(DOC_DATA)
    agent = PrepareDataAgent()
    return agent.execute(max_turns=max_turns)
    
    
#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
    process_master(DOC_DATA)
    agent = PrepareDataAgent()
    agent.execute()
    
if __name__ == "__main__":
    main()
    
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
import os
import pandas as pd

def load_xlsx(file_path: str) -> pd.DataFrame:
    """Load a .xlsx file in a Pandas DataFrame.
	
	Args:
		file_path(str): .xlsx file
  
    Return:
		df(pd.DataFrame): DataFrame
    """
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: file not found {file_path}")

    # Cargar el archivo Excel en un DataFrame
    df = pd.read_excel(file_path, engine="openpyxl")

    return df  # Retornar el DataFrame para que pueda ser usado en otro script


def save_to_csv(df: pd.DataFrame, output_path: str):

    df.to_csv(output_path, index=False)
    
    
if __name__ == "__main__":
    file_path = "./ai/data/raw/BD_Test.xlsx"
    df = load_xlsx(file_path)
    csv_path = "./ai/data/processed/dataset.csv"
    save_to_csv(df, csv_path)
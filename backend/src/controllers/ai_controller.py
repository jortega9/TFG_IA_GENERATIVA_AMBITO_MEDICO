import os
from fastapi import HTTPException
from ai.data.prepare_data import load_xlsx, save_to_csv

def convert_xlsx(file_path: str) -> str:
    """Convert a xlsx file in a .csv file and returns the path.

    Args:
        file_path (str): xlsx file that we want to convert.

    Returns:
        str: .csv path.
    """
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="FILE NOT FOUND.")
    
    try:
        # Load the dataframe
        df = load_xlsx(file_path=file_path)
        # Define the .csv path
        csv_path = file_path.replace(".xlsx", ".csv")
        # Save as .csv
        save_to_csv(df, csv_path)
        # return the csv path
        return csv_path
    except Exception as e:
        raise HTTPException(status_code=500, detail="ERROR CONVERTING FILE.")



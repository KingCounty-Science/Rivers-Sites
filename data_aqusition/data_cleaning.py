import pandas as pd # Read the Excel file
from pathlib import Path
def data_cleaning(input_path, output_path):

    df_sites = pd.read_csv(input_path)
    df_sites = df_sites.rename(columns={"Project Number": "project number", "Project Name": "project name", 
                "Project Manager": "project manager", "SITE_CODE": "site", "SITE_NAME": "site name", 
                "DATE_INSTA": "installed", "DATE_REMOV": "removed", "GAGER_NAME": "gager", 
                "Processor_Name": "processor", "LAT": "latitude", "LON": "longitude"})

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_sites.to_csv(output_path, index=False)
    print(df_sites.columns)


if __name__ == "__main__":

    input_path = "data/Rivers_2025_Sites_with_coords.csv"
    output_path = "data/Rivers_2025_Sites_with_coords.csv"
    data_cleaning(input_path, output_path)
import pandas as pd
import pyodbc
from pathlib import Path

def add_coordinates_to_sites(
    excel_path='data/Rivers_2025_Sites.xlsx',
    output_path='data/Rivers_2025_Sites_with_coords.xlsx',
    server='your_server_name',
    database='your_database_name'
):
    """
    Import Excel sites, match with SQL Server coordinates, and export.
    
    """
    # Read the Excel file
    df_sites = pd.read_excel(excel_path)
    
    
    # Connect to SQL Server using Windows Authentication
    conn_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    
    conn = pyodbc.connect(conn_string)
        
        # Query to get Site_Code, LAT, LON from tblGaugeLLID
    query = """
        SELECT SITE_CODE, LAT, LON
        FROM tblGaugeLLID
        WHERE SITE_CODE IS NOT NULL
        """

    df_coords = pd.read_sql(query, conn)
    conn.close()
        
    print(f"Retrieved {len(df_coords)} records from database")
        
   
    
    # Merge the dataframes on Site_Code
    print("\nMatching site codes and adding coordinates...")
    df_result = df_sites.merge(
        df_coords,
        on='SITE_CODE',
        how='left',
        indicator=True
    )
    
    # Report matching statistics
    matched = (df_result['_merge'] == 'both').sum()
    unmatched = (df_result['_merge'] == 'left_only').sum()
    
   
    if unmatched > 0:
        print("\nUnmatched site codes:")
        unmatched_codes = df_result[df_result['_merge'] == 'left_only']['SITE_CODE'].tolist()
        for code in unmatched_codes[:10]:  # Show first 10
            print(f"  - {code}")
        if unmatched > 10:
            print(f"  ... and {unmatched - 10} more")
    
    # Remove the merge indicator column
    df_result = df_result.drop('_merge', axis=1)
    print(df_result)
    # Save to Excel
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_result.to_csv(output_path, index=False)
     
    return df_result


if __name__ == "__main__":
    # Configuration - UPDATE THESE VALUES
    SERVER = 'KCITSQLPRNRPX01'  # e.g., 'localhost' or 'SERVER\\INSTANCE'
    DATABASE = 'gData'
    
    # Run the function
    df = add_coordinates_to_sites(
        excel_path='data/Rivers_2025_Sites.xlsx',
        output_path='data/Rivers_2025_Sites_with_coords.csv',
        server=SERVER,
        database=DATABASE
    )
    
    # Display sample of results
    print("\nSample of results (first 5 rows):")
    print(df[['SITE_CODE', 'LAT', 'LON']].head())
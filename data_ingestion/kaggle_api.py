import kagglehub
import shutil
from pathlib import Path
import os

DATA_DIR = 'data'

def main():
    # Download latest version of the dataset
    cache_path = kagglehub.dataset_download("osmi/mental-health-in-tech-survey")
    print("Downloaded to cache:", cache_path)
    
    # Ensure DATA_DIR exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Find the survey CSV file in the downloaded data
    survey_file = None
    for item in Path(cache_path).glob('*.csv'):
        if 'survey' in item.name.lower():
            survey_file = item
            break
    
    if not survey_file:
        # If we can't find a file with 'survey' in the name, just use the first CSV
        csv_files = list(Path(cache_path).glob('*.csv'))
        if csv_files:
            survey_file = csv_files[0]
        else:
            raise FileNotFoundError("No CSV files found in the downloaded dataset")
    
    # Copy the survey file to the destination as 'survey.csv'
    destination = os.path.join(DATA_DIR, 'survey.csv')
    shutil.copy(str(survey_file), destination)
    print(f"Copied survey data to: {destination}")

if __name__ == "__main__":
    main()
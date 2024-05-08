import pandas as pd
from collections import defaultdict
import os

def create_markdown_files(csv_file_path, output_dir):
    # Load the CSV file
    data = pd.read_csv(csv_file_path)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Track the number of times each title is used to handle duplicates
    title_count = defaultdict(int)
    
    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        title = row['Title']
        markdown_content = row['Full_Markdown']
        
        # Update count and create filename
        title_count[title] += 1
        if title_count[title] > 1:
            filename = f"Training Details - {title} - {title_count[title]}.md"
        else:
            filename = f"Training Details - {title}.md"
        
        # Create full path for the file
        file_path = os.path.join(output_dir, filename)
        
        # Write the markdown content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

# Specify the path to the CSV file and the output directory
csv_file_path = 'docs/training/training_data.csv'
output_dir = 'docs/training/markdown'

# Call the function
create_markdown_files(csv_file_path, output_dir)
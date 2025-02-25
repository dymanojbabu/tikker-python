import os
import csv
import requests
from bs4 import BeautifulSoup

def extract_roe_from_url(url, index):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all li elements with the class 'flex flex-space-between'
        li_elements = soup.find_all('li', class_='flex flex-space-between')
        
        # Check if there are enough elements
        if len(li_elements) > index:
            roe_element = li_elements[index]  # Get the element at the specified index
            print(f"Found element at index {index}: {roe_element}")  # Debug print to see what we found
            
            # Find the span with class "number" inside the li element
            number_span = roe_element.find('span', class_='number')
            if number_span:
                return number_span.text.strip()
        return "ROE value not found"
    
    except requests.RequestException as e:
        return f"Error accessing URL: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def read_and_update_csv(file_path):
    rows = []
    # Open the file once for both reading and writing
    with open(file_path, mode='r+', newline='') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

        # Process rows and update ROE values, skipping the first row
        for row in rows[1:]:  # Start from the second row
            if len(row) > 1 and row[1].strip():
                url = f"https://www.screener.in/company/{row[1]}/consolidated/"
                
                # ROE Row is 3 and html index is 
                if row[3].strip():
                    print(f"Skipping {row[1]} as ROE already exists: {row[3]}")
                else:
                    roe_value = extract_roe_from_url(url, 7) 
                    print(roe_value)
                    while len(row) < 4:
                        row.append('')
                    row[3] = roe_value

                # ROIC Row is 8 and html index is 6
                if row[8].strip():
                    print(f"Skipping {row[1]} as ROIC already exists: {row[8]}")
                else:
                    roe_value = extract_roe_from_url(url, 6)  
                    print(roe_value)
                    while len(row) < 9:
                        row.append('')
                    row[8] = roe_value

                # PE Row is 7 and html index is 3
                if row[6].strip():
                    print(f"Skipping {row[1]} as PE already exists: {row[6]}")
                else:
                    roe_value = extract_roe_from_url(url, 3)  
                    print(roe_value)    
                    while len(row) < 7:
                        row.append('')
                    row[6] = roe_value

                # Dividend Yield Row is 5 and html index is 5
                if row[5].strip():
                    print(f"Skipping {row[1]} as Dividend Yield already exists: {row[5]}")
                else:
                    roe_value = extract_roe_from_url(url, 5)  
                    print(roe_value)    
                    while len(row) < 6:
                        row.append('')
                    row[5] = roe_value    

        # Move the file pointer to the beginning of the file
        file.seek(0)
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()

if __name__ == "__main__":
    csv_file_path = 'data.csv'
    read_and_update_csv(csv_file_path) 
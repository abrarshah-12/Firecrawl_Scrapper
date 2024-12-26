from firecrawl import FirecrawlApp
import google.generativeai as genai
from dotenv import load_dotenv
import json
import os
import pandas as pd
import datetime
import re


def scrape_data(url):
    """
    Scrapes data from a given URL using Firecrawl.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The scraped markdown content.

    Raises:
        KeyError: If the 'markdown' key is not present in the scraped data.
    """
    load_dotenv()

    app = FirecrawlApp(api_key=os.getenv('FIRE_CRAWL_API'))
    scraped_data = app.scrape_url(url)

    if 'markdown' in scraped_data:
        return scraped_data['markdown']
    else:
        raise KeyError("The key 'MARKDOWN' does not exist in the scraped data!")


def save_raw_data(raw_data, timestamp, output_folder='output'):
    """Saves raw scraped data to a markdown file."""
    os.makedirs(output_folder, exist_ok=True)
    raw_output_path = os.path.join(output_folder, f'rawData_{timestamp}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    print(f'Raw data saved to {raw_output_path}')


def chunk_data(data, chunk_size=2000):
    """
    Chunks the input text data into smaller pieces.

    Args:
        data (str): The data to chunk.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of string chunks.
    """
    if not isinstance(data, str):
      return []  # If data is not a string, return an empty list.

    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks

def format_data(data, fields=None):
  """
    Formats the scraped data using Gemini AI API by chunking the data and combining the results.

    Args:
        data (str): The scraped markdown data.
        fields (list, optional): List of fields to extract. Defaults to predefined fields if None.

    Returns:
        list: A list of dictionaries with formatted data, or None if there was an API error.

    Raises:
        ValueError: If any formatted data from API is not valid JSON.
    """
  load_dotenv()

  GOOGLE_API_KEY = os.getenv('GEMINI_API')
  if not GOOGLE_API_KEY:
      raise ValueError("Please set the GEMINI_API environment variable.")
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-pro')

  if fields is None:
      fields = ['Address', 'Real Estate Agency', 'Price', 'Beds', 'Baths', 'Sqft', 'Year Built', 'Home Type',
                'Picture of home url', 'Listing url']

  system_message = """You are an intelligent text extraction assistant. Your task is to extract structured
                      information from the given text and convert it into a pure JSON format. The JSON should
                      contain no additional commentary, explanations, or extraneous information. You may encounter
                      cases where you can't find the data for the requested fields, or the data will be
                      in a foreign language. Please process the following text and provide the output in pure JSON format
                      with no words before or after the JSON: """
  
  # Split the data into chunks
  chunks = chunk_data(data, chunk_size=2000)
  all_results = []
  for chunk in chunks:
      user_message = f"Extract the following information from the provided text: \nPage content:\n\n{chunk}\n\nInformation to extract: {fields}"
      prompt = f"{system_message}\n\n{user_message}"

      try:
        response = model.generate_content(prompt)
        formatted_data = response.text.strip()
        
        try:
            parsed_json = json.loads(formatted_data)
        except json.JSONDecodeError as e:
            print(f'JSON decoding error: {e}')
            print(f'Formatted data that caused the error: {formatted_data}')
            raise ValueError('The formatted data is not a valid JSON')
        
        if isinstance(parsed_json, dict):
              all_results.append(parsed_json)  # If we only get one output, append the dictionary to the result
        elif isinstance(parsed_json, list):
              all_results.extend(parsed_json) # If we get a list of objects, add them to the result.
        else:
            print(f"Unexpected formatted_data type: {type(parsed_json)}, skipping.") # If the output is of an unexpected type, skip.

      except Exception as e:
        print(f"Error with Gemini API: {e}")
        continue  # Continue to the next chunk on error

  if not all_results:
      print("No valid data extracted from any chunks") # if there is no data returned after processing the chunks
      return None
  
  return all_results # return the result.


def save_formatted_data(formatted_data, timestamp, output_folder='output'):
    """Saves formatted data to JSON and CSV files."""
    os.makedirs(output_folder, exist_ok=True)
    json_output_path = os.path.join(output_folder, f'formattedData_{timestamp}.json')
    csv_output_path = os.path.join(output_folder, f'formattedData_{timestamp}.csv')
    
    with open(json_output_path, 'w', encoding='utf-8') as f:
      json.dump(formatted_data, f, indent=2)
    print(f"Formatted data saved to {json_output_path}")

    if isinstance(formatted_data, list):
        df = pd.DataFrame(formatted_data)
        df.to_csv(csv_output_path, index=False, encoding='utf-8')
        print(f'Formatted data saved to {csv_output_path}')
    elif isinstance(formatted_data, dict):
        df = pd.DataFrame([formatted_data])
        df.to_csv(csv_output_path, index=False, encoding='utf-8')
        print(f'Formatted data saved to {csv_output_path}')
    else:
      print("Formatted data is neither a list nor a dictionary cannot save as csv.")

def main():
    """Main function to execute the scraping, formatting, and saving process."""
    url = "https://www.zillow.com/salt-lake-city-ut/"
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    try:
        raw_data = scrape_data(url)
        save_raw_data(raw_data, timestamp)
        formatted_data = format_data(raw_data)
    
        if formatted_data:
            print("Extracted Data:")
            print(json.dumps(formatted_data, indent=2))
            save_formatted_data(formatted_data, timestamp)
        else:
            print("Could not get formatted data.")
            
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
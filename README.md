# Scraper with Firecrawl and Gemini AI

This Python project scrapes real estate data from Zillow using the Firecrawl API, extracts specific information using Google's Gemini AI API, and saves the extracted data into JSON and CSV files. It's designed to handle large web pages by chunking the content before sending it to the Gemini API.

## Features

-   **Web Scraping:** Uses Firecrawl to extract markdown content from a given URL.
-   **Data Extraction:** Leverages Google's Gemini AI API to extract structured information from the scraped text into JSON format.
-   **Chunking:** Handles large amounts of text by splitting the data into smaller chunks before sending to the Gemini API, respecting API limits.
-   **Data Saving:** Saves both the raw markdown data and the extracted JSON data. Additionally, saves the JSON data in CSV format.
-   **Error Handling:** Includes robust error handling for API calls, JSON parsing, and file operations.
-   **Environment Variables:** Uses a `.env` file for easy management of API keys.

## Prerequisites

Before running the project, make sure you have the following:

-   **Python 3.6+**
-   **Firecrawl API key:** You will need to sign up for Firecrawl and get an API key.
-   **Google Gemini API key:** You will need a Google Cloud project with access to the Gemini AI API.
-   **Installed Python Packages:**
    ```bash
    pip install firecrawl google-generativeai python-dotenv pandas
    ```

## Setup

1.  **Clone Repository:** Clone this repository to your local machine.
2.  **Install Packages:** Install all dependencies using pip:
   ```bash
   pip install -r requirements.txt
content_copy
download
Use code with caution.
Markdown

Create .env File: In the root directory of the project, create a .env file and add your API keys:

FIRE_CRAWL_API=your_firecrawl_api_key
GEMINI_API=your_gemini_api_key
content_copy
download
Use code with caution.
Env

Replace your_firecrawl_api_key and your_gemini_api_key with your actual API keys.

Run the Script Navigate to the project root and run:

python zillow_scraper.py
content_copy
download
Use code with caution.
Bash
Usage

Modify the URL: Open zillow_scraper.py and modify the url variable in the main() function to the Zillow page you want to scrape.

Run the Script: Execute python zillow_scraper.py.

Data Output: The script will create an output folder in the project directory, which will contain the following files:

rawData_[timestamp].md: The raw markdown scraped from the website.

formattedData_[timestamp].json: The structured JSON data extracted by Gemini AI.

formattedData_[timestamp].csv: The structured data from the json saved as a CSV file.

Code Structure

firecrawl.py: Python module for interacting with Firecrawl, found in the firecrawl folder.

zillow_scraper.py: The main script containing:

scrape_data(url): Scrapes the provided URL using Firecrawl.

save_raw_data(raw_data, timestamp, output_folder='output'): Saves raw markdown data to a file.

chunk_data(data, chunk_size=2000): Chunks the provided text data into smaller pieces for processing with the API.

format_data(data, fields=None): Formats scraped data using Gemini AI API.

save_formatted_data(formatted_data, timestamp, output_folder='output'): Saves formatted data to JSON and CSV files.

main(): The main execution function to tie the script together.

.env: File for storing environment variables like api keys.

requirements.txt: File listing all needed dependencies to be installed with pip.

output Folder: Folder to store all output files.

Important Notes

API Limits: Be aware of the usage limits of the Firecrawl and Google Gemini APIs. The free tiers are limited. If you hit the limits you will need to wait or upgrade your account.

Chunk Size: The chunk_size in chunk_data determines how large each chunk of text sent to the Gemini API is. You can adjust this based on the size and structure of the page.

Field Customization: The default fields to extract are in the format_data() function. You can change the fields list to customize what information you want to extract.

Error Handling: The project includes error handling to prevent crashes; however, it might not cover all edge cases. Monitor the console for any warnings or error messages.

Output Data: The output is saved with timestamps in the filenames so you can track different runs of the script.

Disclaimer

This project is provided as-is and is intended for educational and personal use. Please use it responsibly, adhering to the terms of service for both Firecrawl and Google's Gemini API. Scraping data may be subject to website terms, so be aware of the restrictions of scraping sites you do not own.

Contributing

Feel free to contribute to this project by submitting issues, suggesting improvements, or creating pull requests.

**How to Use:**

1.  **Save as `README.md`:** Copy the above content and save it as a file named `README.md` in the root directory of your project.
2.  **View:** The file will be automatically formatted in markdown when viewed on GitHub, GitLab, or similar platforms.

This `README.md` file provides a good overview of your project, instructions for setting it up, and a clear description of how to use it. Let me know if you have any more questions!
content_copy
download
Use code with caution.
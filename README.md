# DRUGSCOMIC: Automated Interactions Checker

## Project Overview
DRUGSCOMIC (Drugs.Com Interaction Checker) is a tool to perform automated search of binary drugs interactions using interaction checker toolkit from drugs.com (https://www.drugs.com/drug_interactions.html). The script works using Selenium with Chromedriver to perform operations without user intervention, such as searching for drugs combination and extracting useful text from the results page. Drugs keyworks are given as active molecule names to avoid inconsistency and increase the chances to actually find the desired drugs. Eventually, the extracted data is saved as .csv file. This will includes several features such as severity of interactions, description and literature references, as well as adverse interactions with food and other products.

## Installation 
First, ensure that you have Python 3.10.12 installed on your system. Then, you can easily install the required Python packages using the provided requirements.txt file:

`pip install -r requirements.txt` 

## How to use
Run the main file DRUGSCOMIC.py to start the scraper. The drugs_dataset.csv file in the dataset folder must contain the list of drug names which interactions needed to be checked. Once the scraper has finished its job, the file drugs_interactions.csv will appear in the same folder. This file report the following:

- **Drugs** The drug combination for which the data has been extracted`
- **Total interactions** Total number of interactions
- **Minor interactions** Number of minor interactions
- **Moderate interactions** Number of moderate interactions
- **Major interactions** Number of major interactions
- **Drug to drug interactions** Description of interactions between drugs 
- **Drug to food interactions** Description of interactions between drugs and food                    




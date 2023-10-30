# DrugsCom interactions checker

## Project description
This is a web scraper aimed at extracting drugs interactions data, using the well known drugs.com interaction checker toolkit (https://www.drugs.com/drug_interactions.html). This scritp works using Selenium to automatically pilot the chromedriver and perform operations without user intervention. Drugs keyworks are given as active molecule names, allowing to search for binary interactions of all the given keywords combinations. The extracted data is then saved as .csv file, and includes several features such as severity of interactions, description and literature references, as well as adverse interactions with food and other products.

## How to use
Run the main file DCIC_launcher.py to strat the scraper. The drugs_dataset.csv file in the dataset folder must contain the list of drug names which interactions needed to be checked. Once the scraper has finished its job, the file drugs_interactions.csv will appear in the same folder. This file report the following:

- `Drugs: The drug combination for which the data has been extracted`
- `Total interactions: Total number of interactions`
- `Minor interactions: Number of minor interactions` 
- `Moderate interactions: Number of moderate interactions`
- `Major interactions: Number of major interactions`
- `Drug to drug interactions: Description of interactions between drugs` 
- `Drug to food interactions: Description of interactions between drugs and food`                       

### Requirements
This application has been developed and tested using the following dependencies (Python 3.10.12):

- `art==6.1`
- `pandas==2.0.3`
- `selenium==4.11.2`
- `webdriver-manager==4.0.1`

These dependencies are specified in the provided `requirements.txt` file to ensure full compatibility with the application. 

import os
import art
import pandas as pd
from itertools import combinations


# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------
from modules.components.scraper_assets import WebDriverToolkit, DrugComScraper
import modules.global_variables as GlobVar
import modules.configurations as cnf

# welcome message
#------------------------------------------------------------------------------
ascii_art = art.text2art('Drugs.com IC')
print(ascii_art)

# [LOAD AND PREPARE DATA]
#==============================================================================
# Load patient dataset and dictionaries from .csv files in the dataset folder.
# Also, create a clean version of the exploded dataset to work on
#==============================================================================

# activate chromedriver and scraper
#------------------------------------------------------------------------------
modules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
WD_toolkit = WebDriverToolkit(modules_path, GlobVar.data_path, headless=cnf.headless)
webdriver = WD_toolkit.initialize_webdriver()

# activate chromedriver
#------------------------------------------------------------------------------
filepath = os.path.join(GlobVar.data_path, 'drugs_dataset.csv')                
df_drugs = pd.read_csv(filepath, sep= ';', encoding='utf-8')

# get list of drugs
#------------------------------------------------------------------------------
drug_names = df_drugs['drug name'].to_list()
active_molecules = df_drugs['active molecule'].to_list()
unique_active_molecules = list(set(active_molecules))
drug_combinations = list(combinations(unique_active_molecules, 2))

# look for drugs interactions
#------------------------------------------------------------------------------
print(f'''
-------------------------------------------------------------------------------
SEARCH FOR BINARY DRUGS INTERACTIONS
-------------------------------------------------------------------------------
Checking interactions for the following combinations (as per data source)
''')
for combo in drug_combinations:
    print(combo)

print()
webscraper = DrugComScraper(webdriver)
interactions = webscraper.search_binary_interactions(drug_combinations)

# create dataset and save it as .csv file
#------------------------------------------------------------------------------
df_interactions = pd.DataFrame(interactions)
file_loc = os.path.join(GlobVar.data_path, 'drugs_interactions.csv')    
df_interactions.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')

















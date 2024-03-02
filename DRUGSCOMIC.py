import os
import pandas as pd
from itertools import combinations

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------
from components.scraper_assets import WebDriverToolkit, DrugComScraper
import components.global_paths as globpt
import configurations as cnf

# [LOAD AND PREPARE DATA]
#==============================================================================
#==============================================================================

# activate chromedriver and scraper
#------------------------------------------------------------------------------
WDtoolkit = WebDriverToolkit(globpt.data_path, 
                             headless=cnf.headless, 
                             ignore_SSL_errors=cnf.ignore_SSL_errors)
webdriver = WDtoolkit.initialize_webdriver()

# activate chromedriver
#------------------------------------------------------------------------------
filepath = os.path.join(globpt.data_path, 'drugs_dataset.csv')                
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
Checking interactions for the following combinations (as per data source)\n''')
for combo in drug_combinations:
    print(f'{combo[0]} vs {combo[1]}')

# perform search of binary interactions between drugs
webscraper = DrugComScraper(webdriver)
extracted_text = webscraper.binary_interactions_checker(drug_combinations, cnf.waiting_time)

# create dataset and save it as .csv file
#------------------------------------------------------------------------------
df_interactions = pd.DataFrame(interactions)
# file_loc = os.path.join(globpt.data_path, 'drugs_interactions.csv')    
# df_interactions.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')






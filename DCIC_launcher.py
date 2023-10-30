import sys
import os
import re
import art
import pandas as pd
from itertools import combinations
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------
from modules.components.scraper_classes import WebDriverToolkit, DrugComScraper
import modules.global_variables as GlobVar
import modules.configurations as cnf

# welcome message
#------------------------------------------------------------------------------
ascii_art = art.text2art('Drugs.com IC')
print(ascii_art)

# [ACTIVATE CHROMEDRIVER VERSION]
#==============================================================================
# ...
#==============================================================================
print('''
Activating chromedriver. Check version for compatibility with the program
      
''')

# check if chromedriver is present
#------------------------------------------------------------------------------
modules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
if cnf.check_CD_version == True:
    chromedriver_check = False    
    for file_name in os.listdir(modules_path):            
        if 'chromedriver' in file_name:
            chromedriver_check = True
    if chromedriver_check == False:
        version = os.popen('google-chrome --version').read() 
        version_number = re.search(r'\d+', version).group(0)
        driver_path = ChromeDriverManager(version=version, chrome_type=ChromeType.GOOGLE).install()

# activate chromedriver
#------------------------------------------------------------------------------
WD_toolkit = WebDriverToolkit(modules_path)
webdriver = WD_toolkit.initialize_webdriver()

# [LOAD AND PREPARE DATA]
#==============================================================================
# Load patient dataset and dictionaries from .csv files in the dataset folder.
# Also, create a clean version of the exploded dataset to work on
#==============================================================================

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

print(f'''
Starting the scraper. This may take a while....
''')

webscraper = DrugComScraper(webdriver)
interactions = webscraper.search_binary_interactions(drug_combinations)

# create dataset
#------------------------------------------------------------------------------
df_interactions = pd.DataFrame(interactions)

# save csv files
#------------------------------------------------------------------------------
file_loc = os.path.join(GlobVar.data_path, 'drugs_interactions.csv')    
df_interactions.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')

















import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re




# define the class for inspection of the input folder and generation of files list.
#==============================================================================
#==============================================================================
#==============================================================================
class WebDriverToolkit:
    
    """
    Initializes a webdriver instance with Chrome options set to disable images loading.
    
    Keyword arguments:
    
    wd_path (str): The file path to the Chrome webdriver executable
    
    Returns:
        
    None 
    
    """
    def __init__(self, path):
        self.path = os.path.join(path, 'chromedriver.exe')       
        self.option = webdriver.ChromeOptions()
        self.service = Service(executable_path=self.path)
        self.chrome_prefs = {}
        self.option.experimental_options['prefs'] = self.chrome_prefs
        self.chrome_prefs['profile.default_content_settings'] = {'images': 2}
        self.chrome_prefs['profile.managed_default_content_settings'] = {'images': 2} 

    def initialize_webdriver(self):
        driver = webdriver.Chrome(service=self.service, options=self.option) 
        
        return driver    
        
    
# define the class for inspection of the input folder and generation of files list
#==============================================================================
#==============================================================================
#==============================================================================
class DrugComScraper: 

    def __init__(self, driver):         
        self.driver = driver
        self.IC_URL = 'https://www.drugs.com/drug_interactions.html'
        self.drugs_interactions = {'drugs' : [],
                                    'total interactions' : [],
                                    'major interactions' : [],
                                    'moderate interactions' : [],
                                    'minor interactions' : [],
                                    'food interactions' : [],
                                    'drug to drug interactions' : [],
                                    'drug to food interactions' : []}
        
    #==========================================================================
    def search_bar_access(self, time):  
        wait = WebDriverWait(self.driver, time)
        accept_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ddc-modal"]/div/div/form/a[2]')))    
        accept_button.click()
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="livesearch-interaction-basic"]')
        search_bar.clear()

        return search_bar
    
    #==========================================================================
    def inject_name(self, time, search_bar, name):  
        wait = WebDriverWait(self.driver, time)
        search_bar.send_keys(name)
        add_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/form/div/input')))
        add_button.click()        
        search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="livesearch-interaction"]')))
        search_bar.clear()
        
        return search_bar
    
    #==========================================================================
    def extract_data(self, time, drug_A, drug_B):  
        wait = WebDriverWait(self.driver, time)
        num_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/p[1]'))).text.split()[0]
        major_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="filterSection"]/div[1]'))).text.split()[-1]
        moderate_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="filterSection"]/div[2]'))).text.split()[-1]
        minor_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="filterSection"]/div[3]'))).text.split()[-1]
        food_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="filterSection"]/div[4]'))).text.split()[-1]
        self.drugs_interactions['drugs'].append(f'{drug_A} vs {drug_B}')
        self.drugs_interactions['total interactions'].append(num_interactions)
        self.drugs_interactions['major interactions'].append(re.findall(r'\((.*?)\)', major_interactions)[0])
        self.drugs_interactions['moderate interactions'].append(re.findall(r'\((.*?)\)', moderate_interactions)[0])
        self.drugs_interactions['minor interactions'].append(re.findall(r'\((.*?)\)', minor_interactions)[0])
        self.drugs_interactions['food interactions'].append(re.findall(r'\((.*?)\)', food_interactions)[0])                
        num_drug2drug_interactions = int(re.findall(r'\((.*?)\)', major_interactions)[0]) + int(re.findall(r'\((.*?)\)', moderate_interactions)[0]) + int(re.findall(r'\((.*?)\)', minor_interactions)[0])
        num_drug2food_interactions = int(re.findall(r'\((.*?)\)', food_interactions)[0])

        drug2drug_descriptions = []
        drug2food_descriptions = []
        if num_drug2drug_interactions > 0:
            for i in range(num_drug2drug_interactions):
                drug2drug = self.driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[2]/div/p[{i+1}]').text
                drug2drug_descriptions.append(drug2drug)
        else:
            drug2drug_descriptions.append('None found')
                
        if num_drug2food_interactions > 0:
            for i in range(num_drug2food_interactions):
                drug2food = self.driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[3]/div/p[{i+1}]').text
                drug2food_descriptions.append(drug2food)
        else:
            drug2food_descriptions.append('None found')                
        
        self.drugs_interactions['drug to drug interactions'].append(drug2drug_descriptions)        
        self.drugs_interactions['drug to food interactions'].append(drug2food_descriptions)
       
        return self.drugs_interactions    

    #==========================================================================
    def search_binary_interactions(self, keywords_pair):
         
        for i, pair in enumerate(keywords_pair):
            try:
                if i == 0:                 
                    wait = WebDriverWait(self.driver, 10)
                    self.driver.get(self.IC_URL) 
                    search_bar = self.search_bar_access(5)
                else:
                    wait = WebDriverWait(self.driver, 10)
                    self.driver.get(self.IC_URL) 
                    search_bar = self.driver.find_element(By.XPATH, '//*[@id="livesearch-interaction-basic"]')
                    search_bar.clear()                          
                for K in pair:
                    try:
                        search_bar = self.inject_name(10, search_bar, K)                        
                    except:
                        print(f'Drug {K} not found! Skipping this item')
                research_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="interaction_list"]/div/a[1]')))    
                research_button.click()           
                drugs_interactions = self.extract_data(10, pair[0], pair[1])                   

            except Exception as e:
                drugs_interactions = self.drugs_interactions
                print(f'An error occurred, skipping this drugs combination: {pair[0]} and {pair[1]}') 
                

                   

        return drugs_interactions


                    
                
            
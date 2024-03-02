import os
import re
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# [WEBDRIVER]
#==============================================================================
# Web driver toolkit 
#==============================================================================
class WebDriverToolkit:    
    
    def __init__(self, download_path, headless=True, ignore_SSL_errors=True):        
        self.download_path = download_path      
        self.option = webdriver.ChromeOptions()        
        if headless==True:
            self.option.add_argument('--headless')
        if ignore_SSL_errors==True: 
            self.option.add_argument('--ignore-ssl-errors=yes')
            self.option.add_argument('--ignore-certificate-errors')       
        self.chrome_prefs = {'download.default_directory' : download_path}
        self.option.experimental_options['prefs'] = self.chrome_prefs
        self.chrome_prefs['profile.default_content_settings'] = {'images': 2}
        self.chrome_prefs['profile.managed_default_content_settings'] = {'images': 2}

    #--------------------------------------------------------------------------
    def initialize_webdriver(self): 

        '''
        This method downloads and installs the Chrome WebDriver executable if needed, 
        creates a WebDriver service, and initializes a Chrome WebDriver instance
        with the specified options.

        Returns:
            driver: A Chrome WebDriver instance.
        '''   
        self.path = ChromeDriverManager().install()
        self.service = Service(executable_path=self.path)
        driver = webdriver.Chrome(service=self.service, options=self.option)                   
        
        return driver
            
    
# [SCRAPER]
#==============================================================================
# Series of method to scrape data from drugs.com
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
        
    #--------------------------------------------------------------------------
    def search_bar_access(self, time):  

        '''
        Access the search bar, clear its contents, and return the search bar element.

        Keywords arguments
            time (int): The maximum time (in seconds) to wait for the "Accept" button to appear.

        Returns:
            search_bar: The WebElement representing the search bar.

        '''
        wait = WebDriverWait(self.driver, time)
        accept_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ddc-modal"]/div/div/form/a[2]')))    
        accept_button.click()
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="livesearch-interaction-basic"]')
        search_bar.clear()

        return search_bar
    
    #--------------------------------------------------------------------------
    def inject_names_pair(self, time, search_bar, name_pair):

        '''
        Inject a name into the search bar, click the "Add" button, and clear the search bar.

        Keyword Arguments:
            time (int): The maximum time (in seconds) to wait for elements to appear.
            search_bar: The WebElement representing the search bar.
            name (str): The name to inject into the search bar.

        Returns:
            None
        '''
        name_1, name_2 = name_pair        
        wait = WebDriverWait(self.driver, time)
        search_bar.send_keys(name_1) 
        # wait for the results dropdown to appear
        results = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ls-wrap"]/div/a[1]')))     
        # Ensure the 'Add' button is located correctly and wait for it to be clickable
        # to add the first drug name
        css_selector = "input.ddc-btn[type='submit'][value='Add']"
        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))       
        add_button.click()        
        search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="livesearch-interaction"]')))
        search_bar.clear()
        # Ensure the 'Add' button is located correctly and wait for it to be clickable
        # to add the second drug name        
        search_bar.send_keys(name_2)       
        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))        
        add_button.click()
            

    #--------------------------------------------------------------------------
    def extract_text_data(self, driver, drug_A, drug_B):  

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)

        return text

    #--------------------------------------------------------------------------
    def binary_interactions_checker(self, keywords_pair, wait_time=10):

        '''
        Process drug interactions for a list of keyword pairs.

        Keyword Arguments:
            keywords_pair (list of tuples): A list of tuples, each containing two drug keywords to search for.

        Returns:
            drugs_interactions: A dictionary containing drug interaction data for each pair of drugs.

        ''' 
        text_dictionary = {}        
        for i, pair in enumerate(keywords_pair):
            try:
                if i == 0:                 
                    wait = WebDriverWait(self.driver, wait_time)
                    self.driver.get(self.IC_URL) 
                    search_bar = self.search_bar_access(wait_time)
                else:
                    wait = WebDriverWait(self.driver, wait_time)
                    self.driver.get(self.IC_URL) 
                    search_bar = self.driver.find_element(By.XPATH, '//*[@id="livesearch-interaction-basic"]')
                    search_bar.clear()                          
                try:
                    self.inject_names_pair(wait_time, search_bar, pair)                        
                except:
                    print(f'Cannot find info on this drugs combination: {pair}')
                research_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="interaction_list"]/div/a[1]')))    
                research_button.click()                  
                extracted_text = self.extract_text_data(self.driver, pair[0], pair[1])   
                text_dictionary[f'{pair[0]} vs {pair[1]}'] = extracted_text           
            except Exception as e:
                drugs_interactions = self.drugs_interactions
                print(f'An error occurred, skipping this drugs combination: {pair[0]} and {pair[1]}')                  

        return text_dictionary


                    
                
            
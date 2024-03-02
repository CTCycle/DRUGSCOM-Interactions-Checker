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
class TextMining: 

    #--------------------------------------------------------------------------
    def text_lookup(self, text):  

        '''
        Extract interaction data between two drugs from a webpage and store it in a dictionary.

        Keyword Arguments:
            time (int): The maximum time (in seconds) to wait for elements to appear.
            drug_A (str): The name of the first drug.
            drug_B (str): The name of the second drug.

        Returns:
            self.drugs_interactions: A dictionary containing interaction data, including total interactions, major interactions,
                                     moderate interactions, minor interactions, food interactions, drug to drug interactions, and
                                     drug to food interactions.

        '''
        wait = WebDriverWait(self.driver, time) 
        num_interactions = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/p[1]'))).text.split()[0]
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
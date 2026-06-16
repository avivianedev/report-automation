import os
from datetime import date
import dotenv
import keyring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.automation.utils.dates import generate_date_range, generate_formatted_date

from dotenv import load_dotenv
from pathlib import Path

from src.automation.core.base_engine import BaseAutomationEngine
from src.automation.utils.logger import get_logger

root = Path(__file__).resolve().parents[3]
load_dotenv(root / ".env")

data = date.today()
logger = get_logger('verisys')

class VerisysSeleniumEngine(BaseAutomationEngine):
    def __init__(self):     

        self.USERNAME = os.getenv('USER')
        self.SERVICE = os.getenv('SERVICE')
        self.pwd = keyring.get_password(self.SERVICE, self.USERNAME) 
        self.driver = None
        
       
    def get_driver(self):          
        URL = os.getenv('URL')
            
        if not URL:
            logger.error("Variável de ambiente URL não definida.")
            raise RuntimeError("Variável de ambiente URL não definida.") 
            
            
        lista_urls = URL.split(',')    

        for url in lista_urls:
            url = url.strip() 
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(2)
            try:     
                logger.info(f"Tentando conexão com: {url}")
                self.driver.get(url)
                logger.info(f'Conexão realizada com: {url}')
                return self.driver
            
            except Exception as e:
                logger.exception(f"Falha ao conectar ao driver. Erro: {e}")   
                self.driver.quit()   
                continue  
        return None       
    
    def authentication(self,):  
        try:              
            wait = WebDriverWait(self.driver, 10) 
            user_field = wait.until(EC.element_to_be_clickable((By.NAME, 'txt_user')))
            user_field.clear()
            user_field.send_keys(self.USERNAME)

            pass_field = wait.until(EC.element_to_be_clickable((By.NAME, 'txt_pass')))
            pass_field.clear()
            pass_field.send_keys(self.pwd)

            login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'cmd_login')))
            login_button.click()

        except Exception as e:
            logger.error('Falha na autenticação. Erro: ', e)         
        
        


    def select_report(self, options):  
        wait = WebDriverWait(self.driver, 20)
        
        try:
            old_rel = self.driver.find_element(By.ID, "CPH_ddl_tipos")
            Select(self.driver.find_element(By.ID, "CPH_ddl_tipos")).select_by_index(options[0])
            wait.until(EC.staleness_of(old_rel))

            select_type =  wait.until(
                    EC.presence_of_element_located((By.ID, 'CPH_ddl_relatorios'))
            )
            Select(select_type).select_by_index(options[1])

            select_data_initial = self.driver.find_element(By.NAME, 'ctl00$CPH$f_data_multipla_inicial')
            select_data_initial.clear()
            range_date = generate_date_range()
            select_data_initial.send_keys(generate_formatted_date(range_date[0], '"%d%m%Y"'))
        

            select_data_end = self.driver.find_element(By.NAME, 'ctl00$CPH$f_data_multiplo_final')
            select_data_end.clear()
            select_data_end.send_keys(generate_formatted_date(range_date[1], '"%d%m%Y"'))     
                            
        except Exception as e:
            logger.error(f'Erro ao selecionar os campos do relatório. Erro {e}',)           

    def select_groups(self, group_dac):
        wait = WebDriverWait(self.driver, 20)   
        try:
            for el in group_dac:
                group = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                f"//input[@type='image' and contains(@onclick, 'Adicionar${el}')]"
                )))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", group)
                group.click()       

            wait.until(EC.staleness_of(group))

        except Exception as e:
            logger.exception(f'Erro ao selecionar o Grupo Dac do relatório. Erro {e}',)


    def select_options_report(self, list_options):
        wait = WebDriverWait(self.driver, 30)
        try:
            option_box = wait.until(EC.element_to_be_clickable((By.ID, 'CPH_cb_colunas')))
            option_box.click()
            wait.until(EC.staleness_of(option_box))
        
            for op in list_options:
                element_id = f'CPH_cbl_colunas_{op}'            
                element = wait.until(EC.presence_of_element_located((By.ID, f'{element_id}')))
                element.click()       
                
            button = wait.until(EC.element_to_be_clickable((By.ID, 'CPH_cmd_gerar')))
            button.click()
            
            wait.until(EC.number_of_windows_to_be(2))
            self.driver.switch_to.window(self.driver.window_handles[-1])

            select_element = wait.until(EC.presence_of_element_located((By.ID, 'RS_Viewer_ctl01_ctl05_ctl00')))
            Select(select_element).select_by_index(2)

            export_button = wait.until(EC.element_to_be_clickable((By.ID, 'RS_Viewer_ctl01_ctl05_ctl01')))
            export_button.click()
        
        except Exception as e:
            logger.exception(f'Erro ao selecionar as colunas do relatório. Erro {e}',)



    def run_report(self, config): 
            driver = self.get_driver()
            if not driver:
                logger.error("[ERROR] Não foi possível iniciar o driver. Abortando.")
                return False
            try:      
                self.authentication() 
                self.select_report(config["report_selection"])
                self.select_groups(config["groups_dac"])
                self.select_options_report(config['columns'])
                logger.info('Automação Selenium executada com sucesso')
                return True
            except Exception as e:
                logger.exception(f"[ERROR] run_report falhou: {e}")
                return False
            
    def close(self,):
        if self.driver:            
            self.driver.quit()
            logger.info('Driver finalizado!')
                


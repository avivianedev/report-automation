from datetime import time
import dotenv
import keyring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.automation.utils.dates import generate_formated_date, generate_date_range
import time
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[2] / ".env") 


URL = os.getenv('URL')
USERNAME = os.getenv('USER')
SERVICE = os.getenv('SERVICE')
pwd = keyring.get_password(SERVICE, USERNAME)

def get_driver():
    driver = webdriver.Firefox()
    try:      
        if not URL:
            raise RuntimeError("Variável de ambiente URL não definida.") 
        
        driver.implicitly_wait(5) 
        driver.get(URL)
        return driver
    except Exception as e:
        print(f"Falha ao conectar ao driver. Erro: {e}")   
        driver.quit()     
        return None            
        

def authentication(driver):
    #driver.implicitly_wait(5) 
    wait = WebDriverWait(driver, 10) 
    user_field = wait.until(EC.element_to_be_clickable((By.NAME, 'txt_user')))
    user_field.clear()
    user_field.send_keys(USERNAME)

    pass_field = wait.until(EC.element_to_be_clickable((By.NAME, 'txt_pass')))
    pass_field.clear()
    pass_field.send_keys(pwd)

    login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'cmd_login')))
    login_button.click()


def select_report(driver, options):    
    wait = WebDriverWait(driver, 10)
    try:
        old_rel = driver.find_element(By.ID, "CPH_ddl_tipos")
        Select(driver.find_element(By.ID, "CPH_ddl_tipos")).select_by_index(options[0])
        wait.until(EC.staleness_of(old_rel))

        select_type =  wait.until(
                EC.presence_of_element_located((By.ID, 'CPH_ddl_relatorios'))
        )
        Select(select_type).select_by_index(options[1])

        select_data_initial = driver.find_element(By.NAME, 'ctl00$CPH$f_data_multipla_inicial')
        select_data_initial.clear()
        range_date = generate_date_range()
        select_data_initial.send_keys(generate_formated_date(range_date[0], '"%d%m%Y"'))
    

        select_data_end = driver.find_element(By.NAME, 'ctl00$CPH$f_data_multiplo_final')
        select_data_end.clear()
        select_data_end.send_keys(generate_formated_date(range_date[1], '"%d%m%Y"'))     
                        
    except Exception as e:
        print(f'Erro ao selecionar os campos do relatório. Erro {e}',)
        #driver.quit()


def select_groups(driver, group_dac):
    wait = WebDriverWait(driver, 10)   
    try:
        for el in group_dac:
            group = wait.until(EC.element_to_be_clickable((
            By.XPATH, 
            f"//input[@type='image' and contains(@onclick, 'Adicionar${el}')]"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", group)
            group.click()       

        wait.until(EC.staleness_of(group))

    except Exception as e:
        print(f'Erro ao selecionar o Grupo Dac do relatório. Erro {e}',)


def select_options_report(driver, list_options):
    wait = WebDriverWait(driver, 30)
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
        
        #Troca Aba
        wait.until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[-1])

        select_element = wait.until(EC.presence_of_element_located((By.ID, 'RS_Viewer_ctl01_ctl05_ctl00')))
        Select(select_element).select_by_index(2)

        export_button = wait.until(EC.element_to_be_clickable((By.ID, 'RS_Viewer_ctl01_ctl05_ctl01')))
        export_button.click()
       
    except Exception as e:
        print(f'Erro ao selecionar as colunas do relatório. Erro {e}',)
         

def run_report(driver, config): 
        try:       
            select_report(driver, config["report_selection"])
            select_groups(driver, config["groups_dac"])
            select_options_report(driver, config['columns'])
            return True
        except Exception as e:
            print(f"[ERROR] run_report falhou: {e}")
            return False
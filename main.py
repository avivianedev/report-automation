import sys, os
from pathlib import Path
from src.automation.io.file_ops import move_file
from src.automation.app import authentication, get_driver,run_report
from src.automation.config.config import REPORTS

sys.path.append(str(Path(__file__).resolve().parent / "src"))

if __name__ == "__main__":   
    
    for key in ['C6']:
        driver = get_driver()  
        authentication(driver)
        config = REPORTS[key]

        try:            
            response = run_report(driver, config) 
            if response:
                print(f'Relatório {key} extraído com sucesso')                
                try:
                    move_file(config['src'], Path(config['dst'])) 
                except Exception as e:
                    print(f'Falha ao mover arquivo. Erro: {e}')          
        except Exception as e:
            print(f'Falha no relatório {key}')                
        finally:            
            driver.quit() 
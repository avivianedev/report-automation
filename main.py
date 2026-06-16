import sys, os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from src.automation.io.file_ops import move_file
from src.automation.config.config import REPORTS
from src.automation.engines.verisys_selenium import VerisysSeleniumEngine
from src.automation.engines.robbu_playwright import RobbuPlaywrightEngine
from src.automation.utils.logger import get_logger
 

logger = get_logger('main')

ENGINES_MAP = {
    'C6': VerisysSeleniumEngine,
    'ROBBU_WHATSAPP': RobbuPlaywrightEngine
    
}


def execute_automation(report_key: str):
    if report_key not in ENGINES_MAP:
        logger.error(f"Configuração não encontrada para o relatório: {report_key}")
        return
    
    config = REPORTS.get(report_key)

    engine_class = ENGINES_MAP[report_key]
    engine = engine_class()
    try:  
        success  = engine.run_report(config)
        if success :
            if 'src' in config and 'dst' in config:
                try:
                    move_file(config['src'], Path(config['dst']))                    
                except Exception as e:
                    logger.exception(f"Falha ao mover arquivo de {report_key}. Erro: {e}")        

    except Exception as e:
        logger.exception(f"Erro na execução de {report_key}: {e}")
    finally:
        engine.close()
        
    
if __name__ == "__main__": 
    execute_automation('ROBBU_WHATSAPP')
    execute_automation('C6')
   
   
    
    
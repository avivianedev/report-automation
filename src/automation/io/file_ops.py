from datetime import date
import os , sys
from pathlib import Path
import shutil
import time

from src.automation.utils.dates import generate_formatted_date
from src.automation.utils.logger import get_logger

sys.path.append(str(Path(__file__).resolve().parents[2])) 

logger = get_logger('files')


def move_file(src, dst):    
    # today = today = date.today()
    DOWNLOAD_PATH = Path(src)
    # DEST_PATH = dst/ f'{generate_formated_date(today, "%Y-%m-%d")}.xlsx'
    DEST_PATH = dst/ 'chamadas.xlsx'
    
    if os.path.exists(DEST_PATH):
            os.remove(DEST_PATH)
            logger.info('Arquivo removido.')
    try:              
        time.sleep(5)
        shutil.move(DOWNLOAD_PATH, DEST_PATH)
        logger.info(f"Arquivo movido para: {DEST_PATH}")

    except Exception as e:
        logger.exception(f'Falha na movimentação dos arquivos. Erro: {e}')
    


 
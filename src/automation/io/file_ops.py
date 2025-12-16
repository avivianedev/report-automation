from datetime import date
import os , sys
from pathlib import Path
import shutil
import time

from src.automation.utils.dates import generate_formated_date

sys.path.append(str(Path(__file__).resolve().parents[2])) 


def move_file(src, dst):    
    today = today = date.today()
    DOWNLOAD_PATH = Path(src)
    DEST_PATH = dst/ f'{generate_formated_date(today, "%Y-%m-%d")}.xlsx'
    
    try:
        time.sleep(5)
        shutil.move(DOWNLOAD_PATH, DEST_PATH)
        print(f"Arquivo movido para: {DEST_PATH}")

    except Exception as e:
        print(f'Falha na movimentação dos arquivos. Erro: {e}')
    


 
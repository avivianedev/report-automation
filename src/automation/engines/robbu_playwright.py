import re
import os
from dotenv import load_dotenv
from pathlib import Path
import time

from playwright.sync_api import sync_playwright
from src.automation.config.config import REPORTS

from src.automation.core.base_engine import BaseAutomationEngine

root = Path(__file__).resolve().parents[3]
load_dotenv(root / ".env")

class RobbuPlaywrightEngine(BaseAutomationEngine):
    def __init__(self):
        self._playwright_context = None
        self.browser = None
        self.page = None

        self.url = os.getenv('ROBBU_URL')
        self.username = os.getenv('USER_ROBBU')
        self.password = os.getenv('PASSWORD')

    def authentication(self):
        self.page.get_by_role("textbox", name="Nome da empresa").fill('TI EDG SGR') 
        self.page.get_by_role("textbox", name="Nome de usuário ou Email").fill(self.username)
        self.page.get_by_role("textbox", name="Senha").fill(self.password)
        self.page.get_by_role("button", name="Entrar").click()       


    def select_report(self):
        self.page.get_by_text("Invenio Center").click()
        self.page.get_by_role("link", name="Relatórios").click()
        self.page.get_by_role("button", name="Gerar relatório").first.click()

        # Selecionado o modelo do Relatório
        self.page.get_by_role("textbox", name="Modelo do relatório").click()
        self.page.get_by_role("link", name="KPI - Eventos Este relatório").click()

           #selecionando as opções do relatório
        self.page.get_by_label("Período").select_option("5")
        self.page.locator("label").filter(has_text="Service Desk").click()
        self.page.locator("label").filter(has_text="VIP").click()
        self.page.locator("label").filter(has_text="Chamado Aberto Para Outra").click()
        self.page.locator("label").filter(has_text="Concluído Com Sucesso").click()
        self.page.locator("label").filter(has_text="Criação De Solicitação").click()
        self.page.locator("label").filter(has_text="Criação De Incidente").click()
        self.page.locator("label").filter(has_text="Desbloqueio De Login").click()
        self.page.locator("label").filter(has_text="Pendente Fornecedor").click()
        self.page.locator("label").filter(has_text="Sem Contato").click()    
        self.page.get_by_role("button", name="Gerar relatório").first.click()


    def wait_and_download(self, config : dict):
        reporter_container = self.page.locator(".list-item-container", has_text="KPI - Eventos").first.filter(has_text="Status:  Finalizado")
        print("Aguardando o processamento do relatório terminar...")

        reporter_container.wait_for(state="visible", timeout=300000)
        self.page.locator(".dots").first.click()

        with self.page.expect_download() as download_info:
            with self.page.expect_popup() as page1_info:
                self.page.get_by_role("link", name="Download").click()
            page1 = page1_info.value
        download = download_info.value

        #config = REPORTS.get('ROBBU')
        destination_path = Path(config.get('dst_path'))
        default_name = Path(config.get('final_filename'))
        final_path = destination_path / default_name

        try:
            download.save_as(final_path)
            print(f'Arquivo salvo em: {final_path}')
    
        except Exception as e:
            print(f"Erro ao abrir ou salvar arquivo padronizado: {e}")

        

    def run_report(self, config):
        try:
            self._playwright_context = sync_playwright().start()
            self.browser = self._playwright_context.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            
            self.page.goto(self.url)

            self.authentication()
            self.select_report()
            self.wait_and_download(config)
        

        except Exception as e:
            print(f"[ERROR] Falha na automação Robbu: {e}")
            return False

    def close(self):        
        if self.browser:
            self.browser.close()
        if self._playwright_context:            
            self._playwright_context.stop() 
        print("Playwright finalizado com sucesso.")


   




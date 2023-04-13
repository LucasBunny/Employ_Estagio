# Imports
import pandas as pd
import datetime
from unidecode import unidecode
import time
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


# URL Linkedin Jobs
url_linkedin = 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0'

# Configurações do Selenium
options = Options()
options.add_argument('window-size=2000,2000')
service = Service(ChromeDriverManager().install())

# Ativação do Selenium
navegador = webdriver.Chrome(service=service, options=options)


# Entra na URL de Empregos
navegador.get(url_linkedin)

time.sleep(2)

# Insere o Trabalho
input_job = navegador.find_element(By.ID, 'job-search-bar-keywords')
input_job.send_keys('Marketing e Publicidade')

time.sleep(2)

# Insere o País
input_country = navegador.find_element(By.ID, 'job-search-bar-location')
input_country.clear()
input_country.send_keys('Brazil')

time.sleep(2)

# Executa a Pesquisa
search_button = navegador.find_element(By.XPATH, '/html/body/div[1]/header/nav/section/section[2]/form/button').click()

time.sleep(2)

# Filtra por 'Trabalho Integral'
job_type_button = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/button').click()
time.sleep(3)
job_fulltime = navegador.find_element(By.ID, 'f_JT-0').click()
time.sleep(3)
submit_button1 = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/div/button').click()
time.sleep(2)

# Filtra por 'Estágio'
experience_button = navegador.find_element(By.XPATH, '//html/body/div[1]/section/div/div/div/form/ul/li[5]/div/div/button').click()
time.sleep(2)
intership_option = navegador.find_element(By.ID, 'f_E-0').click()
time.sleep(2)
submit_button2 = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[5]/div/div/div/button').click()
time.sleep(3)

# Pega o Conteúdo da Página
page_content = navegador.page_source
site = BeautifulSoup(page_content, 'html.parser')

# Checa o Total de Vagas
total_vagas = navegador.find_element(By.CLASS_NAME, 'results-context-header__job-count').text.replace('+', '').replace(',', '')
total_vagas = int(total_vagas)

for i in range(1, total_vagas):
    flag1 = True
    flag2 = True

    while flag1:
        try:
            # Clica no Card de Emprego
            navegador.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a')[0].click()
            time.sleep(2)
            navegador.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a')[0].click()
            time.sleep(2)
            flag1 = False

        except IndexError:
            # Clica no Botão 'See more jobs'
            navegador.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/button')[0].click()
            flag1 = True
            time.sleep(2)


    # --> Lista de Empregos Filtrados <--

    # Conteúdo HTML da Página
    page_content1 = navegador.page_source
    site1 = BeautifulSoup(page_content1, 'html.parser')
    dom1 = etree.HTML(str(site1))


    # --> Página da Empresa <--
    while flag2:
        try:
            navegador.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').click()
            flag2 = False
        except:
            flag2 = True

    # Troca de Janelas
    janela = navegador.window_handles[1]
    navegador.switch_to.window(janela)
    time.sleep(2)


    # Coleta de Conteúdo - 2º Janela
    page_content2 = navegador.page_source
    site2 = BeautifulSoup(page_content2, 'html.parser')
    dom2 = etree.HTML(str(site2))


    # Fecha 2º Janela 
    navegador.close()

    # Troca de Janelas
    janela = navegador.window_handles[0]
    navegador.switch_to.window(janela)

    time.sleep(2)


    # --> Funções para Coleta de Informações <--

    # URL da Vaga
    def url_vaga():
        return site1.find("a", {"class":"topcard__link"}).get('href')

    # Nome da Vaga
    def nome_vaga(): 
        return dom1.xpath(f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/div[2]/h3')[0].text.strip()

    # Nome da Empresa 
    def nome_empresa():
        return site1.find('a', {'class':'topcard__org-name-link'}).get_text(strip=True)
    
    # URL de Perfil da Empresa
    def url_empresa():
        return site1.find("a", {"class":"topcard__org-name-link"}).get('href')

    # Modelo de Contratacao (hibrido, presencial ou remoto)
    def modelo_contratacao():
        palavras = ['hibrido', 'presencial', 'remoto']
        descricao = site1.find("div", {"class":"description__text"}).get_text(strip=True)
        descricao = unidecode(descricao.lower())
        for palavra in palavras:
            if descricao.find(palavra) != -1:
                return palavra
            return None

    # Tipo de Contratação (tempo integral ou estágio)
    def tipo_contratacao(): 
        tipo = dom1.xpath('/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span')
        if tipo != []:
            return tipo[0].text.strip()
        return None
    
    # Nível de Experiência
    def nivel_experiencia():
        return site1.find("span", {"class":"description__job-criteria-text"}).get_text(strip=True)

    # Número de Vagas
    def numero_vagas():
        content = site1.find("span", {"class":"num-applicants__caption"}) 
        if content is None:
            return site1.find("figure", {"class":"num-applicants__figure"}).get_text(strip=True)
        return content.get_text(strip=True)

    # Tempo de Postagem da Vaga
    def data_postagem():
        return site1.find("span", {"class":"posted-time-ago__text"}).get_text(strip=True)

    # Horário do Scraping
    def horario():
        hora = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
        return hora

    # Número de Funcionários
    def numero_funcionarios():
        funcionarios = dom2.xpath('//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd')
        try:
            for i in funcionarios[0].text.strip():
                if not i.isdigit():
                    return dom2.xpath('//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[2]/dd')[0].text.strip()
                return funcionarios[0].text.strip()
        except IndexError:
            return None

    # Número de Seguidores
    def numero_seguidores():
        h3_tag = dom2.xpath('//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h3/text()[2]')
        try:
            return h3_tag[0].strip()
        except IndexError:
            return None

    # Localização da Sede da Empresa
    def local_empresa():
        return dom1.xpath(f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/div[2]/div/span')[0].text.strip()

    # URL da Candidatura
    def url_candidatura():
        return str(site1.find("code", {"id":"applyUrl"})).replace('<code id="applyUrl" style="display: none"><!--"', '').replace('--></code>', '')


    # --> Prints dos Resultados <--
    print(f"--> Resultados Obtidos - {i} de {total_vagas} <--", end='\n')

    dados = {
        'URL da Vaga' : str(url_vaga()),
        'Nome da Vaga' : str(nome_vaga()),
        'Nome da Empresa' : str(nome_empresa()),
        'URL da Empresa' : str(url_empresa()),
        'Modelo de Contratação' : str(modelo_contratacao()),
        'Tipo de Contratação' : str(tipo_contratacao()),
        'Nível de Experiência' : str(nivel_experiencia()),
        'Número de Candidaturas' : str(numero_vagas()),
        'Data da Postagem da Vaga' : str(data_postagem()),
        'Horário do Scraping' : str(horario()),
        'Número de Funcionários' : str(numero_funcionarios()),
        'Número de Seguidores' : str(numero_seguidores()),
        'Local Sede da Empresa' : str(local_empresa()),
        'URL da Candidatura' : str(url_candidatura())
    }
    
    dt = pd.DataFrame(dados, index=[0])
    print(dt, end='\n\n')

import time
from lxml import etree
from functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Apresentação / Filtros
limpar_tela()
print('Web Scraping - Linkedin')
input_vaga = input("Insira Nome da vaga: ")
input_pais = input("Insira o País: ")


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
input_job.send_keys(input_vaga)

time.sleep(2)

# Insere o País
input_country = navegador.find_element(By.ID, 'job-search-bar-location')
input_country.clear()
input_country.send_keys(input_pais)

time.sleep(2)

# Executa a Pesquisa
search_button = navegador.find_element(By.XPATH, '/html/body/div[1]/header/nav/section/section[2]/form/button').click()

time.sleep(2)

# Filtra por 'Trabalho Integral'
# job_type_button = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/button').click()
# time.sleep(3)
# job_fulltime = navegador.find_element(By.ID, 'f_JT-0').click()
# time.sleep(3)
# submit_button1 = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/div/button').click()
# time.sleep(2)

# Filtra por 'Estágio'
# experience_button = navegador.find_element(By.XPATH, '//html/body/div[1]/section/div/div/div/form/ul/li[5]/div/div/button').click()
# time.sleep(2)
# intership_option = navegador.find_element(By.ID, 'f_E-0').click()
# time.sleep(2)
# submit_button2 = navegador.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[5]/div/div/div/button').click()
# time.sleep(3)

# Pega o Conteúdo da Página
page_content = navegador.page_source
site = BeautifulSoup(page_content, 'html.parser')

# Checa o Total de Vagas
total_vagas = navegador.find_element(By.CLASS_NAME, 'results-context-header__job-count').text.replace('+', '').replace(',', '')
total_vagas = int(total_vagas)

for num_vaga in range(1, total_vagas):
    flag1 = True
    flag2 = True

    while flag1:
        try:
            # Clica no Card de Emprego
            navegador.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{num_vaga}]')[0].click()
            time.sleep(2)
            navegador.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{num_vaga}]')[0].click()
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

            flag2 = False
        except:
            dom2 = None
            flag2 = False

    time.sleep(2)

    # --> Prints dos Resultados <--
    limpar_tela()
    print(f"--> Resultados Obtidos - {num_vaga} de {total_vagas} <--", end='\n')

    dados = [
        {
        'URL da Vaga' : str(url_vaga(site1)),
        'Nome da Vaga' : str(nome_vaga(dom1, num_vaga)),
        'Nome da Empresa' : str(nome_empresa(site1)),
        'URL da Empresa' : str(url_empresa(site1)),
        'Modelo de Contratação' : str(modelo_contratacao(site1)),
        'Tipo de Contratação' : str(tipo_contratacao(dom1)),
        'Nível de Experiência' : str(nivel_experiencia(site1)),
        'Número de Candidaturas' : str(numero_vagas(site1)),
        'Data da Postagem da Vaga' : str(data_postagem(site1)),
        'Horário do Scraping' : str(horario()),
        'Número de Funcionários' : str(numero_funcionarios(dom2)),
        'Número de Seguidores' : str(numero_seguidores(dom2)),
        'Local Sede da Empresa' : str(local_empresa(dom1, num_vaga)),
        'URL da Candidatura' : str(url_candidatura(site1))
        }
    ]

    # Salva as Informações em um arquivo temporário
    with open('log_dados.txt', '+a') as p:
        for dado in dados:
            for key, item in dado.items():
                p.writelines(f"{key} : {item}\n")
            p.write('\n\n')

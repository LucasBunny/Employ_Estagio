import os
import platform
import datetime
from unidecode import unidecode


# --> Funções para Coleta de Informações / Formatação<--

# Limpa a Tela
def limpar_tela():
    sistema = platform.system()
    if sistema == 'Windows': 
        os.system('cls')
    os.system('clear')

# URL da Vaga
def url_vaga(site):
    return site.find("a", {"class":"topcard__link"}).get('href')

# Nome da Vaga
def nome_vaga(dom, range):
    try: 
        return dom.xpath(f'//*[@id="main-content"]/section[2]/ul/li[{range}]/div/div[2]/h3')[0].text.strip()
    except:
        return dom.xpath(f'//*[@id="main-content"]/section[2]/ul/li[{range}]/a/div[2]/h3')[0].text.strip()
    
# Nome da Empresa 
def nome_empresa(site):
    try:
        return site.find('a', {'class':'topcard__org-name-link'}).get_text(strip=True)
    except:
        return site.find('span', {'class':'topcard__flavor'}).get_text(strip=True)

# URL de Perfil da Empresa
def url_empresa(site):
    try:
        return site.find("a", {"class":"topcard__org-name-link"}).get('href')
    except:
        return None
    
# Modelo de Contratacao (hibrido, presencial ou remoto)
def modelo_contratacao(site):
    palavras = ['hibrido', 'presencial', 'remoto']
    descricao = site.find("div", {"class":"description__text"}).get_text(strip=True)
    descricao = unidecode(descricao.lower())
    for palavra in palavras:
        if descricao.find(palavra) != -1:
            return palavra
        return None

# Tipo de Contratação (tempo integral ou estágio)
def tipo_contratacao(dom): 
    tipo = dom.xpath('/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span')
    if tipo != []:
        return tipo[0].text.strip()
    return None

# Nível de Experiência
def nivel_experiencia(site):
    return site.find("span", {"class":"description__job-criteria-text"}).get_text(strip=True)

# Número de Vagas
def numero_vagas(site):
    content = site.find("span", {"class":"num-applicants__caption"}) 
    if content is None:
        return site.find("figure", {"class":"num-applicants__figure"}).get_text(strip=True)
    return content.get_text(strip=True)

# Tempo de Postagem da Vaga
def data_postagem(site):
    return site.find("span", {"class":"posted-time-ago__text"}).get_text(strip=True)

# Horário do Scraping
def horario():
    hora = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
    return hora

# Número de Funcionários
def numero_funcionarios(dom):
    if dom is None:
        return None
    
    funcionarios = dom.xpath('//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd')
    try:
        for i in funcionarios[0].text.strip():
            if not i.isdigit():
                return dom.xpath('//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[2]/dd')[0].text.strip()
            return funcionarios[0].text.strip()
    except IndexError:
        return None

# Número de Seguidores
def numero_seguidores(dom):
    if dom is None:
        return None

    h3_tag = dom.xpath('//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h3/text()[2]')
    try:
        return h3_tag[0].strip()
    except IndexError:
        return None

# Localização da Sede da Empresa
def local_empresa(dom, range):
    try:
        return dom.xpath(f'//*[@id="main-content"]/section[2]/ul/li[{range}]/div/div[2]/div/span')[0].text.strip()
    except:
        return dom.xpath(f'/html/body/div[1]/div/section/div[2]/section/div/div[2]/div/h4/div[1]/span[2]')[0].text.strip()
# URL da Candidatura
def url_candidatura(site):
    return str(site.find("code", {"id":"applyUrl"})).replace('<code id="applyUrl" style="display: none"><!--"', '').replace('--></code>', '')

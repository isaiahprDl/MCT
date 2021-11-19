# ----------------------------------------------------------------------------------------------------------------------
#
# (C) 2021 TIVIT BRASIL
# Isaías Pereira Machado
# São Paulo, Brasil
#
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT DE BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
import ctypes
from ctypes import wintypes
import time
import winreg as wreg
#import getpass
import datetime
import psutil
import configparser
import tempfile
import selenium
import hurry
import os
import shutil
import json
import requests
import subprocess, sys

from hurry.filesize import size
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# VARIÁVEIS GLOBAIS
# ----------------------------------------------------------------------------------------------------------------------
now = datetime.datetime.now()

config = configparser.ConfigParser()                            
config.read(tempfile.gettempdir() + '\MCT\Config.ini')          # ACESSA O ARQUIVO INI COM OS PARAMETROS PARA A EXECUÇÃO
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA COLETAR A PERDA DE PACOTES NO TESTE
# ----------------------------------------------------------------------------------------------------------------------
def PacketLoss(url):
    pkFile = tempfile.gettempdir() + '\MCT\PacketLoss.ini'
    if os.path.isfile(pkFile):
        os.remove(pkFile)

    os.system ('ping ' + url + ' -n 10 | findstr /r /i "%" > ' + pkFile)

    with open(pkFile) as f:
        lines = f.readlines()

    pkgloss = str(lines)
    start = pkgloss.index('(') + len('%')
    end = pkgloss.index('%')
    pkgloss[start:end]

    RegWrite("PacketLoss", pkgloss[start:end], r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO DE PING SIMPLES
# ----------------------------------------------------------------------------------------------------------------------
def IsCorpNetwork(ping):
    proc = subprocess.Popen(['ping ', ping], stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return str(proc.returncode)
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA LER O STATUS DO SERVIÇO DO WINDOWS
# ----------------------------------------------------------------------------------------------------------------------
def getService(name):
    service = None
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        print(str(ex))
    return service
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA GRAVAR NO REGISTRO DE USUARIO (HKEY_LOCAL_MACHINE)
# ----------------------------------------------------------------------------------------------------------------------
def RegWrite(valueName, value, path):
    key = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, path)
    wreg.SetValueEx(key, valueName, 0, wreg.REG_SZ, value)
    key.Close()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA LER O REGISTRO DE USUARIO (HKEY_CURRENT_USER)
# ----------------------------------------------------------------------------------------------------------------------
def RegRead_CU(param, path):
    registry_key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, path, 0, (wreg.KEY_READ))
    value = wreg.QueryValueEx(registry_key, param)[0]     
    return value
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA LER O REGISTRO DE MAQUINA (HKEY_LOCAL_MACHINE)
# ----------------------------------------------------------------------------------------------------------------------
def RegRead_LM(param, path):
    registry_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, path, 0, (wreg.KEY_READ))
    value = wreg.QueryValueEx(registry_key, param)[0]     
    return value
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# INICIO DE FUNÇÕES PARA COLETA DE DADOS USANDO O WEBDRIVER DO EDGE/CHROME
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> ALGAR TELECOM <<
# ----------------------------------------------------------------------------------------------------------------------
def Algar():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('http://algar.speedtestcustom.com/')
    
    wait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/button/span'))).click()

    time.sleep(60)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "ALGAR", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> ATPLUS <<
# ----------------------------------------------------------------------------------------------------------------------
def ATPlus():
    #EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://velocidade.atplus.com.br/')

    driver.find_element_by_id("startStopBtn").click()

    time.sleep(30)

    download = driver.find_element_by_id("dlText").text
    upload = driver.find_element_by_id("ulText").text
    jitter = driver.find_element_by_id("jitText").text
 
    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "ATPLUS", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> BRASIL BANDA LARGA <<
# ----------------------------------------------------------------------------------------------------------------------
def BBL():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://www.brasilbandalarga.com.br/bbl/')
    
    driver.find_element_by_id("btnIniciar").click()

    time.sleep(90)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[1]/div[1]/div[2]').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[1]/div[2]/div[2]').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[2]/div[2]').text).replace(' ms',''), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("PacketLoss", str(driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[3]/div[2]').text).replace(' %',''), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "BBL", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> WIIP <<
# ----------------------------------------------------------------------------------------------------------------------
def WIIP():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('http://velocidade.wiip.com.br/')

    driver.find_element_by_id("startStopBtn").click()

    time.sleep(60)

    download = driver.find_element_by_id("dlText").text
    upload = driver.find_element_by_id("ulText").text
    jitter = driver.find_element_by_id("jitText").text
 
    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "WIIP", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> UNIFIQUE <<
# ----------------------------------------------------------------------------------------------------------------------
def Unifique():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://speed.unifique.com.br/')

    driver.find_element_by_id("startStopBtn").click()

    time.sleep(60)

    download = driver.find_element_by_id("dlText").text
    upload = driver.find_element_by_id("ulText").text
    jitter = driver.find_element_by_id("jitText").text
 
    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "UNIFIQUE", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> TESTMETER <<
# ----------------------------------------------------------------------------------------------------------------------
def TestMeter():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://www.meter.net/br/')

    driver.find_element_by_id("retestbtn").click()

    time.sleep(60)

    download = driver.find_element_by_id("nres_value_down").text
    upload = driver.find_element_by_id("nres_value_up").text
    jitter = driver.find_element_by_id("nres_value_jitter").text
 
    RegWrite("Download", download.replace(',','.'), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload.replace(',','.'), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter.replace(',','.'), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "TEST METER", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> LOCAL NET <<
# ----------------------------------------------------------------------------------------------------------------------
def LocalNet():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')


    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://velocimetro.localnetpelotas.com.br/')
    
    driver.find_element_by_id("startStopBtn").click()

    time.sleep(60)

    download = driver.find_element_by_id("dlText").text
    upload = driver.find_element_by_id("ulText").text
    jitter = driver.find_element_by_id("jitText").text
    
    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "LOCALNET PELOTAS", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> FAST <<
# ----------------------------------------------------------------------------------------------------------------------
def Fast():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://fast.com/pt/#')
    
    time.sleep(30)

    download = driver.find_element_by_id("speed-value").text
    
    time.sleep(50)

    driver.find_element_by_id("show-more-details-link").click()
    
    upload = driver.find_element_by_id("upload-value").text
    jitter = driver.find_element_by_id("latency-value").text
    
    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "FAST", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> SUA CONEXÃO <<
# ----------------------------------------------------------------------------------------------------------------------
def SuaConexao():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://testesuaconexao.com.br/wp-content/plugins/wp-speedtest/speedtest/')
    
    driver.find_element_by_id('startStopBtn').click()

    time.sleep(60)

    download = driver.find_element_by_id("dlText").text
    upload = driver.find_element_by_id("ulText").text
    jitter = driver.find_element_by_id("jitText").text

    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "SUA CONEXÃO", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> COPEL BRASIL <<
# ----------------------------------------------------------------------------------------------------------------------
def CopelBrasil():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://testecopelbrasil.speedtestcustom.com/')
    
    wait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/button/span'))).click()

    time.sleep(60)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "COPEL BRASIL", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> WEBBY <<
# ----------------------------------------------------------------------------------------------------------------------
def Weeby():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://webby.speedtestcustom.com/')
    
    wait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/button/span'))).click()

    time.sleep(60)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "WEBBY", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> VIVO <<
# ----------------------------------------------------------------------------------------------------------------------
def Vivo():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('https://telefonica.speedtestcustom.com/')
    
    wait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/button/span'))).click()

    time.sleep(60)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "VIVO", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> SEJA AMIGO <<
# ----------------------------------------------------------------------------------------------------------------------
def SejaAmigo():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('http://sejaamigo.speedtestcustom.com/')
    
    wait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/button/span'))).click()

    time.sleep(60)

    RegWrite("Download", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/div/span').text), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "SEJA AMIGO", r'Software\TIVIT\MCT\Connectivity')
    
    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> OPEN SPEEDTEST <<
# ----------------------------------------------------------------------------------------------------------------------
def OpenSpeed():
    EDGEDRIVER_PATH=tempfile.gettempdir() + '\MCT\msedgedriver.exe'

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    # prefs = {"download.default_directory" : tempfile.gettempdir() + '\MCT'}
    # options.add_experimental_option("prefs",prefs);

    driver = webdriver.Chrome(executable_path=EDGEDRIVER_PATH, options=options)
    driver.get('http://openspeedtest.com/Get-widget.php?Auto=3')
    
    time.sleep(60)

    download = driver.find_element_by_id("downResult").text
    upload = driver.find_element_by_id("upRestxt").text
    jitter = driver.find_element_by_id("jitterDesk").text

    RegWrite("Download", download, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", upload, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", jitter, r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "OPEN SPEEDTEST", r'Software\TIVIT\MCT\Connectivity')

    driver.close()
    driver.quit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA OBTER DADOS DO PROVEDOR >> SPEEDTEST <<
# ----------------------------------------------------------------------------------------------------------------------
def SpeedTest():

    fileSpeed = tempfile.gettempdir() + '\MCT\speedtest.exe'
    exportTest = tempfile.gettempdir() + '\MCT\exportTest.json'

    os.system('cmd /c ' + fileSpeed + ' --accept-license --accept-gdpr --server-id=16322cl -f json-pretty > ' + exportTest)

    # LER ARQUIVO JSON EXTRAÍDO
    with open(exportTest, 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)

    # GET DOS VALORES DENTRO DO ARQUIVO JSON
    download = obj["download"]["bytes"]
    upload = obj["upload"]["bytes"]
    jitter = obj["ping"]["jitter"]
    ploss = obj["packetLoss"]

    RegWrite("Download", str(size(download).replace('M','')), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Upload", str(size(upload).replace('M','')), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Jitter", str("%.2f"% jitter), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("PacketLoss", str(round(ploss)), r'Software\TIVIT\MCT\Connectivity')
    RegWrite("Provider", "SPEEDTEST", r'Software\TIVIT\MCT\Connectivity')

    if os.path.isfile(exportTest):
            os.remove(exportTest)
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO DE VALIDAÇÃO DA VPN CHECKPOINT
# ----------------------------------------------------------------------------------------------------------------------
def VpnCheckpoint():

    VpnFile = tempfile.gettempdir() + '\MCT\VpnFile.ini'
    if os.path.isfile(VpnFile):
        os.remove(VpnFile)

    file = tempfile.gettempdir() + '\MCT\\trac.exe'
    
    os.system (file + ' info | findstr /r /i "status: Connected" > ' + VpnFile)

    with open(VpnFile) as f:
        if 'status: Connected' in f.read():
            RegWrite("VPN", "Sim", r'Software\TIVIT\MCT\Connectivity')
        else:
            RegWrite("VPN", "Não", r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO DE VALIDAÇÃO DA VPN CHECKPOINT SSL (PORTAL)
# ----------------------------------------------------------------------------------------------------------------------
def VpnCheckpointSSL():
    user32 = ctypes.windll.user32
    handle = user32.FindWindowW(None, 'SSL Network Extender - Internet Explorer')
    rect = wintypes.RECT()
    ff=ctypes.windll.user32.GetWindowRect(handle, ctypes.pointer(rect))
    count = rect.left+rect.top+rect.right+rect.bottom

    if count != 0:
        RegWrite("VPN", "Sim", r'Software\TIVIT\MCT\Connectivity')
    else:
        RegWrite("VPN", "Não", r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO DE VALIDAÇÃO DA CISCO VPN CLIENT
# ----------------------------------------------------------------------------------------------------------------------
def CiscoClient():

    VpnFile = tempfile.gettempdir() + '\MCT\VpnFile.ini'
    if os.path.isfile(VpnFile):
        os.remove(VpnFile)

    file = tempfile.gettempdir() + '\MCT\\vpncli.exe'
    
    os.system (file + ' stats | findstr /r /i ">> notice: Connected to" > ' + VpnFile)

    with open(VpnFile) as f:
        if '>> notice: Connected to ' in f.read():
            RegWrite("VPN", "Sim", r'Software\TIVIT\MCT\Connectivity')
        else:
            RegWrite("VPN", "Não", r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO DE VALIDAÇÃO DA CISCO VPN CLIENT
# ----------------------------------------------------------------------------------------------------------------------
def CiscoVpnSSL():

    VpnFile = tempfile.gettempdir() + '\MCT\VpnFile.ini'
    if os.path.isfile(VpnFile):
        os.remove(VpnFile)
    
    os.system ('cmd /c wmic path win32_process get commandline /format:list | findstr /r /i "rundll32.exe" > ' + VpnFile)

    with open(VpnFile) as f:
        if 'csvrelay' in f.read():
            RegWrite("VPN", "Sim", r'Software\TIVIT\MCT\Connectivity')
        else:
            RegWrite("VPN", "Não", r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO DE VALIDAÇÃO DA CISCO VPN CLIENT
# ----------------------------------------------------------------------------------------------------------------------
def Fortclient():

    file = tempfile.gettempdir() + '\MCT\\VpnForticlient.exe'
    
    os.system (file)

# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA ENVIAR AS INFORMAÇÕES POR POST (NATIVO)
# ----------------------------------------------------------------------------------------------------------------------
def PostNativeParam():
    os.startfile(tempfile.gettempdir() +  '\\MCT\\PostBBL.exe')
    # compname = "ComputerName=" + os.environ['COMPUTERNAME']
    # downname = "&Download=" + RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity')
    # uploname = "&Upload=" + RegRead_LM("Upload", r'Software\TIVIT\MCT\Connectivity')
    # packname = "&PacketLoss=" + RegRead_LM("PacketLoss", r'Software\TIVIT\MCT\Connectivity')
    # jittname = "&Jitter=" + RegRead_LM("Jitter", r'Software\TIVIT\MCT\Connectivity')
    # datename = "&dateRun=" + RegRead_LM("DateRun", r'Software\TIVIT\MCT\Connectivity')
    # provname = "&Provider=" + RegRead_LM("Provider", r'Software\TIVIT\MCT\Connectivity')
    # vpnaname = "&VPN=" + RegRead_LM("VPN", r'Software\TIVIT\MCT\Connectivity')
    # corpname = "&CorporateID=" + RegRead_LM("CorporateID", r'Software\TIVIT\MCT\User')
    # username = "&UserName=" + RegRead_LM("UserName", r'Software\TIVIT\MCT\User')
    # versname = "&Versao=" + RegRead_LM("Version", r'Software\TIVIT\MCT\Release')
    # logrname = "&Log=" + RegRead_LM("Log", r'Software\TIVIT\MCT\Release')
    # bootname = "&bootTime=" + RegRead_LM("bootTime", r'Software\TIVIT\MCT\Hardware')
    # diskname = "&diskSpace=" + RegRead_LM("DiskSize", r'Software\TIVIT\MCT\Hardware')
    # freename = "&FreeSpace=" + RegRead_LM("FreeSpace", r'Software\TIVIT\MCT\Hardware')
    # stsename = "&statusEndpoint=" + RegRead_LM("Endpoint", r'Software\TIVIT\MCT\Clients')
    # stsaname = "&statusAV=" + RegRead_LM("Antivirus", r'Software\TIVIT\MCT\Clients')

    # url = "https://tamcmdb.tivit.com/mctwps/MCTAPI/new?" + compname + downname + uploname + packname + jittname + datename + provname + vpnaname + corpname + username + versname + logrname + logrname + bootname + diskname + freename + stsename + stsaname

    # payload={}
    # headers = {}

    # response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.status_code)
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA ENVIAR AS INFORMAÇÕES POR POST (POWERSHELL)
# ----------------------------------------------------------------------------------------------------------------------
def PostPsParam():
    postFile = tempfile.gettempdir() + '\\MCT\\PostParam.ps1'

    p = subprocess.Popen('powershell.exe -ExecutionPolicy ByPass -file ' + postFile, stdout=sys.stdout)
    p.communicate()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA VALIDAR O TEMPO DE PERFORMANCE DO BOOT DO EQUIPAMENTO
# ----------------------------------------------------------------------------------------------------------------------
os.system("C:\Windows\System32\cscript.exe //b " + tempfile.gettempdir() +  '\\MCT\\GetPerformBoot.vbs')
time.sleep(5)
getPerformBoot = RegRead_LM("PerformBootTime", r'Software\TIVIT\MCT\Hardware')

start = getPerformBoot.index('')
end = getPerformBoot.index(',')

intValue = int(getPerformBoot[start:end])
getValue = str(datetime.timedelta(seconds=intValue))

RegWrite("PerformBootTime", getValue, r'Software\TIVIT\MCT\Hardware')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# DELETA CHAVE PARA NOVO TESTE
# ----------------------------------------------------------------------------------------------------------------------
#os.popen("REG DELETE HKEY_LOCALMACHINE\SOFTWARE\TIVIT /f")      # DELETA A CHAVE TIVIT DO REGISTRO
time.sleep(5)
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA AS INFORMAÇÕES REFERENTE AO STATUS DE VPN
# ----------------------------------------------------------------------------------------------------------------------
vpn = config.get("VPN","VPN")
checkpoint_client = config.get("VPN", "CHECKPOINT")
checkpoint_ssl = config.get("VPN", "SSL_CHECKPOINT")
forticlient = config.get("VPN", "FORTICLIENT")
cisco_client = config.get("VPN", "CISCO")
cisco_portal = config.get("VPN", "PORTAL_CISCO")

if vpn == "true":
    if checkpoint_client == "true":
        VpnCheckpoint()

    if checkpoint_ssl == "true":
        VpnCheckpointSSL()

    if forticlient == "true":
        Fortclient()

    if cisco_client == "true":
        CiscoClient()

    if cisco_portal == "true":
        CiscoVpnSSL()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO PARA VALIDAR SE ESTÁ DENTRO DO AMBIENTE
# ----------------------------------------------------------------------------------------------------------------------
internalserver = config.get("INTERNAL_SERVERS","INTERNAL_SERVERS")
server1 = config.get("INTERNAL_SERVERS","SERVER1")
server2 = config.get("INTERNAL_SERVERS","SERVER2")
server3 = config.get("INTERNAL_SERVERS","SERVER3")
stsVpn = RegRead_LM("VPN", r'Software\TIVIT\MCT\Connectivity')

if internalserver == "true":
    if IsCorpNetwork(server1) == "0" or IsCorpNetwork(server2) == "0" or IsCorpNetwork(server3) == "0" and stsVpn == "Não":
        RegWrite("InternalEnvironment", "Sim", r'Software\TIVIT\MCT\Connectivity')
        sys.exit()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTA A FUNÇÃO PARA A MONITORAÇÃO DE REDE
# ----------------------------------------------------------------------------------------------------------------------
RegWrite("Download", "0", r'Software\TIVIT\MCT\Connectivity')   # ZERA A CHAVE PARA INICIAR UMA NOVA LEITURA

providers = config.get("PROVIDERS","PROVIDERS")
algar = config.get("PROVIDERS","ALGAR")
atplus = config.get("PROVIDERS","ATPLUS")
bbl = config.get("PROVIDERS","BBL")
copel = config.get("PROVIDERS","COPELBRASIL")
fast = config.get("PROVIDERS","FAST")
localNet = config.get("PROVIDERS","LOCALNET")
openSpeed = config.get("PROVIDERS","OPENSPEEDTEST")
sejaamigo = config.get("PROVIDERS","SEJAAMIGO")
speedTest = config.get("PROVIDERS","SPEEDTEST")
suaconexao = config.get("PROVIDERS","SUACONEXAO")
testMeter = config.get("PROVIDERS","TESTMETER")
unifique = config.get("PROVIDERS","UNIFIQUE")
vivo = config.get("PROVIDERS","VIVO")
webby = config.get("PROVIDERS","WEBBY")
wiip = config.get("PROVIDERS","WIIP")

if providers == "true":
    if algar == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            Algar()
            PacketLoss('algar.speedtestcustom.com')

    if atplus == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            ATPlus()
            PacketLoss('velocidade.atplus.com.br')
    
    if bbl == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            BBL()
    
    if copel == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            CopelBrasil()
            PacketLoss('testecopelbrasil.speedtestcustom.com')

    if fast == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            Fast()
            PacketLoss('fast.com')
    
    if localNet == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            LocalNet()
            PacketLoss('velocimetro.localnetpelotas.com.br')

    if openSpeed == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            OpenSpeed()
            PacketLoss('openspeedtest.com')

    if sejaamigo == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            SejaAmigo()
            PacketLoss('sejaamigo.speedtestcustom.com')

    if speedTest == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            SpeedTest()

    if suaconexao == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            SuaConexao()
            PacketLoss('testesuaconexao.com.br')
    
    if testMeter == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            TestMeter()
            PacketLoss('www.meter.net')
    
    if unifique == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            Unifique()
            PacketLoss('speed.unifique.com.br')

    if vivo == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            Vivo()
            PacketLoss('telefonica.speedtestcustom.com')

    if webby == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            Weeby()
            PacketLoss('webby.speedtestcustom.com')

    if wiip == "true":
        if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
            WIIP()
            PacketLoss('velocidade.wiip.com.br')

    if RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "0" or RegRead_LM("Download", r'Software\TIVIT\MCT\Connectivity') == "":
        RegWrite("Download", "N/A", r'Software\TIVIT\MCT\Connectivity')
        RegWrite("Upload", "N/A", r'Software\TIVIT\MCT\Connectivity')
        RegWrite("Jitter", "N/A", r'Software\TIVIT\MCT\Connectivity')
        RegWrite("PacketLoss", "N/A", r'Software\TIVIT\MCT\Connectivity')
        RegWrite("Provider", "N/A", r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA A INFORMAÇÃO DO NOME DO USUARIO LOGADO E LOGIN
# ----------------------------------------------------------------------------------------------------------------------
try:
    RegWrite("UserName", RegRead_LM("LastLoggedOnDisplayName", r'SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI'), r'Software\TIVIT\MCT\User')
except:
    RegWrite("UserName", "N/A", r'Software\TIVIT\MCT\User')

RegWrite("CorporateID", os.getlogin(), r'Software\TIVIT\MCT\User')

# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA A INFORMAÇÃO DE DATA DE EXECUÇÃO
# ----------------------------------------------------------------------------------------------------------------------
RegWrite("DateRun", now.strftime("%d/%m/%Y %H:%M"), r'Software\TIVIT\MCT\Connectivity')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# VERSIONAMENTO DA APLICAÇÃO
# ----------------------------------------------------------------------------------------------------------------------
RegWrite("Version", "2.0.092021", r'Software\TIVIT\MCT\Release')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA AS INFORMAÇÕES DO ULTIMO BOOT
# ----------------------------------------------------------------------------------------------------------------------
last_reboot = psutil.boot_time()
bootTime = datetime.datetime.fromtimestamp(last_reboot)
RegWrite("bootTime", bootTime.strftime("%d/%m/%Y"), r'Software\TIVIT\MCT\Hardware')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA AS INFORMAÇÕES REFERENTE AO DISCO
# ----------------------------------------------------------------------------------------------------------------------
obj_Disk = psutil.disk_usage('/')
RegWrite("DiskSize","%d" % (obj_Disk.total / (1024.0 ** 3)), r'Software\TIVIT\MCT\Hardware')
RegWrite("FreeSpace","%d" % (obj_Disk.free / (1024.0 ** 3)), r'Software\TIVIT\MCT\Hardware')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# GRAVA AS INFORMAÇÕES REFERENTE AOS SERVIÇOS IMPORTANTES
# ----------------------------------------------------------------------------------------------------------------------
tools = config.get("TOOLS","TOOLS")
altiris = config.get("TOOLS","ALTIRIS")
cm = config.get("TOOLS","CM")
crowdstrike = config.get("TOOLS","CROWDSTRIKE")
ivanti = config.get("TOOLS","IVANTI")
sep = config.get("TOOLS","SEP")
trend_apex = config.get("TOOLS","TREND_APEX")

if tools == "true":
    if altiris == "true":
        service = getService('AeXNSClient')
        if service and service['status'] == 'running':
            RegWrite("Endpoint","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Endpoint","Stopped", r'Software\TIVIT\MCT\Clients')

    if cm == "true":
        service = getService('ccmexec')
        if service and service['status'] == 'running':
            RegWrite("Endpoint","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Endpoint","Stopped", r'Software\TIVIT\MCT\Clients')

    if crowdstrike == "true":
        service = getService('CSFalconService')
        if service and service['status'] == 'running':
            RegWrite("Antivirus","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Antivirus","Stopped", r'Software\TIVIT\MCT\Clients')
        
    if ivanti == "true":
        service = getService('ivanti')
        if service and service['status'] == 'running':
            RegWrite("Endpoint","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Endpoint","Stopped", r'Software\TIVIT\MCT\Clients')

    if sep == "true":
        service = getService('SepMasterService')
        if service and service['status'] == 'running':
            RegWrite("Antivirus","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Antivirus","Stopped", r'Software\TIVIT\MCT\Clients')

    if sep == "true":
        service = getService('DHCPfwe')
        if service and service['status'] == 'running':
            RegWrite("Antivirus","Running", r'Software\TIVIT\MCT\Clients')
        else:
            RegWrite("Antivirus","Stopped", r'Software\TIVIT\MCT\Clients')
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# CHAMA O POST NA PAGINA DO MCT
# ----------------------------------------------------------------------------------------------------------------------
webservices = config.get("WEBSERVICES","WEBSERVICES")
native = config.get("WEBSERVICES","NATIVE")
ps = config.get("WEBSERVICES","PS")

if webservices == "true":
    if native == "true":
        PostNativeParam()

    if ps == "true":
        PostPsParam()
# ----------------------------------------------------------------------------------------------------------------------
# END
# ----------------------------------------------------------------------------------------------------------------------
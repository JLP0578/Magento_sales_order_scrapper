# External
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import mysql.connector
import pprint
import time
import csv
import sys
import os

# doenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

# Internal
import function

def dd(*args):
    for arg in args:
        pprint.pprint(arg)
        print("-" * 40)
    sys.exit()

def shutdown_computer():
    if os.name == 'nt':
        # For Windows operating system
        os.system('shutdown /s /t 0')
    elif os.name == 'posix':
        # For Unix/Linux/Mac operating systems
        os.system('sudo shutdown now')
    else:
        print('Unsupported operating system.')

def split_commandes(commandes, nb_split):
    # N'EST PAS UTILISE
    taille_tableau = len(commandes)
    taille_sous_tableau = (taille_tableau + nb_split - 1) // nb_split  # Division arrondie supérieure

    sous_tableaux = []
    indice_debut = 0

    for i in range(nb_split):
        indice_fin = min(indice_debut + taille_sous_tableau, taille_tableau)
        sous_tableaux.append(commandes[indice_debut:indice_fin])
        indice_debut = indice_fin

    return sous_tableaux

def recuperer_donnees_bdd_distante(env, requete_sql):
    try:
        if env == "prod":
            connexion = mysql.connector.connect(
                host=os.environ.get("PROD_HOST"),
                user=os.environ.get("PROD_USER"),
                password=os.environ.get("PROD_PASSWORD"),
                database=os.environ.get("PROD_DATABASES"),
            )
        if env == "dev":
            connexion = mysql.connector.connect(
                host=os.environ.get("DEV_HOST"),
                user=os.environ.get("DEV_USER"),
                password=os.environ.get("DEV_PASSWORD"),
                database=os.environ.get("DEV_DATABASES"),
            )
        if env == "local":
            connexion = mysql.connector.connect(
                host=os.environ.get("LOCAL_HOST"),
                user=os.environ.get("LOCAL_USER"),
                password=os.environ.get("LOCAL_PASSWORD"),
                database=os.environ.get("LOCAL_DATABASES"),
            )

        curseur = connexion.cursor()
        print("[DATABASE] Connexion à la base de données ouverte en " + env)
        curseur.execute(requete_sql)
        print("[DATABASE] Requête executée.")
        resultats = curseur.fetchall()

        return resultats

    except mysql.connector.Error as erreur:
        print("[DATABASE] Erreur lors de la récupération des données:", erreur)

    finally:
        if "connexion" in locals() and connexion.is_connected():
            curseur.close()
            connexion.close()
            print("[DATABASE] Connexion à la base de données fermée.")

def get_directory_log(env):
    return "./logs/"+env

def get_log_extention():
    return ".csv"

def get_log_name(store):
    return "log_" + str(store[0]) + "_" + str(store[1]) + get_log_extention()

def get_directory_output(env):
    return "./output/"+env

def get_file_output(store):
    return "Resultat_KPUT_" + str(store[0]) + "_" + str(store[1])+ get_log_extention()

def is_log_for_store(env, store):
    directoryLog = get_directory_log(env)
    nameLog = get_log_name(store)

    if os.path.exists('./logs') is not True:
        os.mkdir('./logs')

    if os.path.exists(directoryLog) is not True:
        os.mkdir('./logs/'+env)

    if os.path.exists(directoryLog + "/" + nameLog):
        # Load file
        result = read_file(directoryLog + "/" + nameLog)
    else:
        # create file
        header = ['entity_id']
        create_file(directoryLog + "/" + nameLog)
        append_file(directoryLog + "/" + nameLog, header)
        result = ""

    return result

def is_output_for_store(env, store):
    directoryOutput = get_directory_output(env)
    nameOutput = get_file_output(store)

    if os.path.exists('./output') is not True:
        os.mkdir('./output')

    if os.path.exists(directoryOutput) is not True:
        os.mkdir('./output/'+env)

    if os.path.exists(directoryOutput + "/" + nameOutput):
        # Load file
        result = read_file(directoryOutput + "/" + nameOutput)
    else:
        # create file
        header = ['entity_id', 'error_type']
        create_file(directoryOutput + "/" + nameOutput)
        append_file(directoryOutput + "/" + nameOutput, header)
        result = ""

    return result

def read_file(file_name):
    result = []
    with open(file_name, "r", newline="") as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv)
        for ligne in lecteur_csv:
            result.append(ligne)

    return result

def append_file(file_name, data_array):
    with open(file_name, "a", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(data_array)

def create_file(file_name):
    open(file_name, "w").close()

def worker(env, store, commandes):
    os.environ.get("")
    if env == 'prod':
        domain = os.environ.get("PROD_DOMAIN")
        username_login = os.environ.get("PROD_USERNAME_LOGIN")
        password_login = os.environ.get("PROD_PASSWORD_LOGIN")
    if env == "dev":
        domain = os.environ.get("DEV_DOMAIN")
        username_login = os.environ.get("DEV_USERNAME_LOGIN")
        password_login = os.environ.get("DEV_PASSWORD_LOGIN")
    if env == 'local':
        domain = os.environ.get("LOCAL_DOMAIN")
        username_login = os.environ.get("LOCAL_USERNAME_LOGIN")
        password_login = os.environ.get("LOCAL_PASSWORD_LOGIN")
        
    try:
        num = str(store[0])
        name = str(store[1])
        print(f"Process {num}_{name} : Wake Up")

        # Chrome
        options = ChromeOptions()

        # Firefox
        # options = FirefoxOptions()

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        # options.add_argument("--headless")

        # Chrome
        driver = webdriver.Chrome(options=options)

        # Firefox
        # driver = webdriver.Firefox(options=options)
        
        driver.get(domain)

        if env == 'local':
            # valid ssl
            time.sleep(1)

        # Connect
        username = driver.find_element(By.ID,"username")
        username.clear()
        username.send_keys(username_login)

        password = driver.find_element(By.ID,"login")
        password.clear()
        password.send_keys(password_login)

        password.send_keys(Keys.ENTER)

        print(f"Process {num}_{name} : Connected")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "html-body"))
        )

        commande_menu = driver.find_element(By.CSS_SELECTOR, "ul#nav li:nth-child(2) div.submenu li[data-ui-id=\"menu-magento-sales-sales-order\"] a")
        href = commande_menu.get_attribute("href")
        driver.get(href)

        spinner = driver.find_element(By.CSS_SELECTOR, "div.admin__data-grid-loading-mask[data-role='spinner']")

        while True:
            display_style = spinner.value_of_css_property('display')
            if display_style == 'none':
                print(f"Process {num}_{name} : End Loading")
                break

            time.sleep(1)

        print(f"Process {num}_{name} : On Sales")

        # Parcourir chaque élément du tableau
        for commande in commandes:
            time.sleep(1)
            sales_order_id = commande[0]
            type_error = None

            try:
                driver.get(domain+'/sales/order/view/order_id/'+str(sales_order_id))

                is_header = True
                is_pre = True

                try:
                    driver.find_element(By.CSS_SELECTOR, "header.page-header.row h1.page-title")
                except NoSuchElementException:
                    is_header = False

                try:
                    driver.find_element(By.CSS_SELECTOR, "main.page-main div.trace-container pre")
                except NoSuchElementException:
                    is_pre = False

                try:
                    pre = driver.find_element(By.CSS_SELECTOR, "body pre")
                    if 'Unable to unserialize value.' in pre.text:
                        is_pre = True
                except NoSuchElementException:
                    is_pre = False

            except NoSuchElementException as e:
                dd(e)

            finally:
                if is_header is True:
                    print(f"Process {num}_{name} : "+str(sales_order_id)+' should be OK')
                else:
                    print(f"Process {num}_{name} : "+str(sales_order_id)+' should be KPUT')
                    if is_pre is True:
                        type_error = 'Unable to unserialize value. Error: Control character error, possibly incorrectly encoded'
                    else:
                        type_error = 'Product SKU not found'
                        is_output_for_store(env, store)
                        append_file(get_directory_output(env)+"/"+ get_file_output(store), [sales_order_id, type_error])

                function.update_log_by_store(env, store, commande)

        driver.quit()
    except Exception as e:
        print(f"Process {num}_{name} : Une erreur - {e}")
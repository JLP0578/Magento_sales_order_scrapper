import outils

from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_store_to_parse(env):
    requete = (
        "SELECT store_id, code, name, website_id"
        + " FROM store"
        + " WHERE store_id NOT IN ("+os.environ.get("EXCLUDE_STORE")+")"
    )
    
    datas = outils.recuperer_donnees_bdd_distante(env, requete)

    return datas

def get_last_element_treat(env, store):
    log_datas = outils.is_log_for_store(env, store)
    if log_datas == "":
        pack_1000 = 0
    else:
        directoryLog = outils.get_directory_log(env)
        nameLog = outils.get_log_name(store)
        datas = outils.read_file(directoryLog + "/" + nameLog)
        if isinstance(datas, list) and len(datas) == 1 and datas[0][0] == 'entity_id':
            pack_1000 = 0
        else:
            pack_1000 = log_datas[len(log_datas)-1][0]

    return pack_1000

def get_1000_commandes_by_store(env, offset, store):
    store_id = store[0]
    requete = (
        "SELECT entity_id"
        + " FROM sales_order"
        + " WHERE store_id = "
        + str(store_id)
        + " AND entity_id > "
        + str(offset)
        + " ORDER BY entity_id"
        + " LIMIT 5000;"
    )
    datas = outils.recuperer_donnees_bdd_distante(env, requete)

    return datas

def update_log_by_store(env, store, commande):
    directoryLog = outils.get_directory_log(env)
    nameLog = outils.get_log_name(store)

    outils.append_file(directoryLog + "/" + nameLog, [commande[0]])

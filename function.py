# External
from os.path import join, dirname
from dotenv import load_dotenv
import os

# doenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), ".env"))

# Internal
import outils

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def get_store_to_parse(env, store_selected):
    if store_selected == "0":
        query = (
            "SELECT store_id, store.code, store.name, store.website_id, store_website.name as domaine"
            + " FROM store"
            + " INNER JOIN store_website on store.website_id = store_website.website_id"
            + " WHERE store_id NOT IN ("
            + os.environ.get("EXCLUDE_STORE")
            + ")"
        )
        data = ()
    else:
        query = (
            "SELECT store_id, store.code, store.name, store.website_id, store_website.name as domaine"
            + " FROM store"
            + " INNER JOIN store_website on store.website_id = store_website.website_id"
            + " WHERE store_id NOT IN ("
            + os.environ.get("EXCLUDE_STORE")
            + ") AND store_id IN ("
            + store_selected
            + ")"
        )
        data = ()

    datas = outils.recuperer_donnees_bdd_distante(env, query, data)

    return datas


def get_treated_elements(env, store):
    log_datas = outils.is_log_for_store(env, store)
    if log_datas == "":
        pack_1000 = []
    else:
        directoryLog = outils.get_directory_log(env)
        nameLog = outils.get_log_name(store)
        datas = outils.read_file(directoryLog + "/" + nameLog)
        if isinstance(datas, list) and len(datas) == 1 and datas[0][0] == "entity_id":
            pack_1000 = []
        else:
            # Récupérer tous les éléments de la colonne 'entity_id'
            pack_1000 = [row[0] for row in datas]

    return pack_1000


def update_log_by_store(env, store, commande):
    directoryLog = outils.get_directory_log(env)
    nameLog = outils.get_log_name(store)

    outils.append_file(directoryLog + "/" + nameLog, [commande[0]])


def split_array_equally(arr, nb_part):
    # Calculer la taille de chaque partie
    part_size = len(arr) // nb_part
    remainder = len(arr) % nb_part  # Nombre d'éléments restants

    # Initialiser une liste pour stocker les parties
    parts = []

    # Diviser le tableau en parties
    start_index = 0
    for i in range(nb_part):
        # Calculer la taille de la partie en fonction de la division équitable
        size = part_size + (1 if i < remainder else 0)
        # Ajouter la partie au tableau
        parts.append(arr[start_index : start_index + size])
        start_index += size

    return parts


def get_commande_from_store(env, store_selected, treated):
    if len(treated) == 0:
        query = (
            "SELECT entity_id"
            + " FROM sales_order so"
            + " WHERE so.store_id IN ("
            + str(store_selected[0])
            + ")"
            + " AND so.store_id NOT IN ("
            + os.environ.get("EXCLUDE_STORE")
            + ")"
            + " ORDER BY so.entity_id"
        )
        data = ()
    else:
        query = (
            "SELECT entity_id"
            + " FROM sales_order so"
            + " WHERE so.store_id IN ("
            + str(store_selected[0])
            + ")"
            + " AND so.store_id NOT IN ("
            + os.environ.get("EXCLUDE_STORE")
            + ")"
            + " AND so.entity_id NOT IN ("
            + ", ".join(treated)
            + ")"
            + " ORDER BY so.entity_id"
        )
        data = ()

    datas = outils.recuperer_donnees_bdd_distante(env, query, data)

    return datas

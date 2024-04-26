#  External
from datetime import datetime
import multiprocessing

# doenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

# Internal
import outils
import function

if __name__ == "__main__":
    start = datetime.now()
    env = input("Quel est l'envvironnement a utiliser ? prod, dev(defaut), local : ")
    if not env:
        env = "dev"
    shutdown = input("Eteindre le PC a la fin du script ? oui, non(defaut) : ")
    if not shutdown:
        shutdown = "non"

    stores = function.get_store_to_parse(env)
    multiprocessingMonitor = multiprocessing.Queue()
    processus = []
    for store in stores:
        print(store[2].upper())
        last_treat = function.get_last_element_treat(env, store)
        commandes = function.get_1000_commandes_by_store(env, last_treat, store)
        #  start multi process
        processes = []
        try:
            directoryLog = outils.get_directory_log(env)
            nameLog = outils.get_log_name(store)
            datas = outils.read_file(directoryLog + "/" + nameLog)
            if datas is not None:
                if len(commandes) > 0:
                    p = multiprocessing.Process(target=outils.worker, args=(env, store, commandes))
                    processes.append(p)
                    p.start()
                else:
                    print("[INFO] Pas de nouvelle commande à traiter")
                
            print("[INFO] Tous les processus ont terminé.")

        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

        finally:
            for p in processus:
                p.join()

            end = datetime.now()
            print('[TEMPS] Time spent', end - start)

            if shutdown == 'oui':
                outils.shutdown_computer()
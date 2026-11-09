from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_all_biblioteche(self):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Errore di connessione al database")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT id, nome, indirizzo FROM biblioteca"""

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(Biblioteca(id=row["id"],
                                         nome=row["nome"],
                                         indirizzo=row["indirizzo"]))
            cursor.close()
            cnx.close()
            return result
        except Exception as e:
            print(f"Errore nella query delle biblioteche: {e}")
            cursor.close()
            cnx.close()
            return result

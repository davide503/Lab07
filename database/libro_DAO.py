from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_libri_filtrati(self, id_biblioteca, genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result

        cursor = cnx.cursor(dictionary=True)

        # Usiamo COALESCE per gestire i filtri opzionali se passati come None
        query = """
            SELECT id, titolo, autore, genere, anno_pubblicazione, id_biblioteca
            FROM libro
            WHERE (id_biblioteca = COALESCE(%s, id_biblioteca))
              AND (genere = COALESCE(%s, genere))
        """

        try:
            cursor.execute(query, (id_biblioteca, genere))
            for row in cursor:
                result.append(Libro(
                    id=row["id"],
                    titolo=row["titolo"],
                    autore=row["autore"],
                    genere=row["genere"],
                    anno_pubblicazione=row["anno_pubblicazione"],
                    id_biblioteca=row["id_biblioteca"]
                ))
            cursor.close()
            cnx.close()
            return result
        except Exception as e:
            print(f"Errore nella query dei libri: {e}")
            cursor.close()
            cnx.close()
            return result

    def get_all_generi(self):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT genere FROM libro WHERE genere IS NOT NULL ORDER BY genere"""

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row["genere"])
            cursor.close()
            cnx.close()
            return result
        except Exception as e:
            print(f"Errore nella query dei generi: {e}")
            cursor.close()
            cnx.close()
            return result

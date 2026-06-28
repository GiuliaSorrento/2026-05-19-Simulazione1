from database.DB_connect import DBConnect
from model.Artist import Artist
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct g.*
                        from genre g"""
            cursor.execute(query)

            for row in cursor:
                result.append(Genre(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(genreId):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct a.*
                        from artist a , album al, track t 
                        where a.ArtistId = al.ArtistId  and al.AlbumId = t.AlbumId 
                        and t.GenreId = %s """
            cursor.execute(query, (genreId,))

            for row in cursor:
                result.append(Artist(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def cliente_artista_numbrani(genere_id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)  # FACCIO UNA QUERY CHE NON MI CALCOLA NE GLI ARCHI NE IL PESO DI ESSI
        # MI CALCOLA UNA LISTA IN CUI METTO TUPLE CON CLIENTE, ARTISTA, NUMEROTRACCIEVENDUTE DA QUELL'ARTISTA A QUEL CLIENTE
        # ARCHI E PESO VERRANNO GESTITI NEL MDOEL
        query = """select i.CustomerId, art.ArtistId, count(*) as ntracks
                    from invoice i, invoiceline i2, track t, genre g, artist art,album a
                    where i.InvoiceId  = i2.InvoiceId 
                    and t.TrackId = i2.TrackId 
                    and t.AlbumId = a.AlbumId
                    and g.GenreId = t.GenreId
                    and art.ArtistId = a.ArtistId 
                    and g.GenreId = %s
                    group by i.CustomerId, art.ArtistId"""
        cursor.execute(query, (genere_id,))

        for row in cursor:
            results.append((row["CustomerId"], row["ArtistId"], row["ntracks"]))

        cursor.close()
        conn.close()
        return results



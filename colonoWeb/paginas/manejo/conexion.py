import psycopg2


class BDConexion:
    def __init__(self, dbname, user, password):
        self.conn = None
        try:
            self.conn = psycopg2.connect ("dbname=\'" + dbname + "\' user='" + user + "\' password=\'" + password + "\'" )
        except:
            self.conn = None

    def desconectar(self):
        self.conn.close ( )

    def reinicioBDs(self):
        cur = self.conn.cursor ( )
        cur.execute ( "TRUNCATE TABLE paginas_tc_patron RESTART IDENTITY" )
        self.conn.commit ( )

    def filtrarPatrones(self, limite):
        cur = self.conn.cursor ( )
        cur.execute ( "select filtrarPatrones(" + str ( limite ) + ")" )
        self.conn.commit ( )

    def filtrarRuido(self, limite):
        cur = self.conn.cursor ( )
        cur.execute ( "select filtrarRuido(" + str ( limite ) + ")" )
        self.conn.commit ( )

    def insercionPatronesSecundario(self, id):
        try:
            cur = self.conn.cursor ( )
            cur.execute ( "select patroncombinado(" + str ( id ) + ")" )
            self.conn.commit ( )
        except psycopg2.DatabaseError, e:
            print e
            if self.conn:
                self.conn.rollback ( )

    def insercionPatronSimpre(self, lista):
        try:
            for indice in lista:
                cur = self.conn.cursor ( )
                cur.execute (
                    "insert into paginas_tc_patron(xp,yp,contadorp) values (" + str ( indice[0] ) + "," + str (
                        indice[1] ) + "," + str ( indice[2] ) + ") " )
                self.conn.commit ( )
        except psycopg2.DatabaseError, e:
            print e
            if self.conn:
                self.conn.rollback ( )

    def cantidadPatrones(self):
        try:
            cur = self.conn.cursor ( )
            cur.execute ( "select count(idpatron) from paginas_tc_patron" )
            while True:

                row = cur.fetchone ( )

                if row == None:
                    break

                return row[0]
        except psycopg2.DatabaseError, e:
            print e
        return 0

    def listaCoordenadas(self):
        lista = []
        try:
            cur = self.conn.cursor ( )
            cur.execute ( "select xp,yp from paginas_tc_patron" )

            while True:

                row = cur.fetchone ( )

                if row == None:
                    break

                lista.append ( [row[0], row[1]] )


        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
        return lista

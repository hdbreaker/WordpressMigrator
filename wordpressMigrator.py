import MySQLdb #apt-get install python-mysqldb
import time
from colorama import init, Fore
init()
class Migrator():

    def __init__(self):
        self.host=""
        self.user=""
        self.passwd=""
        self.prefix="aaa"
        self.dbName=""
        self.sqlFile=""
        self.oldDomain=""
        self.newDomain=""
        self.db = ""
        self.cursor=""
        self.start()

    def start(self):
        print "[*][*][*] WordpressMigrator by Alejandro Parodi [*][*][*]\n"
        self.host=raw_input("Ingrese Host de Mysql:  ")
        self.user=raw_input("Ingrese Usuario Mysql: ")
        self.passwd=raw_input("Ingrese Password Mysql: ")
        self.prefix=raw_input("Ingrese Wordpress prefix: ")
        self.dbName=raw_input("Ingrese nombre de la nueva db: ")
        self.sqlFile=raw_input("Ingrese path del archivo sql a importar: ")
        self.oldDomain=raw_input("Ingrese el viejo domino: ")
        self.newDomain=raw_input("Ingrese nuevo dominio: ")

        self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd)

        self.createDB()

    def createDB(self):
        self.cursor = self.db.cursor()
        #sql = 'DROP DATABASE ' + self.dbName
        #self.cursor.execute(sql)
        sql = 'CREATE DATABASE ' + self.dbName
        self.cursor.execute(sql)
        self.cursor.execute("USE "+self.dbName)
        time.sleep(1)
        self.importDB()

    def importDB(self):
        f = file(self.sqlFile,'r')
        self.cursor.execute(f.read())
        time.sleep(1)
        self.replaceDomains()

    def replaceDomains(self):
        #http://guardianes.noviggo.com.ar
        #http://localhost/guardianes2
        self.cursor.close()
        self.db.close()
        self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd)
        self.cursor = self.db.cursor()
        self.cursor.execute("USE "+self.dbName)


        queryArray=[
            "UPDATE "+self.prefix+"options SET option_value = REPLACE(option_value,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"_options SET option_value = REPLACE(option_value,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"posts SET post_content = REPLACE(post_content,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"posts SET guid = REPLACE(guid,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"_posts SET guid = REPLACE(guid,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"_posts SET post_content = REPLACE(post_content,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"postmeta SET meta_value = REPLACE(meta_value,'"+self.oldDomain+"','"+self.newDomain+"')",
            "UPDATE "+self.prefix+"_postmeta SET meta_value = REPLACE(meta_value,'"+self.oldDomain+"','"+self.newDomain+"')"
        ]

        try:
            for query in queryArray:
               self.cursor.execute(query)
               self.db.commit()
        except:
            print "No existe una tabla, se continuara con las demas"



        self.cursor.close()
        self.db.close()
        self.end()

    def end(self):
        print "Migracion completada con exito\n"
        print Fore.RED +""" !!!! NO OLVIDE MODIFICAR SU .HTACCESS !!!!

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /"""+Fore.GREEN + "[***PROYECT PATH***]"+Fore.RED+"""/
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /"""+Fore.GREEN + "[***PROYECT PATH***]"+Fore.RED+"""/index.php [L]
</IfModule>

        """

migrator = Migrator()

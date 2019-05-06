from google.appengine.ext import ndb
class Gimnasio(ndb.Model):
 actividades = ndb.StringProperty()
 dia = ndb.StringProperty()
 numInscritos = ndb.IntegerProperty()
 usuarios = ndb.StringProperty(repeated = True)
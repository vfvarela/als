from google.appengine.ext import ndb
class Usuario(ndb.Model):
 email = ndb.StringProperty(required=True)
 name = ndb.StringProperty()

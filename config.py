import os
# Do not change these values!
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

# Add list of python libraries you wish to install on startup in this list
# Example:
# additional_packages = ['flask-mail','nose']
ADDITIONAL_PACKAGES = []

# Select the database connectivity that you wish to use.
# THe current value defaults to sqlite
#SQLALCHEMY_DATABASE_URI = 'mysql://root:password01@127.0.0.1/flasklearn' # << use this for MySQL, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db/app.db')  # << use this for SQLite, adjust accordingly
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:s3cr3t@localhost/nembok' #<< use this for postgresql, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'oracle://scott:tiger@127.0.0.1:1521/sidname' #<< use this for oracle, adjust accordingly

# This is the default server port settings that will be used by the system
SERVER_PORT = 5000

GITHUB_CLIENT_ID = '502c898b4cb9fcd51696'
GITHUB_CLIENT_SECRET = 'fa96af28fb10efc87dea1e7a15faeac5e1074e6b'

SECRET_KEY = 'InNlY3JldC1rZXki.BFppWA.gkFJPvPbeob653P1KE1O_fKdkTs'

# end of file

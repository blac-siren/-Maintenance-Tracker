from app.DB import table_db
from app.DB import defaultAdmin

# runs migration- create table
table_db.run_migrations('development')

# create default admin
defaultAdmin.create_admin('development')

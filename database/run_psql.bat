echo Creating postgres database cct and its objects
:: Below is for dropping and creating the database
set PGPASSWORD=%DATABASE_PWD%

psql --file create_db_tables.sql --echo-errors --host=%DATABASE_HOSTNAME% --port=%DATABASE_PORT% --username=%DATABASE_USER%
psql --file roles.sql --echo-errors --host=%DATABASE_HOSTNAME% --port=%DATABASE_PORT% --username=%DATABASE_USER%
exit
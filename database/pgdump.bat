echo Dumping postgres database cct and its objects
:: Below is for dropping and creating the database
setlocal PGPASSWORD=administrator
pg_dump -Upostgres --schema-only --no-owner --create --oids --clean --if-exists  --quote-all-identifiers --verbose cct > create_db_tables.sql
:: pg_dump -Upostgres --schema-only --no-owner --oids --clean --if-exists  --quote-all-identifiers --verbose cct > create_tables.sql
exit
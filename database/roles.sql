CREATE USER app_user WITH PASSWORD '4DataL0@d' LOGIN;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA PUBLIC TO app_user;
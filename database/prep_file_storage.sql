-----------------------------------------------------------
--- File Name      : INSERT_public.file_storage.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function INSERTs  data INTO public.phases
---                  
--- 
--- 
------------------------------------------------------------
	
CREATE OR REPLACE FUNCTION prep_public.file_storage()
RETURNS VOID AS $$
DECLARE
	l_num_rows INTEGER;
BEGIN
	SELECT COUNT(1) INTO STRICT l_num_rows
	FROM   public.file_storage;
    
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Structural', NULL);
			INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Baseline', NULL);
			INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Production', NULL);
		WHEN TOO_MANY_ROWS THEN
			IF ( l_num_rows < 3 or l_num_rows > 3 ) THEN
				RAISE EXCEPTION 'Found incorrect number of rows in public.file_storage';
			END IF;
   
END; $$
LANGUAGE plpgsql;

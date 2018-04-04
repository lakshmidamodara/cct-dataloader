-----------------------------------------------------------
--- File Name      : insert_units_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.units
---                  
--- 
--- 
------------------------------------------------------------


CREATE OR REPLACE FUNCTION insert_units_data(p_name text, p_id integer)
RETURNS INTEGER AS $$
DECLARE
	l_unit_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_unit_id
	FROM public.units AS u
	WHERE
		UPPER(u.name) IS NOT DISTINCT FROM UPPER(p_name);
    
	RETURN l_unit_id;
		
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.units (name) VALUES (p_name);
			RETURN CURRVAL('public.units_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in units for name %', p_name;
   
END; $$
LANGUAGE plpgsql;
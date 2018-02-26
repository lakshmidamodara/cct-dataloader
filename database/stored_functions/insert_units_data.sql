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
BEGIN
	
	if exists ( select 1 from public.units as u where upper(u.name) = upper(p_name))
    then
          return( select id from public.units as u where upper(u.name) = upper(p_name));
    else
		
    	INSERT INTO public.units (id, name)
     	VALUES (nextval('public.units_id_seq'), p_name);
    	return currval('public.units_id_seq');
     end if;
   
END; $$
LANGUAGE plpgsql;
-----------------------------------------------------------
--- File Name      : insert_location_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts location data into public.locations
---                  
--- 
--- 
------------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_location_data(p_street varchar, p_city varchar, 
                                               p_state varchar, p_country varchar,
                                               p_latitude double precision, 
                                               p_longitude double precision)
RETURNS INTEGER AS $$
DECLARE
	l_location_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_location_id
	FROM public.locations AS loc
	WHERE
		UPPER(loc.street) IS NOT DISTINCT FROM UPPER(p_street)
        AND UPPER(loc.city) IS NOT DISTINCT FROM UPPER(p_city) 
		AND UPPER(loc.state) IS NOT DISTINCT FROM UPPER(p_state)
        AND UPPER(loc.country) IS NOT DISTINCT FROM UPPER(p_country);
		
	RETURN l_location_id;
	
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.locations (street, city, state, country, latitude, longitude)
			VALUES (p_street, p_city, p_state, p_country, p_latitude, p_longitude);
			RETURN CURRVAL('public.locations_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in phases for name %', p_name;
   
END; $$
LANGUAGE plpgsql;
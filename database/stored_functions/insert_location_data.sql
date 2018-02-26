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

drop function insert_location_data
CREATE OR REPLACE FUNCTION insert_location_data(p_street varchar, p_city varchar, 
                                               p_state varchar, p_country varchar,
                                               p_latitude double precision, 
                                               p_longitude double precision)
RETURNS INTEGER AS $$
BEGIN
	if exists ( select 1 from public.locations loc where upper(loc.street) = upper(p_street)
              and upper(loc.city) = upper(p_city) and upper(loc.state) = upper(p_state)
               and upper(loc.country) = upper(p_country))
    then
          return( select id from public.locations loc where upper(loc.street) = upper(p_street)
              and upper(loc.city) = upper(p_city) and upper(loc.state) = upper(p_state)
               and upper(loc.country) = upper(p_country));
    else
    	INSERT INTO public.locations (id, street, city, state, country, latitude, longitude)
     	VALUES (nextval('public.locations_id_seq'), p_street, p_city, p_state, p_country, p_latitude, p_longitude);
    	return currval('public.locations_id_seq');
     end if;
   
END; $$
LANGUAGE plpgsql;

selecT * from public.locations
select insert_location_data( 'St 4' , 'Hyd', 'TS','India', null, null)
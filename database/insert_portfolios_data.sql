-----------------------------------------------------------
--- File Name      : insert_portfolios_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.portfolios
---                  
--- 
--- 
------------------------------------------------------------


CREATE OR REPLACE FUNCTION insert_portfolios_data(p_name text, p_id integer)
RETURNS INTEGER AS $$
DECLARE
	l_portfolio_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_portfolio_id
	FROM public.portfolios AS u
	WHERE
		UPPER(u.name) IS NOT DISTINCT FROM UPPER(p_name);
    
	RETURN l_portfolio_id;
		
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.portfolios (name) VALUES (p_name);
			RETURN CURRVAL('public.portfolios_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in portfolios for name %', p_name;
   
END; $$
LANGUAGE plpgsql;
-----------------------------------------------------------
--- File Name      : insert_portfolio_projects_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.portfolio_projects
---                  
--- 
--- 
------------------------------------------------------------


CREATE OR REPLACE FUNCTION insert_portfolio_projects_data(p_portfolio_id integer, p_project_id integer)
RETURNS INTEGER AS $$
DECLARE
	l_portfolio_project_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_portfolio_project_id
	FROM public.portfolio_projects AS u
	WHERE
		u.portfolio_id IS NOT DISTINCT FROM p_portfolio_id
		AND u.project_id IS NOT DISTINCT FROM p_project_id
		;
    
	RETURN l_portfolio_project_id;
		
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.portfolio_projects (portfolio_id, project_id) VALUES (p_portfolio_id, p_project_id);
			RETURN CURRVAL('public.portfolio_projects_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in portfolio_projects for project_id %', p_project_id;
   
END; $$
LANGUAGE plpgsql;
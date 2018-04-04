-----------------------------------------------------------
--- File Name      : insert_project_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts data into public.projects
---                  
--- 
--- 
------------------------------------------------------------
	
CREATE OR REPLACE FUNCTION insert_project_data(p_name text, p_start date, 
                                               p_end date, p_workdays json,
                                               p_budget integer, p_bundle_title text,
											   p_location_id integer, p_contingency bigint)
RETURNS INTEGER AS $$
DECLARE
	l_project_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_project_id
	FROM public.projects AS prj
	WHERE
		UPPER(prj.name) IS NOT DISTINCT FROM UPPER(p_name)
        --AND prj.workdays IS NOT DISTINCT FROM p_workdays 
		AND prj.bundle_title IS NOT DISTINCT FROM p_bundle_title
        AND start IS NOT DISTINCT FROM p_start 
		AND "end" IS NOT DISTINCT FROM p_end 
		AND location_id IS NOT DISTINCT FROM p_location_id 
		AND contingency IS NOT DISTINCT FROM p_contingency;
		
	RETURN l_project_id;
	
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.projects (name, start, "end", workdays, budget, bundle_title, location_id, contingency)
			VALUES (p_name, p_start, p_end, p_workdays, p_budget, p_bundle_title, p_location_id, p_contingency);
			RETURN currval('public.projects_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in projects for name %', p_name;
	
END; $$
LANGUAGE plpgsql;
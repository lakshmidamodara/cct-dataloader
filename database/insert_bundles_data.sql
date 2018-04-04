-----------------------------------------------------------
--- File Name      : insert_bundles_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.bundles
---                  
--- 
--- 
------------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_bundles_data(p_parent_bundle_id integer, p_name text, 
                                                  p_project_id integer, p_title text)
RETURNS INTEGER AS $$
DECLARE
	l_bundle_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_bundle_id
	FROM public.bundles AS bun
	WHERE
		UPPER(bun.name) IS NOT DISTINCT FROM UPPER(p_name)
        AND bun.parent_bundle_id IS NOT DISTINCT FROM p_parent_bundle_id 
		AND bun.project_id IS NOT DISTINCT FROM p_project_id
		AND bun.title IS NOT DISTINCT FROM p_title;
		
	RETURN l_bundle_id;
	
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.bundles (name, parent_bundle_id, project_id, title)
			VALUES (p_name, p_parent_bundle_id, p_project_id, p_title);
			return currval('public.bundle_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in bundles for name %', p_name;
END; $$
LANGUAGE plpgsql;
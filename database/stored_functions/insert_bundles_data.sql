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
BEGIN
	
	if exists ( select 1 from public.bundles as bun where upper(bun.name) = upper(p_name)
                and bun.parent_bundle_id = p_parent_bundle_id 
				and bun.project_id = p_project_id
				and bun.title = p_title)
    then
          return( select id from public.bundles as bun where upper(bun.name) = upper(p_name)
                and bun.parent_bundle_id = p_parent_bundle_id 
				and bun.project_id = p_project_id
				and bun.title = p_title);
    else
    	INSERT INTO public.bundles (id, name, parent_bundle_id, project_id, title)
     	VALUES (nextval('public.bundle_id_seq'), p_name, p_parent_bundle_id, p_project_id, p_title);
    	return currval('public.bundle_id_seq');
     end if;
   
END; $$
LANGUAGE plpgsql;
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
BEGIN
	
	if exists ( select 1 from public.projects as prj where upper(prj.name) = upper(p_name)
                --and prj.workdays = p_workdays 
				and coalesce(prj.bundle_title,'a') = coalesce(p_bundle_title,'a')
                and start = p_start and "end" = p_end and location_id = p_location_id and coalesce(contingency,0) = coalesce(p_contingency,0))
    then
          return( select id from public.projects as prj where upper(prj.name) = upper(p_name)
                --and prj.workdays = p_workdays 
				and coalesce(prj.bundle_title,'a') = coalesce(p_bundle_title,'a')
                and start = p_start and "end" = p_end and location_id = p_location_id and coalesce(contingency,0) = coalesce(p_contingency,0));
    else
    	INSERT INTO public.projects (id, name, start, "end", workdays, budget, bundle_title, location_id, contingency)
     	VALUES (nextval('public.projects_id_seq'), p_name, p_start, p_end, p_workdays, p_budget, p_bundle_title, p_location_id, p_contingency);
    	return currval('public.projects_id_seq');
     end if;
   
END; $$
LANGUAGE plpgsql;
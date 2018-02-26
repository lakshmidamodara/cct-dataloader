-----------------------------------------------------------
--- File Name      : insert_phases_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.phases
---                  
--- 
--- 
------------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_phases_data(p_name text, p_sch_start date, p_sch_end date, p_act_start date, p_act_end date)
RETURNS INTEGER AS $$
BEGIN
	
	if exists ( select 1 from public.phases as p where upper(p.name) = upper(p_name)
				and coalesce(p.scheduled_start,'1999/01/01') = coalesce(p_sch_start, '1999/01/01') 
				and coalesce(p.scheduled_end, '1999/01/01') = coalesce(p_sch_end, '1999/01/01')
				and coalesce(p.actual_start, '1999/01/01') = coalesce(p_act_start, '1999/01/01')
				and coalesce(p.actual_end, '1999/01/01') = coalesce(p_act_end, '1999/01/01'))
    then
          return(select id from public.phases as p where  upper(p.name) = upper(p_name)
				and coalesce(p.scheduled_start,'1999/01/01') = coalesce(p_sch_start, '1999/01/01') 
				and coalesce(p.scheduled_end, '1999/01/01') = coalesce(p_sch_end, '1999/01/01')
				and coalesce(p.actual_start, '1999/01/01') = coalesce(p_act_start, '1999/01/01')
				and coalesce(p.actual_end, '1999/01/01') = coalesce(p_act_end, '1999/01/01'));
    else
		
    	INSERT INTO public.phases (id, name, scheduled_start, scheduled_end, actual_start, actual_end)
     	VALUES (nextval('public.phases_id_seq'), p_name, p_sch_start, p_sch_end, p_act_start, p_act_end);
    	return currval('public.phases_id_seq');
     end if;
   
END; $$
LANGUAGE plpgsql;

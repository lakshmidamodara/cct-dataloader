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
DECLARE
	l_phase_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_phase_id
	FROM public.phases AS p
	WHERE
		UPPER(p.name) IS NOT DISTINCT FROM UPPER(p_name)
		AND p.scheduled_start IS NOT DISTINCT FROM p_sch_start
		AND p.scheduled_end IS NOT DISTINCT FROM p_sch_end
		AND p.actual_start IS NOT DISTINCT FROM p_act_start
		AND p.actual_end IS NOT DISTINCT FROM p_act_end;
    
	RETURN l_phase_id;
	
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.phases (name, scheduled_start, scheduled_end, actual_start, actual_end) 
			VALUES (p_name, p_sch_start, p_sch_end, p_act_start, p_act_end);
			RETURN CURRVAL('public.phases_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in phases for name %', p_name;
   
END; $$
LANGUAGE plpgsql;

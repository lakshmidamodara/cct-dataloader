-----------------------------------------------------------
--- File Name      : insert_activities_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.activities
---                  
--- 
--- 
-----------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_activities_data(p_name text, p_unit_id integer, p_contractor_name text,
													p_unit_cost double precision, p_total_planned_hours integer,
													p_phase_id integer, p_project_id integer,
													p_total_planned_units bigint, p_planned_start date,
													p_planned_end date, p_unit_name text,
													p_actual_start date, p_actual_end date, 
													p_hourly_cost double precision)
RETURNS INTEGER AS $$
DECLARE 
	l_contractor_id INTEGER;
	l_activity_id INTEGER;
BEGIN
	
	SELECT id into l_contractor_id 
	  FROM public.contractors AS con 
	 WHERE 
		upper(con.name) IS NOT DISTINCT FROM upper(p_contractor_name);
	
	SELECT id INTO STRICT l_activity_id
	FROM public.activities AS act
	WHERE
		UPPER(act.name) IS NOT DISTINCT FROM UPPER(p_name)
		AND act.contractor_id IS NOT DISTINCT FROM l_contractor_id
        AND act.unit_id IS NOT DISTINCT FROM p_unit_id
		AND act.total_planned_hours IS NOT DISTINCT FROM p_total_planned_hours
		AND act.project_id IS NOT DISTINCT FROM p_project_id
		AND act.phase_id IS NOT DISTINCT FROM p_phase_id
		AND act.total_planned_units IS NOT DISTINCT FROM p_total_planned_units
		AND act.planned_start IS NOT DISTINCT FROM p_planned_start
		AND act.planned_end IS NOT DISTINCT FROM p_planned_end
		AND act.unit_name IS NOT DISTINCT FROM p_unit_name
		AND act.actual_start IS NOT DISTINCT FROM p_actual_start
		AND act.actual_end IS NOT DISTINCT FROM p_actual_end
		AND act.hourly_cost IS NOT DISTINCT FROM p_hourly_cost
		ORDER BY id;

		RETURN l_activity_id;
		
		EXCEPTION
			WHEN NO_DATA_FOUND THEN
				INSERT INTO public.activities (name, unit_id, contractor_id,
												unit_cost, total_planned_hours,
												phase_id, project_id,
												total_planned_units, planned_start,
												planned_end, unit_name,
												actual_start, actual_end, 
												hourly_cost) 
				VALUES (p_name, p_unit_id, l_contractor_id, p_unit_cost, p_total_planned_hours,
						p_phase_id, p_project_id, p_total_planned_units, p_planned_start,
						p_planned_end, p_unit_name, p_actual_start, p_actual_end, p_hourly_cost);
				RETURN CURRVAL('public.activities_id_seq');
			WHEN TOO_MANY_ROWS THEN
				RAISE EXCEPTION 'Found more than one row in activities for name %', p_name;
   
END; $$
LANGUAGE plpgsql;
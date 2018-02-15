-----------------------------------------------------------
--- File Name      : update_baseline_activities.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This function processes baseline data in temp.activities and
---                  populates public.activities table
--- 
--- 
--- ---------------------------------------------------------


CREATE OR REPLACE FUNCTION update_baseline_activities()
RETURNS VOID AS $$
BEGIN
    UPDATE public.activities act
       SET total_planned_hours = t.total_planned_hours,
           total_planned_units = t.total_planned_units,
           planned_start = t.planned_start,
           planned_end = t.planned_end
      FROM ( SELECT tact.name, unit.id as unit_id, cntrs.id as contractor_id, proj.id as project_id,
                    tact.total_planned_hours, tact.total_planned_units, tact.planned_start, 
                    tact.planned_end
               FROM temp.activities as tact
              INNER JOIN public.units as unit on tact.unit_name = unit.name
              INNER JOIN public.contractors as cntrs on cntrs.name = tact.contractor_name
              INNER JOIN public.projects as proj on proj.name = tact.project_name ) as t
     WHERE UPPER(t.name) = UPPER(act.name)
       AND t.unit_id = act.unit_id
       AND t.contractor_id = act.contractor_id
       AND t.project_id = act.project_id;
END; $$
LANGUAGE plpgsql;


--- End
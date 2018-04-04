-----------------------------------------------------------
--- File Name      : update_production_activity_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This function inserts production data into public.activity_data
---                  from temp.activity_data. 
--- 
--- 
------------------------------------------------------------


CREATE OR REPLACE FUNCTION update_production_activity_data()
RETURNS VOID AS $$
BEGIN
    UPDATE public.activity_data act
       SET actual_hours = t.actual_hours,
           actual_units = t.actual_units,
           updated = current_timestamp(2)
      FROM ( SELECT pact.id, tact.date, tact.actual_hours, 
                    tact.actual_units
               FROM public.activities as pact,
                    temp.activity_data as tact
              WHERE UPPER(pact.name) = UPPER(tact.activity_name)
            ) as t
     WHERE t.id= act.activity_id
       AND t.date = act.date;
END; $$
LANGUAGE plpgsql;
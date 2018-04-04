-----------------------------------------------------------
--- File Name      : update_baseLine_activity_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This function inserts baseline data into public.activity_data
---                  from temp.activity_data. 
--- 
--- 
------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_baseline_activity_data()
RETURNS VOID AS $$
BEGIN

    PERFORM insert_activity_data();
    
    UPDATE public.activity_data act
       SET planned_hours = t.planned_hours,
           planned_units = t.planned_units,
           created = current_timestamp(2)
      FROM ( SELECT pact.id, tact.date, tact.planned_hours, 
                    tact.planned_units
               FROM public.activities as pact,
                    temp.activity_data as tact
              WHERE UPPER(pact.name) = UPPER(tact.activity_name)
            ) as t
     WHERE t.id= act.activity_id
       AND t.date = act.date;
END; $$
LANGUAGE plpgsql;


---END
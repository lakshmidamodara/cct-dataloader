-----------------------------------------------------------
--- File Name      : insert_activity_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This function inserts rows into public.activity_data
---                  from temp.activity_data. Only rows not already present
---                  will be inserted. This function should be run prior to
---                  calling update_baseline_activity_data
--- 
--- 
------------------------------------------------------------


CREATE OR REPLACE FUNCTION insert_activity_data()
RETURNS VOID AS $$
BEGIN
    INSERT INTO public.activity_data (activity_id, date)
      SELECT act.id, tact.date
      FROM public.activities as act,
             temp.activity_data as tact
     WHERE UPPER(act.name) = UPPER(tact.activity_name)
       AND 1 not in ( SELECT 1 
                        FROM public.activity_data as adata
                       WHERE act.id = adata.activity_id
                         AND UPPER(act.name) = UPPER(tact.activity_name)
                         AND adata.date = tact.date ) ;
                         
END; $$
LANGUAGE plpgsql;

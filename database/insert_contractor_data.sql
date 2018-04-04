-----------------------------------------------------------
--- File Name      : insert_contractor_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 02/28/2018
--- Updated on     : 
--- Version        : 1.0
--- Description    : This function inserts  data into public.contractors
---                  
--- 
--- 
------------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_contractor_data(p_name text, p_email text, 
                                                  p_phone text, p_pm_contact CHARACTER VARYING)
RETURNS INTEGER AS $$
DECLARE
	contractorId INTEGER;
BEGIN
	SELECT id INTO STRICT contractorId
	FROM public.contractors AS con
	WHERE
		UPPER(con.name) IS NOT DISTINCT FROM UPPER(p_name)
        AND UPPER(con.email) IS NOT DISTINCT FROM UPPER(p_email)
        AND con.phone IS NOT DISTINCT FROM p_phone
		AND UPPER(con.pm_contact) IS NOT DISTINCT FROM UPPER(p_pm_contact)
		ORDER BY id;

		RETURN contractorId;

		EXCEPTION
			WHEN NO_DATA_FOUND THEN
				INSERT INTO public.contractors (name, email, phone, pm_contact) VALUES (p_name, p_email, p_phone, p_pm_contact);
				RETURN CURRVAL('public.contractors_id_seq');
			WHEN TOO_MANY_ROWS THEN
				RAISE EXCEPTION 'Found more than one row in contractors for name %', p_name;

END; $$
LANGUAGE plpgsql;


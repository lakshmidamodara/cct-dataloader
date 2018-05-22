--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

-- Started on 2018-03-08 19:24:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS "cct";
--
-- TOC entry 3100 (class 1262 OID 16655)
-- Name: cct; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE "cct" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect "cct"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3101 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


--
-- TOC entry 8 (class 2615 OID 16921)
-- Name: temp; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA "temp";


--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "plpgsql" WITH SCHEMA "pg_catalog";


--
-- TOC entry 3103 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION "plpgsql"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "plpgsql" IS 'PL/pgSQL procedural language';


SET search_path = "public", pg_catalog;

--
-- TOC entry 268 (class 1255 OID 16961)
-- Name: checkforbaselinedata(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "checkforbaselinedata"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
   BEGIN
      IF ( TG_OP = 'UPDATE')
      THEN
          IF (old.total_planned_hours is not null) OR
             (old.total_planned_units is not null) OR
             (old.planned_start is not null) OR
             (old.planned_end is not null)
          THEN
             new.total_planned_hours = old.total_planned_hours;
             new.total_planned_units = old.total_planned_units;
             new.planned_start = old.planned_start;
             new.planned_end = old.planned_end;
          END IF;
          RETURN NEW;
      ELSIF (TG_OP = 'DELETE') 
      THEN
          RETURN NULL;
      END IF;
END; $$;


--
-- TOC entry 281 (class 1255 OID 25776)
-- Name: insert_activities_data("text", integer, "text", double precision, integer, integer, integer, bigint, "date", "date", "text", "date", "date", double precision); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_activities_data"("p_name" "text", "p_unit_id" integer, "p_contractor_name" "text", "p_unit_cost" double precision, "p_total_planned_hours" integer, "p_phase_id" integer, "p_project_id" integer, "p_total_planned_units" bigint, "p_planned_start" "date", "p_planned_end" "date", "p_unit_name" "text", "p_actual_start" "date", "p_actual_end" "date", "p_hourly_cost" double precision) RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

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

   

END; $$;


--
-- TOC entry 265 (class 1255 OID 17058)
-- Name: insert_activity_data(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_activity_data"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
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
                         
END; $$;


--
-- TOC entry 256 (class 1255 OID 25497)
-- Name: insert_bundles_data(integer, "text", integer, "text"); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_bundles_data"("p_parent_bundle_id" integer, "p_name" "text", "p_project_id" integer, "p_title" "text") RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_bundle_id INTEGER;

BEGIN

	SELECT id INTO STRICT l_bundle_id

	FROM public.bundles AS bun

	WHERE

		UPPER(bun.name) IS NOT DISTINCT FROM UPPER(p_name)

        AND bun.parent_bundle_id IS NOT DISTINCT FROM p_parent_bundle_id 

		AND bun.project_id IS NOT DISTINCT FROM p_project_id

		AND bun.title IS NOT DISTINCT FROM p_title;

		

	RETURN l_bundle_id;

	

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO public.bundles (name, parent_bundle_id, project_id, title)

			VALUES (p_name, p_parent_bundle_id, p_project_id, p_title);

			return currval('public.bundle_id_seq');

		WHEN TOO_MANY_ROWS THEN

			RAISE EXCEPTION 'Found more than one row in bundles for name %', p_name;

END; $$;


--
-- TOC entry 266 (class 1255 OID 25496)
-- Name: insert_bundles_data(integer, "text", "text", "text"); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_bundles_data"("p_parent_bundle_id" integer, "p_name" "text", "p_project_id" "text", "p_title" "text") RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

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

     	VALUES (nextval('public.bundles_id_seq'), p_name, p_parent_bundle_id, p_project_id, p_title);

    	return currval('public.bundles_id_seq');

     end if;

   

END; $$;


--
-- TOC entry 277 (class 1255 OID 25438)
-- Name: insert_contractor_data("text", "text", "text", character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_contractor_data"("p_name" "text", "p_email" "text", "p_phone" "text", "p_pm_contact" character varying) RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

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



END; $$;


--
-- TOC entry 279 (class 1255 OID 25146)
-- Name: insert_location_data(character varying, character varying, character varying, character varying, double precision, double precision); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_location_data"("p_street" character varying, "p_city" character varying, "p_state" character varying, "p_country" character varying, "p_latitude" double precision, "p_longitude" double precision) RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_location_id INTEGER;

BEGIN

	SELECT id INTO STRICT l_location_id

	FROM public.locations AS loc

	WHERE

		UPPER(loc.street) IS NOT DISTINCT FROM UPPER(p_street)

        AND UPPER(loc.city) IS NOT DISTINCT FROM UPPER(p_city) 

		AND UPPER(loc.state) IS NOT DISTINCT FROM UPPER(p_state)

        AND UPPER(loc.country) IS NOT DISTINCT FROM UPPER(p_country);

		

	RETURN l_location_id;

	

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO public.locations (street, city, state, country, latitude, longitude)

			VALUES (p_street, p_city, p_state, p_country, p_latitude, p_longitude);

			RETURN CURRVAL('public.locations_id_seq');

		WHEN TOO_MANY_ROWS THEN

			RAISE EXCEPTION 'Found more than one row in phases for name %', p_name;

   

END; $$;


--
-- TOC entry 275 (class 1255 OID 25760)
-- Name: insert_phases_data("text", "date", "date", "date", "date"); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_phases_data"("p_name" "text", "p_sch_start" "date", "p_sch_end" "date", "p_act_start" "date", "p_act_end" "date") RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_phase_id INTEGER;

BEGIN

	SELECT id INTO STRICT l_phase_id

	FROM public.phases AS p

	WHERE

		UPPER(p.name) IS NOT DISTINCT FROM UPPER(p_name)

		and p.scheduled_start IS NOT DISTINCT FROM p_sch_start

		and p.scheduled_end IS NOT DISTINCT FROM p_sch_end

		and p.actual_start IS NOT DISTINCT FROM p_act_start

		and p.actual_end IS NOT DISTINCT FROM p_act_end;

    

	RETURN l_phase_id;

	

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO public.phases (name, scheduled_start, scheduled_end, actual_start, actual_end) 

			VALUES (p_name, p_sch_start, p_sch_end, p_act_start, p_act_end);

			RETURN CURRVAL('public.phases_id_seq');

		WHEN TOO_MANY_ROWS THEN

			RAISE EXCEPTION 'Found more than one row in phases for name %', p_name;

   

END; $$;


--
-- 
-- Name: insert_portfolios_data("text", integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE OR REPLACE FUNCTION insert_portfolios_data(p_name text, p_id integer)
RETURNS INTEGER AS $$
DECLARE
	l_portfolio_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_portfolio_id
	FROM public.portfolios AS u
	WHERE
		UPPER(u.name) IS NOT DISTINCT FROM UPPER(p_name);
    
	RETURN l_portfolio_id;
		
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.portfolios (name) VALUES (p_name);
			RETURN CURRVAL('public.portfolios_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in portfolios for name %', p_name;
   
END; $$
LANGUAGE plpgsql;

--
-- 
-- Name: insert_portfolio_projects_data(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE OR REPLACE FUNCTION insert_portfolio_projects_data(p_portfolio_id integer, p_project_id integer)
RETURNS INTEGER AS $$
DECLARE
	l_portfolio_project_id INTEGER;
BEGIN
	SELECT id INTO STRICT l_portfolio_project_id
	FROM public.portfolio_projects AS u
	WHERE
		u.portfolio_id IS NOT DISTINCT FROM p_portfolio_id
		AND u.project_id IS NOT DISTINCT FROM p_project_id
		;
    
	RETURN l_portfolio_project_id;
		
	EXCEPTION
		WHEN NO_DATA_FOUND THEN
			INSERT INTO public.portfolio_projects (portfolio_id, project_id) VALUES (p_portfolio_id, p_project_id);
			RETURN CURRVAL('public.portfolio_projects_id_seq');
		WHEN TOO_MANY_ROWS THEN
			RAISE EXCEPTION 'Found more than one row in portfolio_projects for project_id %', p_project_id;
   
END; $$
LANGUAGE plpgsql;

--
-- TOC entry 263 (class 1255 OID 25284)
-- Name: insert_project_data("text", "date", "date", "json", integer, "text", integer, bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_project_data"("p_name" "text", "p_start" "date", "p_end" "date", "p_workdays" "json", "p_budget" integer, "p_bundle_title" "text", "p_location_id" integer, "p_contingency" bigint) RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_project_id INTEGER;

BEGIN

	SELECT id INTO STRICT l_project_id

	FROM public.projects AS prj

	WHERE

		UPPER(prj.name) IS NOT DISTINCT FROM UPPER(p_name)

        --AND prj.workdays IS NOT DISTINCT FROM p_workdays 

		AND prj.bundle_title IS NOT DISTINCT FROM p_bundle_title

        AND start IS NOT DISTINCT FROM p_start 

		AND "end" IS NOT DISTINCT FROM p_end 

		AND location_id IS NOT DISTINCT FROM p_location_id 

		AND contingency IS NOT DISTINCT FROM p_contingency;

		

	RETURN l_project_id;

	

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO public.projects (name, start, "end", workdays, budget, bundle_title, location_id, contingency)

			VALUES (p_name, p_start, p_end, p_workdays, p_budget, p_bundle_title, p_location_id, p_contingency);

			RETURN currval('public.projects_id_seq');

		WHEN TOO_MANY_ROWS THEN

			RAISE EXCEPTION 'Found more than one row in projects for name %', p_name;

	

END; $$;


--
-- TOC entry 262 (class 1255 OID 25746)
-- Name: insert_units_data("text", integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "insert_units_data"("p_name" "text", "p_id" integer) RETURNS integer
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_unit_id INTEGER;

BEGIN

	SELECT id INTO STRICT l_unit_id

	FROM public.units AS u

	WHERE

		UPPER(u.name) = UPPER(p_name);

    

	RETURN l_unit_id;

		

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO public.units (name) VALUES (p_name);

			RETURN CURRVAL('public.units_id_seq');

		WHEN TOO_MANY_ROWS THEN

			RAISE EXCEPTION 'Found more than one row in units for name %', p_name;

   

END; $$;


--
-- TOC entry 271 (class 1255 OID 25970)
-- Name: prep_file_storage(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "prep_file_storage"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$

DECLARE

	l_num_rows INTEGER;

BEGIN

	SELECT COUNT(1) INTO STRICT l_num_rows

	FROM   file_storage;

    

	EXCEPTION

		WHEN NO_DATA_FOUND THEN

			INSERT INTO file_storage (load_type, filename) VALUES ( 'Structural', NULL);

			INSERT INTO file_storage (load_type, filename) VALUES ( 'Baseline', NULL);

			INSERT INTO file_storage (load_type, filename) VALUES ( 'Production', NULL);

		WHEN TOO_MANY_ROWS THEN

			IF ( l_num_rows < 3 or l_num_rows > 3 ) THEN

				RAISE EXCEPTION 'Found incorrect number of rows in file_storage';

			END IF;

   

END; $$;


--
-- TOC entry 278 (class 1255 OID 17056)
-- Name: update_baseline_activities(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "update_baseline_activities"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
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
END; $$;


--
-- TOC entry 269 (class 1255 OID 17059)
-- Name: update_baseline_activity_data(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "update_baseline_activity_data"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
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
END; $$;


--
-- TOC entry 273 (class 1255 OID 17057)
-- Name: update_production_activities(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "update_production_activities"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    UPDATE public.activities act
       SET actual_start= t.actual_start,
           actual_end = t.actual_end
      FROM ( SELECT tact.name, unit.id as unit_id, cntrs.id as contractor_id, proj.id as project_id,
                    tact.actual_start, tact.actual_end
               FROM temp.activities as tact
              INNER JOIN public.units as unit on tact.unit_name = unit.name
              INNER JOIN public.contractors as cntrs on cntrs.name = tact.contractor_name
              INNER JOIN public.projects as proj on proj.name = tact.project_name ) as t
     WHERE UPPER(t.name) = UPPER(act.name)
       AND t.unit_id = act.unit_id
       AND t.contractor_id = act.contractor_id
       AND t.project_id = act.project_id;
END; $$;


--
-- TOC entry 261 (class 1255 OID 17060)
-- Name: update_production_activity_data(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "update_production_activity_data"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
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
END; $$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 215 (class 1259 OID 16703)
-- Name: activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "activities" (
    "id" integer NOT NULL,
    "name" "text",
    "unit_id" integer,
    "contractor_id" integer,
    "unit_cost" double precision,
    "total_planned_hours" integer,
    "project_id" integer,
    "total_planned_units" bigint,
    "planned_start" "date",
    "planned_end" "date",
    "unit_name" "text",
    "actual_start" "date",
    "actual_end" "date",
    "hourly_cost" double precision,
    "required_activities" integer[],
    "phase_id" integer
);


--
-- TOC entry 216 (class 1259 OID 16710)
-- Name: activity_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "activity_data" (
    "id" integer NOT NULL,
    "activity_id" integer NOT NULL,
    "date" "date",
    "actual_hours" integer,
    "actual_units" integer,
    "planned_hours" bigint,
    "planned_units" double precision,
    "updated" timestamp(6) without time zone,
    "created" timestamp(6) without time zone
);


--
-- TOC entry 221 (class 1259 OID 16737)
-- Name: contractors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "contractors" (
    "name" "text",
    "email" "text",
    "phone" "text",
    "pm_contact" character varying,
    "id" smallint NOT NULL
);


--
-- TOC entry 238 (class 1259 OID 16836)
-- Name: projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "projects" (
    "id" integer DEFAULT "nextval"(('public.projects_id_seq'::"text")::"regclass") NOT NULL,
    "name" "text",
    "start" "date",
    "end" "date",
    "workdays" "json",
    "budget" integer,
    "bundle_title" "text",
    "location_id" integer,
    "contingency" bigint
);


--
-- TOC entry 249 (class 1259 OID 17378)
-- Name: activities_activity_data; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "activities_activity_data" AS
 SELECT "proj"."id" AS "proj_id",
    "proj"."name" AS "proj_name",
    "proj"."start" AS "proj_start",
    "proj"."end" AS "proj_end",
    "act"."id" AS "activity_id",
    "act"."name" AS "activity_name",
    "act"."unit_id",
    "act"."unit_name",
    "act"."planned_start" AS "activity_pl_start",
    "act"."planned_end" AS "activity_pl_end",
    "act"."actual_start" AS "activity_act_start",
    "act"."actual_end" AS "activity_act_end",
    "act"."contractor_id",
    "con"."name" AS "contractor_name",
    "act_data"."id" AS "activity_data_id",
    "act_data"."date" AS "activitiy_data_date",
    "act_data"."planned_hours" AS "act_data_pl_hrs",
    "act_data"."planned_units" AS "act_data_pl_units",
    "act_data"."actual_hours" AS "act_data_act_hrs",
    "act_data"."actual_units" AS "act_data_act_units"
   FROM ((("activities" "act"
     FULL JOIN "projects" "proj" ON (("proj"."id" = "act"."project_id")))
     LEFT JOIN "contractors" "con" ON (("con"."id" = "act"."contractor_id")))
     LEFT JOIN "activity_data" "act_data" ON (("act_data"."activity_id" = "act"."id")));


--
-- TOC entry 197 (class 1259 OID 16656)
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "activities_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3104 (class 0 OID 0)
-- Dependencies: 197
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "activities_id_seq" OWNED BY "activities"."id";


--
-- TOC entry 198 (class 1259 OID 16658)
-- Name: activity_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "activity_data_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3105 (class 0 OID 0)
-- Dependencies: 198
-- Name: activity_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "activity_data_id_seq" OWNED BY "activity_data"."id";


--
-- TOC entry 217 (class 1259 OID 16715)
-- Name: bundle_activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "bundle_activities" (
    "bundle_id" integer,
    "activity_id" integer,
    "id" smallint NOT NULL
);


--
-- TOC entry 199 (class 1259 OID 16660)
-- Name: bundle_activities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "bundle_activities_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


--
-- TOC entry 200 (class 1259 OID 16662)
-- Name: bundle_activities_id_seq1; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "bundle_activities_id_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3106 (class 0 OID 0)
-- Dependencies: 200
-- Name: bundle_activities_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "bundle_activities_id_seq1" OWNED BY "bundle_activities"."id";


--
-- TOC entry 201 (class 1259 OID 16664)
-- Name: bundle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "bundle_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


--
-- TOC entry 218 (class 1259 OID 16719)
-- Name: bundle_phases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "bundle_phases" (
    "id" smallint NOT NULL,
    "bundle_id" integer,
    "phase_id" integer
);


--
-- TOC entry 202 (class 1259 OID 16666)
-- Name: bundle_phases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "bundle_phases_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3107 (class 0 OID 0)
-- Dependencies: 202
-- Name: bundle_phases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "bundle_phases_id_seq" OWNED BY "bundle_phases"."id";


--
-- TOC entry 219 (class 1259 OID 16723)
-- Name: bundles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "bundles" (
    "id" integer DEFAULT "nextval"(('public.bundle_id_seq'::"text")::"regclass") NOT NULL,
    "parent_bundle_id" integer,
    "name" "text",
    "project_id" integer,
    "title" "text",
    "phase_id" integer
);


--
-- TOC entry 220 (class 1259 OID 16730)
-- Name: change_orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "change_orders" (
    "id" integer DEFAULT "nextval"(('public.change_orders'::"text")::"regclass") NOT NULL,
    "project_id" integer,
    "contractor_id" integer,
    "description" "text",
    "approved_cost" double precision,
    "estimted_cost" double precision,
    "date_submitted" "date",
    "date_approved" "date",
    "percent_complete" double precision
);


--
-- TOC entry 252 (class 1259 OID 25772)
-- Name: contractorid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "contractorid" (
    "id" smallint
);


--
-- TOC entry 250 (class 1259 OID 25457)
-- Name: contractors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "contractors_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3108 (class 0 OID 0)
-- Dependencies: 250
-- Name: contractors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "contractors_id_seq" OWNED BY "contractors"."id";


--
-- TOC entry 203 (class 1259 OID 16668)
-- Name: contractors_id_seq1; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "contractors_id_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3109 (class 0 OID 0)
-- Dependencies: 203
-- Name: contractors_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "contractors_id_seq1" OWNED BY "contractors"."id";


--
-- TOC entry 248 (class 1259 OID 17302)
-- Name: file_storage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "file_storage" (
    "load_type" "text",
    "filename" "text",
    "filedata" "bytea",
    "updated" timestamp(6) without time zone
);


--
-- TOC entry 222 (class 1259 OID 16744)
-- Name: incident_classes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "incident_classes" (
    "id" integer NOT NULL,
    "name" "text"
);


--
-- TOC entry 223 (class 1259 OID 16751)
-- Name: incident_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "incident_types" (
    "id" integer NOT NULL,
    "name" "text"
);


--
-- TOC entry 224 (class 1259 OID 16758)
-- Name: incidents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "incidents" (
    "id" integer NOT NULL,
    "date" "date",
    "contractor_id" integer,
    "incident_type_id" integer,
    "incident_class_id" integer,
    "project_id" integer
);


--
-- TOC entry 204 (class 1259 OID 16670)
-- Name: incidents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "incidents_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3110 (class 0 OID 0)
-- Dependencies: 204
-- Name: incidents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "incidents_id_seq" OWNED BY "incidents"."id";


--
-- TOC entry 225 (class 1259 OID 16762)
-- Name: indirect_costs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "indirect_costs" (
    "id" integer NOT NULL,
    "actual_amount" double precision,
    "planned_amount" integer,
    "project_id" integer
);


--
-- TOC entry 226 (class 1259 OID 16765)
-- Name: installations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "installations" (
    "id" integer DEFAULT "nextval"(('public.installations'::"text")::"regclass") NOT NULL,
    "item_id" integer,
    "date_installed" "date",
    "units_installed" integer,
    "units_failed" integer
);


--
-- TOC entry 227 (class 1259 OID 16769)
-- Name: invoices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "invoices" (
    "id" integer NOT NULL,
    "activity_id" integer,
    "amount" double precision,
    "date_invoiced" "date"
);


--
-- TOC entry 228 (class 1259 OID 16772)
-- Name: issue_statuses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "issue_statuses" (
    "id" integer NOT NULL,
    "name" "text"
);


--
-- TOC entry 229 (class 1259 OID 16779)
-- Name: issues; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "issues" (
    "id" integer NOT NULL,
    "name" "text",
    "responsible" "text",
    "description" "text",
    "status" "text",
    "resolution" "text",
    "deadline" "date",
    "updated_by" "text",
    "updated" "date",
    "activity_id" integer,
    "issue_status_id" integer
);


--
-- TOC entry 230 (class 1259 OID 16786)
-- Name: items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "items" (
    "id" integer NOT NULL,
    "name" character varying(100)
);


--
-- TOC entry 253 (class 1259 OID 25948)
-- Name: l_contractor_id; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "l_contractor_id" (
    "id" smallint
);


--
-- TOC entry 231 (class 1259 OID 16789)
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "locations" (
    "id" integer DEFAULT "nextval"(('public.locations_id_seq'::"text")::"regclass") NOT NULL,
    "street" "text",
    "city" "text",
    "state" "text",
    "country" "text",
    "latitude" double precision,
    "longitude" double precision
);


--
-- TOC entry 205 (class 1259 OID 16672)
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "locations_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


--
-- TOC entry 232 (class 1259 OID 16796)
-- Name: milestones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "milestones" (
    "name" "text",
    "actual" "date",
    "planned" "date",
    "contract" "date",
    "project_id" integer,
    "phase_id" integer,
    "id" smallint NOT NULL
);


--
-- TOC entry 206 (class 1259 OID 16674)
-- Name: milestones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "milestones_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3111 (class 0 OID 0)
-- Dependencies: 206
-- Name: milestones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "milestones_id_seq" OWNED BY "milestones"."id";


--
-- TOC entry 233 (class 1259 OID 16803)
-- Name: ncrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "ncrs" (
    "id" integer DEFAULT "nextval"(('public.ncrs'::"text")::"regclass") NOT NULL,
    "project_id" integer,
    "contractor_id" integer,
    "description" "text",
    "date_open" "date",
    "date_closed" "date"
);


--
-- TOC entry 207 (class 1259 OID 16676)
-- Name: new_table_0_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "new_table_0_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3112 (class 0 OID 0)
-- Dependencies: 207
-- Name: new_table_0_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "new_table_0_id_seq" OWNED BY "incident_types"."id";


--
-- TOC entry 208 (class 1259 OID 16678)
-- Name: new_table_0_id_seq1; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "new_table_0_id_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3113 (class 0 OID 0)
-- Dependencies: 208
-- Name: new_table_0_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "new_table_0_id_seq1" OWNED BY "incident_classes"."id";


--
-- TOC entry 209 (class 1259 OID 16680)
-- Name: new_table_0_id_seq2; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "new_table_0_id_seq2"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3114 (class 0 OID 0)
-- Dependencies: 209
-- Name: new_table_0_id_seq2; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "new_table_0_id_seq2" OWNED BY "issues"."id";


--
-- TOC entry 210 (class 1259 OID 16682)
-- Name: new_table_1_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "new_table_1_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3115 (class 0 OID 0)
-- Dependencies: 210
-- Name: new_table_1_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "new_table_1_id_seq" OWNED BY "issue_statuses"."id";


--
-- TOC entry 234 (class 1259 OID 16810)
-- Name: phases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "phases" (
    "name" "text",
    "scheduled_start" "date",
    "scheduled_end" "date",
    "actual_start" "date",
    "actual_end" "date",
    "id" smallint NOT NULL
);


--
-- TOC entry 211 (class 1259 OID 16684)
-- Name: phases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "phases_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3116 (class 0 OID 0)
-- Dependencies: 211
-- Name: phases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "phases_id_seq" OWNED BY "phases"."id";


--
-- TOC entry 235 (class 1259 OID 16818)
-- Name: portfolio_projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "portfolio_projects" (
    "id" integer NOT NULL,
    "portfolio_id" integer,
    "project_id" integer
);


--
-- TOC entry 212 (class 1259 OID 16686)
-- Name: portfolio_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "portfolio_projects_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3117 (class 0 OID 0)
-- Dependencies: 212
-- Name: portfolio_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "portfolio_projects_id_seq" OWNED BY "portfolio_projects"."id";


--
-- TOC entry 236 (class 1259 OID 16822)
-- Name: portfolios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "portfolios" (
    "id" integer NOT NULL,
    "name" "text"
);


--
-- TOC entry 213 (class 1259 OID 16688)
-- Name: portfolios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "portfolios_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3118 (class 0 OID 0)
-- Dependencies: 213
-- Name: portfolios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "portfolios_id_seq" OWNED BY "portfolios"."id";


--
-- TOC entry 237 (class 1259 OID 16829)
-- Name: procurements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "procurements" (
    "id" integer DEFAULT "nextval"(('public.procurements'::"text")::"regclass") NOT NULL,
    "name" "text",
    "date_needed" "date",
    "date_delivered" "date",
    "project_id" integer
);


--
-- TOC entry 251 (class 1259 OID 25742)
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "units_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


--
-- TOC entry 239 (class 1259 OID 16843)
-- Name: units; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "units" (
    "id" integer DEFAULT "nextval"('"units_id_seq"'::"regclass") NOT NULL,
    "name" "text"
);


--
-- TOC entry 254 (class 1259 OID 34161)
-- Name: project_activities; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "project_activities" AS
 SELECT "proj"."id" AS "proj_id",
    "proj"."name" AS "proj_name",
    "proj"."start" AS "proj_start",
    "proj"."end" AS "proj_end",
    "loc"."id" AS "loc_id",
    "loc"."state" AS "loc_state",
    "act"."id" AS "activity_id",
    "act"."name" AS "activity_name",
    "act"."unit_id",
    "act"."planned_start" AS "activity_pl_start",
    "act"."planned_end" AS "activity_pl_end",
    "act"."actual_start" AS "activity_act_start",
    "act"."actual_end" AS "activity_act_end",
    "unit"."name" AS "unit_name",
    "act"."contractor_id",
    "con"."name" AS "contractor_name",
    "bact"."id" AS "bundle_id",
    "bun"."name" AS "bundle_name",
    "ph"."id" AS "phase_id",
    "ph"."name" AS "phase_name",
    "ph"."scheduled_start" AS "ph_pl_start",
    "ph"."scheduled_end" AS "ph_pl_end",
    "ph"."actual_start" AS "ph_act_start",
    "ph"."actual_end" AS "ph_act_end"
   FROM (((((((("activities" "act"
     LEFT JOIN "projects" "proj" ON (("proj"."id" = "act"."project_id")))
     LEFT JOIN "locations" "loc" ON (("loc"."id" = "proj"."location_id")))
     LEFT JOIN "units" "unit" ON (("unit"."id" = "act"."unit_id")))
     LEFT JOIN "contractors" "con" ON (("con"."id" = "act"."contractor_id")))
     LEFT JOIN "bundle_activities" "bact" ON (("bact"."activity_id" = "act"."id")))
     LEFT JOIN "bundles" "bun" ON ((("bact"."id" = "bun"."id") AND ("proj"."id" = "bun"."project_id"))))
     LEFT JOIN "bundle_phases" "bph" ON (("bph"."id" = "bun"."id")))
     LEFT JOIN "phases" "ph" ON (("ph"."id" = "bph"."phase_id")));


--
-- TOC entry 214 (class 1259 OID 16690)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "projects_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


--
-- TOC entry 240 (class 1259 OID 16850)
-- Name: variance_reasons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "variance_reasons" (
    "id" integer DEFAULT "nextval"(('public.variance_reasons'::"text")::"regclass") NOT NULL,
    "variance_id" integer,
    "comment" "text",
    "created" "date",
    "updated" "date"
);


--
-- TOC entry 241 (class 1259 OID 16857)
-- Name: variances; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "variances" (
    "id" integer DEFAULT "nextval"(('public.variances'::"text")::"regclass") NOT NULL,
    "activity_id" integer,
    "reported_date" "date",
    "updated_date" "date"
);


--
-- TOC entry 242 (class 1259 OID 16861)
-- Name: weightings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "weightings" (
    "id" integer DEFAULT "nextval"(('public.weightings'::"text")::"regclass") NOT NULL,
    "score" "text",
    "weighting" numeric
);


SET search_path = "temp", pg_catalog;

--
-- TOC entry 243 (class 1259 OID 16922)
-- Name: activities; Type: TABLE; Schema: temp; Owner: -
--

CREATE TABLE "activities" (
	"id" integer,
    "name" "text",
    "contractor_name" "text",
    "unit_cost" double precision,
    "total_planned_hours" integer,
    "project_name" "text",
    "total_planned_units" bigint,
    "planned_start" "date",
    "planned_end" "date",
    "unit_name" "text",
    "actual_start" "date",
    "actual_end" "date",
    "hourly_cost" double precision,
    "required_activities" integer[]
);


--
-- TOC entry 245 (class 1259 OID 16947)
-- Name: activity_data; Type: TABLE; Schema: temp; Owner: -
--

CREATE TABLE "activity_data" (
	"id" integer,
    "activity_name" "text",
    "date" "date",
    "actual_hours" integer,
    "actual_units" integer,
    "planned_hours" bigint,
    "planned_units" double precision,
    "updated" timestamp(6) without time zone,
    "created" timestamp(6) without time zone
);


--
-- TOC entry 247 (class 1259 OID 17287)
-- Name: contractors; Type: TABLE; Schema: temp; Owner: -
--

CREATE TABLE "contractors" (
	"id" integer,
    "name" "text",
    "email" "text",
    "phone" "text",
    "pm_contact" character varying
);


--
-- TOC entry 246 (class 1259 OID 17263)
-- Name: projects; Type: TABLE; Schema: temp; Owner: -
--

CREATE TABLE "projects" (
	"id" integer,
    "name" "text",
    "start_dt" "date",
    "end_dt" "date",
    "workdays" "json",
    "budget" integer,
    "bundle_title" "text",
    "location_name" "text",
    "contingency" bigint
);


--
-- TOC entry 244 (class 1259 OID 16928)
-- Name: units; Type: TABLE; Schema: temp; Owner: -
--

CREATE TABLE "units" (
	"id" integer,
    "name" "text"
);


SET search_path = "public", pg_catalog;

--
-- TOC entry 2896 (class 2604 OID 16706)
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "activities" ALTER COLUMN "id" SET DEFAULT "nextval"('"activities_id_seq"'::"regclass");


--
-- TOC entry 2897 (class 2604 OID 16713)
-- Name: activity_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "activity_data" ALTER COLUMN "id" SET DEFAULT "nextval"('"activity_data_id_seq"'::"regclass");


--
-- TOC entry 2898 (class 2604 OID 16718)
-- Name: bundle_activities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "bundle_activities" ALTER COLUMN "id" SET DEFAULT "nextval"('"bundle_activities_id_seq1"'::"regclass");


--
-- TOC entry 2899 (class 2604 OID 16722)
-- Name: bundle_phases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "bundle_phases" ALTER COLUMN "id" SET DEFAULT "nextval"('"bundle_phases_id_seq"'::"regclass");


--
-- TOC entry 2902 (class 2604 OID 25459)
-- Name: contractors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "contractors" ALTER COLUMN "id" SET DEFAULT "nextval"('"contractors_id_seq"'::"regclass");


--
-- TOC entry 2903 (class 2604 OID 16747)
-- Name: incident_classes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incident_classes" ALTER COLUMN "id" SET DEFAULT "nextval"('"new_table_0_id_seq1"'::"regclass");


--
-- TOC entry 2904 (class 2604 OID 16754)
-- Name: incident_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incident_types" ALTER COLUMN "id" SET DEFAULT "nextval"('"new_table_0_id_seq"'::"regclass");


--
-- TOC entry 2905 (class 2604 OID 16761)
-- Name: incidents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incidents" ALTER COLUMN "id" SET DEFAULT "nextval"('"incidents_id_seq"'::"regclass");


--
-- TOC entry 2907 (class 2604 OID 16775)
-- Name: issue_statuses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "issue_statuses" ALTER COLUMN "id" SET DEFAULT "nextval"('"new_table_1_id_seq"'::"regclass");


--
-- TOC entry 2908 (class 2604 OID 16782)
-- Name: issues id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "issues" ALTER COLUMN "id" SET DEFAULT "nextval"('"new_table_0_id_seq2"'::"regclass");


--
-- TOC entry 2910 (class 2604 OID 16799)
-- Name: milestones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "milestones" ALTER COLUMN "id" SET DEFAULT "nextval"('"milestones_id_seq"'::"regclass");


--
-- TOC entry 2912 (class 2604 OID 25745)
-- Name: phases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "phases" ALTER COLUMN "id" SET DEFAULT "nextval"('"phases_id_seq"'::"regclass");


--
-- TOC entry 2913 (class 2604 OID 16821)
-- Name: portfolio_projects id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "portfolio_projects" ALTER COLUMN "id" SET DEFAULT "nextval"('"portfolio_projects_id_seq"'::"regclass");


--
-- TOC entry 2914 (class 2604 OID 16825)
-- Name: portfolios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "portfolios" ALTER COLUMN "id" SET DEFAULT "nextval"('"portfolios_id_seq"'::"regclass");


--
-- TOC entry 2922 (class 2606 OID 16869)
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "activities"
    ADD CONSTRAINT "activities_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2924 (class 2606 OID 16871)
-- Name: activity_data activity_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "activity_data"
    ADD CONSTRAINT "activity_data_pkey" PRIMARY KEY ("id", "activity_id");


--
-- TOC entry 2926 (class 2606 OID 16873)
-- Name: bundle_phases bundle_phases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "bundle_phases"
    ADD CONSTRAINT "bundle_phases_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2928 (class 2606 OID 16875)
-- Name: bundles bundle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "bundles"
    ADD CONSTRAINT "bundle_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2932 (class 2606 OID 16879)
-- Name: contractors contractors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "contractors"
    ADD CONSTRAINT "contractors_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2938 (class 2606 OID 16885)
-- Name: incidents incidents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incidents"
    ADD CONSTRAINT "incidents_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2952 (class 2606 OID 16899)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "locations"
    ADD CONSTRAINT "locations_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2954 (class 2606 OID 16901)
-- Name: milestones milestones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "milestones"
    ADD CONSTRAINT "milestones_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2966 (class 2606 OID 16913)
-- Name: units new_table_0_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "units"
    ADD CONSTRAINT "new_table_0_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2930 (class 2606 OID 16877)
-- Name: change_orders new_table_0_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "change_orders"
    ADD CONSTRAINT "new_table_0_pkey1" PRIMARY KEY ("id");


--
-- TOC entry 2968 (class 2606 OID 16915)
-- Name: variance_reasons new_table_0_pkey10; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "variance_reasons"
    ADD CONSTRAINT "new_table_0_pkey10" PRIMARY KEY ("id");


--
-- TOC entry 2936 (class 2606 OID 16883)
-- Name: incident_types new_table_0_pkey11; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incident_types"
    ADD CONSTRAINT "new_table_0_pkey11" PRIMARY KEY ("id");


--
-- TOC entry 2934 (class 2606 OID 16881)
-- Name: incident_classes new_table_0_pkey12; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "incident_classes"
    ADD CONSTRAINT "new_table_0_pkey12" PRIMARY KEY ("id");


--
-- TOC entry 2962 (class 2606 OID 16909)
-- Name: procurements new_table_0_pkey2; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "procurements"
    ADD CONSTRAINT "new_table_0_pkey2" PRIMARY KEY ("id");


--
-- TOC entry 2942 (class 2606 OID 16889)
-- Name: installations new_table_0_pkey3; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "installations"
    ADD CONSTRAINT "new_table_0_pkey3" PRIMARY KEY ("id");


--
-- TOC entry 2956 (class 2606 OID 16903)
-- Name: ncrs new_table_0_pkey4; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "ncrs"
    ADD CONSTRAINT "new_table_0_pkey4" PRIMARY KEY ("id");


--
-- TOC entry 2972 (class 2606 OID 16919)
-- Name: weightings new_table_0_pkey6; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "weightings"
    ADD CONSTRAINT "new_table_0_pkey6" PRIMARY KEY ("id");


--
-- TOC entry 2948 (class 2606 OID 16895)
-- Name: issues new_table_0_pkey8; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "issues"
    ADD CONSTRAINT "new_table_0_pkey8" PRIMARY KEY ("id");


--
-- TOC entry 2970 (class 2606 OID 16917)
-- Name: variances new_table_0_pkey9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "variances"
    ADD CONSTRAINT "new_table_0_pkey9" PRIMARY KEY ("id");


--
-- TOC entry 2946 (class 2606 OID 16893)
-- Name: issue_statuses new_table_1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "issue_statuses"
    ADD CONSTRAINT "new_table_1_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2940 (class 2606 OID 16887)
-- Name: indirect_costs pk_indirect_costs_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "indirect_costs"
    ADD CONSTRAINT "pk_indirect_costs_id" PRIMARY KEY ("id");


--
-- TOC entry 2944 (class 2606 OID 16891)
-- Name: invoices pk_invoices_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "invoices"
    ADD CONSTRAINT "pk_invoices_id" PRIMARY KEY ("id");


--
-- TOC entry 2950 (class 2606 OID 16897)
-- Name: items pk_items_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "items"
    ADD CONSTRAINT "pk_items_id" PRIMARY KEY ("id");


--
-- TOC entry 2958 (class 2606 OID 16905)
-- Name: portfolio_projects portfolio_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "portfolio_projects"
    ADD CONSTRAINT "portfolio_projects_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2960 (class 2606 OID 16907)
-- Name: portfolios portfolios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "portfolios"
    ADD CONSTRAINT "portfolios_pkey" PRIMARY KEY ("id");


--
-- TOC entry 2964 (class 2606 OID 16911)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "projects"
    ADD CONSTRAINT "projects_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3102 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA "public" TO PUBLIC;

-- Prep file_storage
INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Structural', NULL);
INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Baseline', NULL);
INSERT INTO public.file_storage (load_type, filename) VALUES ( 'Production', NULL);


-- Completed on 2018-03-08 19:24:58

--
-- PostgreSQL database dump complete
--


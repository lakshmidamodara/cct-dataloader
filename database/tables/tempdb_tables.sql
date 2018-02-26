--Create schema to hold temp tables. 
--These tables will be placeholders for data transfer
--from files to main tables

drop schema if exists temp
create schema temp

-- ----------------------------
-- Table structure for units
-- ----------------------------
DROP TABLE IF EXISTS "temp"."units";
CREATE TABLE "temp"."units" (
 "name" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for contractors
-- ----------------------------
DROP TABLE IF EXISTS "temp"."contractors";
CREATE TABLE "temp"."contractors" (
  "id" integer,
  "name" text COLLATE "pg_catalog"."default",
  "email" text COLLATE "pg_catalog"."default",
  "phone" text COLLATE "pg_catalog"."default",
  "pm_contact" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS "temp"."projects";
CREATE TABLE "temp"."projects" (
  "id" integer,
  "name" text COLLATE "pg_catalog"."default",
  "start" date,
  "end" date,
  "workdays" json,
  "budget" int4,
  "bundle_title" text COLLATE "pg_catalog"."default",
  "location_name" text COLLATE "pg_catalog"."default",
  "contingency" int8
)
;

-- ----------------------------
-- Table structure for activites
-- ----------------------------
DROP TABLE IF EXISTS "temp"."activities";
CREATE TABLE "temp"."activities" (
  "id" integer,
  "name" text COLLATE "pg_catalog"."default",
  "contractor_name" text COLLATE "pg_catalog"."default",
  "contractor_id" integer,
  "unit_cost" float8,
  "total_planned_hours" int4,
  "project_name" text COLLATE "pg_catalog"."default",
  "project_id" integer, 
  "total_planned_units" int8,
  "planned_start" date,
  "planned_end" date,
  "unit_name" text COLLATE "pg_catalog"."default",
  "actual_start" date,
  "actual_end" date,
  "hourly_cost" float8,
  "required_activities" int4[]
)
;

-- ----------------------------
-- Table structure for activity_data
-- ----------------------------
DROP TABLE IF EXISTS "temp"."activity_data";
CREATE TABLE "temp"."activity_data" (
  "id" integer,
  "activity_id" integer
  "activity_name" text COLLATE "pg_catalog"."default",
  "date" date,
  "actual_hours" int4,
  "actual_units" int4,
  "planned_hours" int8,
  "planned_units" float8,
  "updated" timestamp(6),
  "created" timestamp(6)
)
;

------- This to be created in public schema

DROP TABLE IF EXISTS "file_storage";
CREATE TABLE "file_storage" (
  "load_type" text COLLATE "pg_catalog"."default",
  "filename" text COLLATE "pg_catalog"."default",
  "filedata" bytea,
  "updated" timestamp(6)
)
;

insert into file_storage (load_type, filename) values ( 'Structural', 'struct.xlsx')
insert into file_storage (load_type, filename) values ( 'Baseline', 'baseline.xlsx')
insert into file_storage (load_type, filename) values ( 'Production', 'prod.xlsx')



--
-- Name: units; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE units (
    id integer DEFAULT nextval(('public.units_id_seq'::text)::regclass) NOT NULL,
    name text
);


--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE units_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;

	
	
--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('units_id_seq', 1, true);


--
-- Name: phases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE phases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
	
--
-- Name: phases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('phases_id_seq', 1, true);

ALTER TABLE ONLY phases ALTER COLUMN id SET DEFAULT nextval('phases_id_seq'::regclass);

-- Change the date cols from text to date type 

CREATE TABLE phases (
    id integer DEFAULT nextval(('public.phases'::text)::regclass) NOT NULL,
    name text,
    scheduled_start date,
    scheduled_end date,
    actual_start date,
    actual_end date
);


ALTER TABLE phases ALTER COLUMN scheduled_end TYPE date using scheduled_end::date;
ALTER TABLE phases ALTER COLUMN actual_start TYPE date using actual_start::date;

alter table public.activities add column phase_id integer;



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
--  "id" int4 NOT NULL DEFAULT nextval(('public.projects_id_seq'::text)::regclass),
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
  "name" text COLLATE "pg_catalog"."default",
  "contractor_name" text COLLATE "pg_catalog"."default",
  "unit_cost" float8,
  "total_planned_hours" int4,
  "project_name" text COLLATE "pg_catalog"."default",
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

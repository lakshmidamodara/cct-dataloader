-----------------------------------------------------------
--- File Name      : activities_activity_data.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This view selects out data from project, activities and activity_data 
---                   
--- 
--- 
------------------------------------------------------------

DROP VIEW IF EXISTS activities_activity_data
CREATE VIEW activities_activity_data
AS

	SELECT proj.id as proj_id, proj.name as proj_name, proj.start as proj_start, 
           proj.end as proj_end, act.id as activity_id, act.name as activity_name, 
           act.unit_id, act.unit_name as unit_name, act.planned_start as activity_pl_start,
           act.planned_end as activity_pl_end, act.actual_start as activity_act_start, 
           act.actual_end as activity_act_end, act.contractor_id, 
           con.name as contractor_name, act_data.id as activity_data_id,
           act_data.date as activitiy_data_date, act_data.planned_hours as act_data_pl_hrs,
           act_data.planned_units as act_data_pl_units, 
           act_data.actual_hours as act_data_act_hrs,
           act_data.actual_units as act_data_act_units
    FROM activities as act
    FULL OUTER JOIN projects as proj on proj.id = act.project_id 
    LEFT OUTER JOIN contractors as con on con.id = act.contractor_id
    LEFT OUTER JOIN activity_data as act_data on act_data.activity_id = act.id;
    
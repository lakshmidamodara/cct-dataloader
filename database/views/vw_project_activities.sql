-----------------------------------------------------------
--- File Name      : project_activities.sql
--- Author Name    : Lakshmi Damodara
--- Creation Date  : 01/28/2018
--- Updated on     : 02/02/2018
--- Version        : 1.0
--- Description    : This view selects out project and activities data
---                   
--- 
--- 
------------------------------------------------------------


DROP VIEW IF EXISTS project_activities
CREATE VIEW project_activities
AS

	SELECT proj.id as proj_id, proj.name as proj_name, proj.start as proj_start, 
           proj.end as proj_end, loc.id as loc_id, loc.state as loc_state,
           act.id as activity_id, act.name as activity_name, act.unit_id,
           unit.name as unit_name, act.contractor_id, con.name as contractor_name,
           bact.id as bundle_id, bun.name as bundle_name, ph.id as phase_id, 
           ph.name as phase_name
    FROM activities as act
    FULL OUTER JOIN projects as proj on proj.id = act.project_id 
    LEFT OUTER JOIN locations as loc on loc.id = proj.location_id
    LEFT OUTER JOIN units as unit on unit.id = act.unit_id
    LEFT OUTER JOIN contractors as con on con.id = act.contractor_id
    LEFT OUTER JOIN bundle_activities as bact on bact.activity_id = act.id
    LEFT OUTER JOIN bundles as bun on bact.id = bun.id and proj.id = bun.project_id
    LEFT OUTER JOIN bundle_phases as bph on bph.id = bun.id 
    LEFT OUTER JOIN phases as ph on ph.id = bph.phase_id;
    

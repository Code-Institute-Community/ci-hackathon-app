SELECT
    users.id AS judge_id,
    users.slack_display_name AS judge_name,
    teams.id AS team_id,
    teams.display_name AS team_name,
    projects.id AS project_id,
    projects.display_name AS project_name,
    SUM(scores.score) AS score
FROM hackathon_hackprojectscore AS scores
INNER JOIN accounts_customuser AS users
ON users.id = scores.judge_id
INNER JOIN hackathon_hackteam AS teams
ON scores.project_id = teams.project_id
INNER JOIN hackathon_hackproject AS projects
ON scores.project_id = projects.id
INNER JOIN (
    SELECT 
        judge_id,
        project_id,
        COUNT(*) AS num_scores
    FROM hackathon_hackprojectscore
    GROUP BY judge_id, project_id
) AS judge_counts
ON scores.judge_id = judge_counts.judge_id
AND scores.project_id = judge_counts.project_id
WHERE teams.hackathon_id = %s
GROUP BY
    users.id,
    users.slack_display_name,
    teams.id,
    teams.display_name,
    projects.id,
    projects.display_name
ORDER BY teams.id, users.id;
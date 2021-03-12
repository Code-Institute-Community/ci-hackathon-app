from dateutil.parser import parse
from datetime import datetime

import pandas as pd
import numpy as np


def format_date(date_str):
    """ Try parsing your dates with strptime and fallback to dateutil.parser
    """
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    except ValueError:
        return parse(date_str)


def query_scores(hackathon_id):
    """ Runs a mysql query to extract all of the project scores per judge """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
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
        """, [hackathon_id])
        rows = cursor.fetchall()
        rows = [[desc[0] for desc in cursor.description]] + list(rows)
    return rows


def combine_name(name1, name2):
    """ Function used to combine team and project name """
    return f'{name1} ({name2})'


def create_judges_scores_table(scores, judges, teams):
    """ Creates a list of lists of each judges score per team, the total for 
    each team, excludes judges scores who have not scored all teams yet and
    creates a name column from team and project name
    
    Returns a dict that represents the headers and results table that will be
    displayed in the template """
    default_values = [0 for i in range(len(judges))]
    headers = ['team_name', 'project_name'] + judges
    rows = [[team, ''] + default_values for team in teams]
    scores_table = pd.DataFrame(rows, columns=headers)
    judges_scores_table = pd.DataFrame(scores[1:], columns=scores[0])
    judges_scores_table = judges_scores_table[['judge_name', 'team_name',
                                               'project_name', 'score']]
    pivoted_scores_table = pd.pivot_table(judges_scores_table, values='score',
                                          index=['team_name', 'project_name'],
                                          columns=['judge_name'],
                                          aggfunc=np.sum)

    pivoted_scores_table.reset_index(inplace=True)
    scores_table.update(pivoted_scores_table)

    # Calculate how many projects the judges have scored and set scores for
    # judges who have not scored all projects to 0 which will exclude their
    # scores from the overall
    scores_per_judge = dict(judges_scores_table.groupby('judge_name'
        ).count()['team_name'])
    judges_to_exclude = [judge for judge in judges
                     if (scores_per_judge.get(judge) or 0) < len(teams)]
    for j in judges_to_exclude:
        scores_table[j] = 0
    
    # Convert all scores to a numeric value
    for judge in judges:
        scores_table[judge] = scores_table[judge].apply(pd.to_numeric)
    # Adding a total column to sum each judges scores for each team
    # and sort by that column in descending order
    scores_table['Total'] = 0
    scores_table['Total'] = scores_table.sum(axis=1)
    scores_table.sort_values(by=['Total'], inplace=True, ascending=False)

    # Combine team_name and project_name in one column and drop the unneeded
    # extra columns
    scores_table.insert(
        0, 'Team / Project Name', 
        scores_table['team_name'].combine(scores_table['project_name'],
        combine_name))
    scores_table.drop(columns=['team_name', 'project_name'], inplace=True)

    return {
        'headers': list(scores_table.columns),
        'rows': scores_table.to_records(index=False).tolist()
    }

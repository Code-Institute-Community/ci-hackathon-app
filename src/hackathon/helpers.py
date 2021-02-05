from copy import deepcopy
from dateutil.parser import parse
from datetime import datetime

from django.db.models import Count


def create_team_judge_category_construct(teams, judges, categories):
    """ Creates the default scores data structure for the team and judge scores
    e.g.:
    {
        team_name: {
            team_name: 'Team',
            project_name: 'Project',
            scores: {
                judge_1: {
                    'Score Category 1': 1,
                    ...
                    'Score Category n': 1,
                    'Total': 2
                    'count_scores' False,
                },
                judge_n: {
                    ...
                }
            },
            total_score: 5
        }
    } """
    score_construct = {}
    default_score_categories = {
        category.category: 0
        for category
        in categories
    }
    default_score_categories['Total'] = 0
    default_score_categories['count_scores'] = False

    for team in teams:
        if not team.project:
            continue
        score_construct[team.display_name] = {
            'team_name': team.display_name,
            'project_name': team.project.display_name,
            'scores': {},
            'total_score': 0,
        }
        for judge in judges:
            score_construct[team.display_name]['scores'][
                judge.slack_display_name] = deepcopy(default_score_categories)
            
            
    return score_construct
    

def create_category_team_construct(teams, categories):
    """ Creates the default scores data structure for the team and category
    scores, e.g.:
    {
        category_1: {
            team_1: 0,
            team_n: 0
        },
        category_n: {
            team_1: 1,
            team_n: 0
        }
    } """
    score_construct = {}
    for category in categories:
        score_construct[category.category] = {}
        for team in teams:
            if team.project:
                score_construct[category.category][team.display_name] = 0
    return score_construct


def count_judges_scores(judges, projects, score_categories):
    """ Checks each judge if they submitted scores for each project and
    if their scores should be counted """
    judge_scores = {}
    for judge in judges:
        scores = judge.hackprojectscores.filter(project_id__in=projects)
        judge_scores[judge.slack_display_name] = (
            scores.count() == len(projects) * len(score_categories))
    return judge_scores


def format_date(date_str):
    """ Try parsing your dates with strptime and fallback to dateutil.parser
    """
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    except ValueError:
        return parse(date_str)

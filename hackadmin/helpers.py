from hackathon.models import HackProjectScore
from accounts.models import CustomUser as User

CSV_COLUMNS = [
    'recipient_first_name',
    'recipient_name',
    'recipient_email',
    'issue_date',
    'team',
    'project',
    'award',
    'award_ranking',
    'hackathon',
    'badge_type',
]


def extract_badges_for_hackathon(hackathon, issue_date, format='json'):
    """ Extracts a list of badges to award to participants """
    print("\n\n\nextract_badges_for_hackathon helper function CALLED\n\n\n")
    badges = {}
    awards = hackathon.awards.order_by('hack_award_category__ranking')
    participants = [
        {'participant': participant, 'team': team}
        for team in hackathon.teams.all()
        for participant in team.participants.all()]
    for award in awards:
        badge_key = f'place_{(award.hack_award_category.ranking)}'
        badges.setdefault(badge_key, [])
        if not award.winning_project:
            continue

        for participant in award.winning_project.hackteam.participants.all():
            badges[badge_key].append({
                'first_name': participant.first_name,
                'name': (participant.full_name
                         or participant.slack_display_name),
                'email': participant.email,
                'issue_date': issue_date,
                'team': award.winning_project.hackteam.display_name,
                'project': award.winning_project.display_name,
                'award': f'{award.hack_award_category.display_name}',
                'award_ranking': str(award.hack_award_category.ranking),
            })

    awardees = [p.get('email') for b in badges.values()
                for p in b]
    badges.setdefault('participants', [])
    for data in participants:
        participant = data.get('participant')
        team = data.get('team')
        participant_data = {
            'first_name': participant.first_name,
            'name': (participant.full_name or participant.slack_display_name),
            'email': participant.email,
            'issue_date': issue_date,
            'team': team.display_name,
            'project': team.project.display_name if team.project else '',
            'award': 'Participant',
            'award_ranking': 'n/a',
        }
        if participant_data.get('email') not in awardees:
            badges['participants'].append(participant_data)

    badges.setdefault('facilitators', [])
    for team in hackathon.teams.all():
        print("\n CRITICAL LINE RAN")
        print(f"{team.mentor.first_name=}")
        badges['facilitators'].append({
            'first_name': team.mentor.first_name,
            'name': team.mentor.full_name or team.mentor.slack_display_name,
            'email': team.mentor.email,
            'issue_date': issue_date,
            'team': team.display_name,
            'project': team.project.display_name if team.project else '',
            'award': 'Hackathon Facilitators',
            'award_ranking': 'n/a',
        })

    projects = [team.project for team in hackathon.teams.all()
                if team.project]
    judge_ids = HackProjectScore.objects.filter(
        project__in=projects).values_list('judge', flat=True).distinct()
    judges = [User.objects.get(id=judge) for judge in judge_ids]

    badges.setdefault('judges', [])
    for judge in judges:
        badges['judges'].append({
            'first_name': judge.first_name,
            'name': judge.full_name or judge.slack_display_name,
            'email': judge.email,
            'issue_date': issue_date,
            'team': '',
            'project': '',
            'award': 'Hackathon Judge',
            'award_ranking': 'n/a',
        })

    if format == 'json':
        return badges

    badges_csv = ','.join(CSV_COLUMNS) + '\n'
    for badge_category, badge_recipients in badges.items():
        for badge_recipient in badge_recipients:
            recipient = ','.join(list(badge_recipient.values()))
            recipient += f',{hackathon.display_name}'
            recipient += f',{badge_category}\n'
            badges_csv += recipient

    return badges_csv

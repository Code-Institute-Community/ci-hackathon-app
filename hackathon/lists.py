"""
List of stauts types to be passed into dropdown of same name for each
user selection.
"""
STATUS_TYPES_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('registration_open', 'Registration Open'),
    ('hack_in_progress', 'Hackathon In Progress'),
    ('judging', 'Judging'),
    ('finished', 'Hackathon Finished'),
    ('deleted', 'Deleted'),
)

JUDGING_STATUS_CHOICES = (
    ('not_yet_started', "Hasn't started"),
    ('open', "Open"),
    ('closed', "Closed"),
)

AWARD_CATEGORIES = ['Best Project', 'Best Project (1st Runners Up)', 
                    'Best Project (2nd Runners Up)', 'Most Innovative Project',
                    'Best Commercial Application', 'Most Creative Project']

"""
List of user types to be passed into dropdown of same name for each
user selection.
"""
import pytz

USER_TYPES_CHOICES = (
    ('', 'Select Post Category'),
    ('participant', 'Participant'),
    ('mentor', 'Mentor'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
)

"""
List of CI LMS modules to be passed into dropdown of same name for each
user selection.
"""
LMS_MODULES_CHOICES = (
    ('', 'Select Learning Stage'),
    ('no_coding_experience', 'No coding experience'),
    ('just_starting', 'Just starting the course'),
    ('mid_course', 'In the middle of the course'),
    ('end_course', 'At the end of the course'),
    ('graduated', 'Graduated'),
    ('dev_duties',
        'Working with some development duties'),
    ('working_dev', 'Working as a developer'),
    ('guest_judge', 'Guest judge'),
    ('guest_facilitator', 'Guest facilitator'),
    ('staff', 'Staff'),
)

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

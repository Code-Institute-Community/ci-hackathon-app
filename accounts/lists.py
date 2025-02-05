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

"""
List of CI courses to be passed into dropdown of same name for each
user selection.
"""
LMS_COURSE_CHOICES = (
    ('', 'Select Current Course'),
    ('L3', 'The Level 3 Diploma in Software Development (L3)'),
    ('5P', 'The 5 project Diploma in Software Development Course (5P)'),
    ('4P', 'The 4 project Diploma in Software Development Course (4P)'),
    ('FSBC', 'The 16 Week Full Stack Developer Bootcamp (BC)'),
    ('DATABC', 'The 16 Week Data-Analytics Bootcamp (DBC)'),
)

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

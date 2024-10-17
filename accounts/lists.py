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

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]


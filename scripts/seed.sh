echo "============================"
echo "Seeding fixtures"
echo "============================"
python3 manage.py loaddata organisation
python3 manage.py loaddata accounts
python3 manage.py loaddata resources
python3 manage.py loaddata profiles
python3 manage.py loaddata emailaddresses
python3 manage.py loaddata hackathons
python3 manage.py loaddata showcase
python3 manage.py loaddata showcase_site_settings
python3 manage.py loaddata reviews
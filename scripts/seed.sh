echo "============================"
echo "Seeding fixtures"
echo "============================"
python3 manage.py loaddata organisation
python3 manage.py loaddata accounts
python3 manage.py loaddata resources
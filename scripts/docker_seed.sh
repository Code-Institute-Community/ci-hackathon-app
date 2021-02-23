echo "============================"
echo "Seeding fixtures"
echo "============================"
docker-compose exec hackathon-app python3 manage.py loaddata organisation
docker-compose exec hackathon-app python3 manage.py loaddata accounts
docker-compose exec hackathon-app python3 manage.py loaddata resources
docker-compose exec hackathon-app python3 manage.py loaddata profiles
docker-compose exec hackathon-app python3 manage.py loaddata emailaddresses
docker-compose exec hackathon-app python3 manage.py loaddata hackathons
docker-compose exec hackathon-app python3 manage.py loaddata showcase

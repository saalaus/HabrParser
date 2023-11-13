## HabrParser
Habr hub parser with django admin, celery, redis

### Run locally
1. Rename `.env.example` to `.env` and put your data
2. Buid `container docker-compose build`
3. Run: `docker-compose up web`
4. Go to http://localhost:8000/admin 
5. Default superuser credentinals: admin admin
6. Add hub to database
7. You can observe the parsing steps in the console or in the Articles model 
# todo-docker
Steps to run the docker container
1. Run the following command to build the docker container
    docker-compose build
2. Run the following command to run the docker container
    docker-compose up
3. Run the following command to make migrations
    docker-compose run web python manage.py makemigrations
4. Run the following command to migrate the database
    docker-compose run web python manage.py migrate

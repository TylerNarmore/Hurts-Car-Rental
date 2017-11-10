# Hurts-Car-Rental
Software Architecture and Design Project

#### Starting Development Environment
- In terminal go to directory Dockerfile is located.
- Run `docker-compose up`
- In browser go to `http://0.0.0.0:5000/`
- Able to edit code, to see changes run `docker-compose up` again
- When done run `docker-compose stop && docker-compose down --volumes`

#### Deploying New Version of App
-Create a new version of the app, with # being replace with version number
>`docker build -t gcr.io/hurts-car-rental/hurts:v#`
-Push image to Google Container Registry
>`gcloud docker --push gcr.io/hurts-car-rental/hurts:v#`
-Apply a rolling update to the existing deployment with an image update
>`kubectl set image deployment/hurts-web hurts-web=gcr.io/hurts-car-rental/hurts:v#`

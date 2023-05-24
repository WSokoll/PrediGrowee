# PrediGrowee
The secure educational web application to assess facial growth based on cephalometric images.

# Table of Contents
- [About Project](#about-project)
- [App functionality](#app-functionality)
- [Endpoints](#endpoints)
- [Database](#database)
- [Configuration](#configuration)
  - [Configuration files](#configuration-files)
  - [Database init file](#database-init-file)
  - [Folder with cephalometric photos](#folder-with-cephalometric-photos)
- [Deployment](#deployment)
  - [Testing locally](#testing-locally)
  - [Installation of the necessary software](#installation-of-the-necessary-software)
  - [Application image](#application-image)
  - [File structure](#file-structure)
  - [Deploying application on the 80 port via HTTP](#deploying-application-on-the-80-port-via-http)
  - [Getting and setting up certificates](#getting-and-setting-up-certificates)
  - [Deploying application on the 443 port via HTTPS](#deploying-application-on-the-443-port-via-https)
  - [Recaptcha and Google OAuth 2.0 reconfiguration](#recaptcha-and-google-oauth-20-reconfiguration)
  - [Changes and fixes - maintenance after deployment](#changes-and-fixes---maintenance-after-deployment)
- [Technology stack](#technology-stack)

## About Project
...

## App functionality
...

## Endpoints
...

## Database
...

## Configuration

### Configuration files
For the application to work properly, a `config.local.py` file should be created in the *local* folder. Then contents of
the *app/config.default.py* file should be copied to the newly created file and appropriate values should be changed.
You can see a list of the most important variables, whose values should be set, below.  

| Variable name          | Description                                                                                                                                                                                                                                                                                               |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SECRET_KEY             | A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application. It should be a long random bytes or str. See [Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/config/) for more details.   |
 | ORT_FOLDER_PATH        | Absolute path to the folder containing cephalometric photos ([See more](#folder-with-cephalometric-photos)). Should match the volume set in the *docker-compose.prod.yaml* (or *docker-compose.dev.yaml*) file during deployment (testing).                                                               |
| CONTACT_EMAIL          | Email displayed on the "Contact" subpage                                                                                                                                                                                                                                                                  |
| ADMIN_EMAIL_1          | Email for the first admin account, which will be automatically set up before first request                                                                                                                                                                                                                |
| ADMIN_PASSWORD_1       | Default password for the first admin account                                                                                                                                                                                                                                                              |
| ADMIN_EMAIL_2          | Email for the second admin account, which will be automatically set up before first request                                                                                                                                                                                                               |
| ADMIN_PASSWORD_2       | Default password for the second admin account                                                                                                                                                                                                                                                             |
| DB_HOST                | MySQL database host, should be set up to `db` during deployment.                                                                                                                                                                                                                                          |
| DB_PORT                | MySQL database port, default value: `3306`                                                                                                                                                                                                                                                                |
| DB_NAME                | Name of the MySQL database. Should match the database name set up in the *database-init.sql* file during deployment ([See more](#database-init-file)).                                                                                                                                                    |
| DB_USER                | MySQL username, should be set to `root` during deployment (this can be changed, but requires changes in the *database-init.sql* file)                                                                                                                                                                     |
| DB_PASSWORD            | MySQL password, should match the value set in the MYSQL_ROOT_PASSWORD and the DB_PASS environment variables located in the *docker-compose.prod.yaml* (or *docker-compose.dev.yaml*) file during deployment (testing).                                                                                    |
| RECAPTCHA_PUBLIC_KEY   | Can be generated via [https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)                                                                                                                                                                                       |
| RECAPTCHA_PRIVATE_KEY  | Can be generated via [https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)                                                                                                                                                                                       |
| SECURITY_PASSWORD_SALT | Specifies the HMAC salt. This is required for all schemes that are configured for double hashing. A good salt can be generated using: `secrets.SystemRandom().getrandbits(128)`. [Flask-Security Documentation](https://flask-security-too.readthedocs.io/en/stable/configuration.html) for more details. |
| MAIL_SERVER            | Default `localhost`. Currently using `smtp.gmail.com` is not possible, as Google has blocked third party apps from accesing an account using just username and password.                                                                                                                                  |
| MAIL_PORT              | Default `25`                                                                                                                                                                                                                                                                                              |
| MAIL_USERNAME          | Username - email, which will be used to send security emails (account registration, password change, etc.) and results to the users.                                                                                                                                                                      |
| MAIL_PASSWORD          | Email password.                                                                                                                                                                                                                                                                                           |
| MAIL_DEFAULT_SENDER    | Can be set the same as MAIL_USERNAME                                                                                                                                                                                                                                                                      |
| GOOGLE_CLIENT_ID       | Google OAuth 2.0 client ID                                                                                                                                                                                                                                                                                |
| GOOGLE_CLIENT_SECRET   | Google OAuth 2.0 client secret                                                                                                                                                                                                                                                                            |

### Database init file
Before the deployment process, the `database-init.sql` file should be created in the *db* folder. This file should
contain SQL scripts responsible for database creation, tables creation and population of some tables with the values, 
which won't be changed. Details about the database can be found in the [Database section](#database). During deployment
this file will be used to initialize mysql container.

### Folder with cephalometric photos
By *folder with cephalometric photos* is meant the *photos* folder. Inside there should be folders containing 
cephalometric photos, to which paths can be found in the *path* column of the *ort_data* table.


## Deployment
App was meant to run under Linux Ubuntu 22.04 virtual machine. Compatability with other systems and versions is not
guaranteed.

### Testing locally
You can test the app before setting it up on the production server, for example on your local virtual machine,
by using *docker-compose.dev.yaml* file. This allows to skip the app image building process and NGINX configuration.
All You need is Docker Compose installed on the machine (See more about installation [HERE](#docker-compose)) and
following project folders and files copied to the one folder (later referred to as *main folder*): *app folder*,
*db folder*, *dump folder*, *local folder*, *photos folder*, *docker-compose.dev.yaml file*. Be sure to set up
appropriate access settings for the *dump* folder (Read more [HERE](#files-and-folders-on-the-server)). To start the 
containers navigate to Your *main folder* and run the command:
```
sudo docker-compose up --detach --build
```

### Installation of the necessary software

#### Docker Compose
Instructions can be found here: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)  
After following instructions above, there might be a need to also run a command:
```
sudo apt install docker-compose
```

#### ACME Shell script
Script used to issue the free certificates. Installation instructions can be found here: 
[https://github.com/acmesh-official/get.acme.sh](https://github.com/acmesh-official/get.acme.sh)

### Application image
Recommended way of building and then using the application image is to build it locally, save it to the .tar file
(which can also be compressed if needed), send it to the server and load it there. This way You can avoid having to 
copy the application code to the production server. It is even better to use an image repository, but this may lead to
additional costs.  
Building an image (should be executed from the main folder containing the *app* folder and the *local* folder):
```
docker build -t predigrowee:v1 .
```
Saving the image to a .tar file:
```
docker save predigrowee:v1 -o predigroweeImage.tar
```
Loading the image:
```
docker load --input predigroweeImage.tar
```
Rebuilding the image in case of any changes in the code (requires changes to the image tag in the
*docker-compose.prod.yaml* file, re-saving and re-loading image on the server):
```
docker build --no-cache -t predigrowee:v2 .
```

### File structure
Initial file structure on the server should look like:
```
TBD
```

For the db-backup container to work properly You have to change the owner of the *dump* folder:
```
sudo chown 1005 ./dump
```

### Deploying application on the 80 port via HTTP

### Getting and setting up certificates
```
acme.sh --issue -d www.predigrowee.agh.edu.pl -d predigrowee.agh.edu.pl -w /app/nginx/data --server letsencrypt
```

### Deploying application on the 443 port via HTTPS

### Recaptcha and Google OAuth 2.0 reconfiguration

### Changes and fixes - maintenance after deployment

Restart single service (app in this example) - good for small changes in the code: `sudo docker-compose restart app`  
Rebuild single service (app in this example) - if for example new dependencies needed: `sudo docker-compose up --detach --build app`

## Technology stack

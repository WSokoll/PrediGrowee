# <img src="https://github.com/WSokoll/PrediGrowee/blob/main/app/static/img/logo.png" width="40" height="40"/> Predigrowee
This project was part of the engineering thesis, which was focused on creating and deploying the secure educational
web application to assess facial growth based on cephalometric images called **Predigrowee**.

## Technology stack

### Backend
 - **Framework:** Flask
 - **WSGI Server:** Gunicorn
 - **Database:** MySQL

### Frontend
 - **Templating Engine:** Jinja2
 - **Technologies:** HTML5, JavaScript, CSS

### Deployment
 - **Containerization:** Docker
 - **Orchestration:** Docker Compose
 - **Reverse Proxy:** Nginx

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
*Folder with cephalometric photos* refers to the *photos* folder. Inside there should be folders containing 
cephalometric photos, to which paths can be found in the *path* column of the *ort_data* table within the database.


## Deployment
App was meant to run under Linux Ubuntu 22.04 virtual machine. Compatability with other systems and versions is not
guaranteed.

### Testing locally
You can test the app before setting it up on the production server, for example on your local virtual machine,
by using *docker-compose.dev.yaml* file. This allows to skip the app image building process and NGINX configuration.
All You need is Docker Compose installed on the machine (See more about installation [HERE](#docker-compose)) and
following project folders and files copied to the one folder (later referred to as *main folder*): *app folder*,
*db folder*, *dump folder*, *local folder*, *photos folder*, *docker-compose.dev.yaml file*. Be sure to set up
appropriate access settings for the *dump* folder (Read more [HERE](#file-structure)). To start the 
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
docker build -t application:v1 .
```
Saving the image to a .tar file:
```
docker save application:v1 -o applicationImage.tar
```
Loading the image:
```
docker load --input applicationImage.tar
```
Rebuilding the image in case of any changes in the code (requires changes to the image tag in the
*docker-compose.prod.yaml* file, re-saving and re-loading image on the server):
```
docker build --no-cache -t application:v2 .
```

### File structure
Initial file structure on the server should look like:
```
app
├── docker-compose.yaml
├── nginx
    ├── Dockerfile
    ├── nginx.conf
    ├── data
    └── certs
├── db
    └── database-init.sql
├── dump     
└── photos
```
For the db-backup container to work properly You have to change the owner of the *dump* folder:
```
sudo chown 1005 ./dump
```

### Deploying application on port 80 via HTTP
In order to obtain SSL/TLS certificate it is necessary to first deploy the application using HTTP protocol. To achieve
that *nginx.dev.conf* should be used (You should rename it temporarily to `nginx.conf` or change the *nginx/Dockerfile* 
accordingly). *nginx.dev.conf* file contains proxy configuration for the app (which is exposed on port 80) along 
with the configuration for the ACME challenge (needed in order to obtain the certificate in the next step).  
After making the changes described above, You can deploy your application (build and start all containers) using the
command:
```
sudo docker-compose up --detach
```
* docker-compose.yaml should correspond to the *docker-compose.prod.yaml* file. If You don't want to rename it, or You
have multiple files with different configurations You can run the command with specified .yaml file:
```
sudo docker-compose up -f docker-compose.prod.yaml --detach
```
Execution of the above instructions should result in a working application on port 80.

### Getting and setting up certificates
Before proceeding please make sure that the instructions above have been followed and the application is running on port 80.
Also ensure that you have a registered domain name and that it is correctly connected to the public IP address of the 
server (meaning entering the domain name into a web browser allows users to access the app). The command below uses
acme.sh and Let's Encrypt to generate a certificate for the *www.exampledomainname.com* and the *exampledomainname.com* 
domain. Note that `-w` flag points to the folder from which acme challenge will be served (same folder was mounted as 
the volume of the nginx service inside docker-compose.yaml configuration file and is accessed and served by nginx proxy 
configured in the nginx.conf file).
```
acme.sh --issue -d www.exampledomainname.com -d exampledomainname.com -w /app/nginx/data --server letsencrypt
```
After generating certificate, resulting files should be copied or moved to the *app/nginx/certs* folder, especially 
`fullchain.cer` file and `.key` file.

### Deploying application on the 443 port via HTTPS
Before proceeding with this step, please ensure that You have completed the instructions provided above.  Then replace
the currently used *nginx.conf* file (*nginx.dev.conf*) with the proper *nginx.conf* file, containing setup for 443 ssl 
port. You can restart nginx service by running the command provided below:
```
sudo docker-compose up --detach --build nginx
```

### Changes and fixes - maintenance after deployment

Deploying any changes in the application code requires three steps:
 - creating and uploading to the server new image of the application with bumped tag or changed name
 - updating the *docker-compose.yaml* file - updating the name of the application image
 - rebuilding app container by running `sudo docker-compose up --detach --build app`

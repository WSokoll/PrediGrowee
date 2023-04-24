# PrediGrowee
The secure educational web application to assess facial growth based on cephalometric images.

# Table of Contents
- [About Project](#about-project)
- [App functionality](#app-functionality)
- [Endpoints](#endpoints)
- [Deployment](#deployment)
  - [Configuration](#configuration)
    - [Configuration file](#configuration-file)
    - [Database init file](#database-init-file)
    - [Folder with cephalometric images](#folder-with-cephalometric-images)
  - [Deploy and run with Docker Compose](#deploy-and-run-with-docker-compose)
- [Technology stack](#technology-stack)

## About Project

## App functionality

## Endpoints

## Deployment

### Configuration
#### Configuration file
#### Database init file
#### Folder with cephalometric images

### Deploy and run with Docker Compose
Please make sure you have followed all the steps in the [Configuration](#Configuration) section, before proceeding with
the instructions below.  
Build containers: `sudo docker-compose build`  
Start containers: `sudo docker-compose up --detach`  
Stop containers: `sudo docker-compose down`
Restart single service (app in this example) - good for small changes in the code: `sudo docker-compose restart app`  
Rebuild single service (app in this example) - if for example new dependencies needed: `sudo docker-compose up --detach --build app`

## Technology stack

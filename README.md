# Tech-Assesment-Customers-API

## Description

This project is a RESTful API that allows users to manage customers in a banking system.

## Contents

- [Tech-Assesment-Customers-API](#tech-assesment-customers-api)
  - [Description](#description)
  - [Contents](#contents)
  - [Project Setup and Installation](#project-setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Deploy AWS RDS](#2-deploy-aws-rds)
    - [3. Set Up the Environment Variables](#3-set-up-the-environment-variables)
    - [4. Build and Run the Containers](#4-build-and-run-the-containers)
    - [5. Local runnning](#5-local-runnning)
  - [API REST Documentation](#api-rest-documentation)
  - [Testing Instructions](#testing-instructions)

## Project Setup and Installation

### Prerequisites

Before you begin, ensure that you have the following tools installed on your machine:

- **Git**: To clone the repository.
- **Docker**: To build and run containers.
- **Docker Compose**: To manage multiple containers.
- **Python**: To check and use the local environment if needed.
- **AWS CLI**: To deploy the RDS instance.

### 1. Clone the Repository

First, you need to clone this repository to your local machine. Open a terminal and run the following command:

```bash
git clone https://github.com/Daniel-Ortiz1210/Banking-System-Customers-API.git
cd <Banking-System-Customers-API>
```

### 2. Deploy AWS RDS

To deploy the AWS RDS, you need to execute the following command:

First you need to verify that you have the AWS CLI installed on your machine. You can check this by running the following command:

```bash
aws --version
```

If you don't have the AWS CLI installed, you can follow the instructions in the following link: [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

Once you have the AWS CLI installed, you need to configure the AWS CLI with your credentials. You can do this by running the following command:

```bash
aws configure
```

Set up AWS CLI with the following information:

**IMPORTANT**: Configure the AWS CLI with the credentials that have the necessary permissions to deploy the RDS instance.
You can use the credentials provided in the email with the submission of the challenge.

Once you have the AWS CLI configured, you can deploy the RDS instance by running the following command:

```bash
aws cloudformation create-stack --stack-name RDSStack --template-body file://cloudformation.yml --capabilities CAPABILITY_NAMED_IAM
```

You can check the status of the stack creation by running the following command:

```bash
aws cloudformation describe-stacks --stack-name RDSStack
```

Once the stack is created, you can check the outputs of the stack by running the following command:

```bash
aws cloudformation describe-stacks --stack-name RDSStack --query 'Stacks[0].Outputs'
```

You will get the following output:

```bash
[
    {
        "OutputKey": "RDSInstanceEndpoint",
        "OutputValue": "databaseinfo.rds.amazonaws.com"
        "Description": "The endpoint of the publicly accessible RDS instance"
    }
]
```

**You need to copy the `OutputValue` of the `RDSInstanceEndpoint` key and set it as the `DATABASE_HOST` environment variable in the `.env.dev` file.**

### 3. Set Up the Environment Variables

Create a `.env.dev` file in the root directory of the project and copy the content from the file attached in the email.
If you don't have the file, you can create it manually with the following content:

```bash
APP_NAME='[Tech Assessment] Banking System Customers API'
HOST='0.0.0.0'
PORT=3000
DATABASE_HOST='RDSInstanceEndpoint' # Set the value of the RDSInstanceEndpoint output (previous step)
DATABASE_PORT=3306
DATABASE_USER='admin'
DATABASE_PASSWORD='Xcvi762gsnoanAswrabzn'
DATABASE_NAME='customers'
TOKEN_SECRET_KEY='XWPxvcaou37va213cp0xml'
TOKEN_ALGORITHM='HS256'
TOKEN_EXPIRATION_IN_MINUTES=2
```

### 4. Build and Run the Containers

To build and run the containers, you need to execute the following command (You need to have Docker and Docker Compose installed and AWS RDS deployed):

```bash
docker-compose up --build -d
```

This command will build the Docker images and run the containers in detached mode.

### 5. Local runnning

To run the API locally, you need to run the following commands (You need to have AWS RDs deployed):

Create a virtual environment:

```bash
python3 -m venv .env
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
python3 main.py
```

## API REST Documentation

Once the containers are up and running, you can access the API documentation using your browser.
The API documentation is available at the following URL:

```bash
http://0.0.0.0:3000/docs
```

**Note**: The API documentation is generated using Swagger UI.

## Testing Instructions

To run the tests, you need to execute the following command:

If you are running the API locally:

```bash
pytest
```

If you are running the API using Docker:

```bash
docker-compose exec app pytest
```

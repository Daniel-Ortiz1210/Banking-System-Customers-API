# Tech-Assesment-Customers-API

## Description

This is a simple API that allows you to manage customers. You can create, read, update and delete customers.
The API is built using Python, FastAPI and SQLAlchemy.

## Contents

- [Tech-Assesment-Customers-API](#tech-assesment-customers-api)
  - [Description](#description)
  - [Contents](#contents)
  - [Project Setup and Installation](#project-setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up the Environment Variables](#2-set-up-the-environment-variables)
  - [3. Build and Run the Containers](#3-build-and-run-the-containers)
  - [API REST Documentation](#api-rest-documentation)
  - [Arquitecture and Design](#arquitecture-and-design)
  - [Testing Instructions](#testing-instructions)

## Project Setup and Installation

## Prerequisites

Before you begin, ensure that you have the following tools installed on your machine:

- **Git**: To clone the repository.
- **Docker**: To build and run containers.
- **Docker Compose**: To manage multiple containers.
- **Python**: To check and use the local environment if needed.

## 1. Clone the Repository

First, you need to clone this repository to your local machine. Open a terminal and run the following command:

```bash
git clone https://github.com/Daniel-Ortiz1210/Banking-System-Customers-API.git
cd <Banking-System-Customers-API>
```

## 2. Set Up the Environment Variables

Create a `.env.dev` file in the root directory of the project and copy the content from the file attached in the email.
If you don't have the file, you can create it manually with the following content:

```bash
APP_NAME='[Tech Assessment] Banking System Customers API'
HOST='0.0.0.0'
PORT=3000
DATABASE_HOST='localhost'
DATABASE_PORT=5432
DATABASE_USER='postgres'
DATABASE_PASSWORD='postgres'
DATABASE_NAME='customers'
TOKEN_SECRET_KEY='XWPxvcaou37va213cp0xml'
TOKEN_ALGORITHM='HS256'
TOKEN_EXPIRATION_IN_MINUTES=2
```

## 3. Build and Run the Containers

To build and run the containers, you need to execute the following command:

```bash
docker-compose up --build
```

## API REST Documentation

The API documentation is available at the following URL:

```bash
http://localhost:3000/docs
```

**Note**: The API documentation is generated using Swagger UI.

## Arquitecture and Design

## Testing Instructions

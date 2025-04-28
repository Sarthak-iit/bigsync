
# BigSync
This software is my undergoing final year B.Tech. project.
It uses the algorithm developed in paper "**A Novel Event Detection and Classification Scheme Using Wide-Area Frequency Measurements**" to detect and classify events.

## Tech-stack

 1. Frontend : **React.js**
 2. Backend : 
 -- **Python** for implementing algorithms discussed in the paper 
-- Two different servers :  one is a **fastAPI** server and is using **node.js** and child processes module for making python child process.
-- **fastAPI** server is preferred.

## Prerequisites for installing

Before you begin, make sure you have the following software installed on your system:
- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (Comes with Node.js)
- [fastAPI](https://fastapi.tiangolo.com/)

> If fastAPI not installed install it by `pip install fastapi`

## Backend (FastAPI) Setup

### Navigate to the fastAPI backend directory

    cd  python-backend
### Install backend dependencies
	pip3 install -r requirements.txt

### Start the backend server
	python server.py


## Backend (Node.js) Setup

### Navigate to the Node.js backend directory

    cd  node_backend
### Install backend dependencies
	npm  install
	pip  install  numpy

### Start the backend server
	npm  start

  

  

## Frontend setup
### Navigate to react frontend directory
	cd  app

### To use development server
- #### Install frontend dependencies
		 npm  install
- #### Start the React development server
		 npm  start

>The react app will be accessible at http://localhost:3000
### To serve production build server
Installing serve package

    npm i -S serve
Serving the build folder using npx

	npx serve -s build


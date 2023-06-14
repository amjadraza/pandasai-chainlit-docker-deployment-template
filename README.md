<h1 align="center">
📖 PandasAI-Chainlit-Docker-Deployment App Template
</h1>

![UI](ui.PNG?raw=true)


## 🔧 Features

- Basic Skeleton App configured with `openai` API
- A ChatBot using PandasAI and Chainlit
- Docker Support with Optimisation Cache etc
- Deployment on Google Cloud App Engine
- Deployment on Google Cloud using `Cloud Run`

> Reference repository: https://github.com/amjadraza/langchain-chainlit-docker-template

This repo contains an `main.py` file which has a template for a chatbot talking to CSV implementation.

## Adding your chain
To add your chain, you need to change the `load_chain` function in `main.py`.
Depending on the type of your chain, you may also need to change the inputs/outputs that occur later on.


## 💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/amjadraza/pandasai-chainlit-docker-deployment-template
```

2. Install dependencies with [Poetry](https://python-poetry.org/) and activate virtual environment🔨

```bash
poetry install
poetry shell
```

3. Run the Chainlit server🚀

```bash
chainlit run demo_app/main.py
```

Run App using Docker
--------------------
This project includes `Dockerfile` to run the app in Docker container. In order to optimise the Docker Image
size and building time with cache techniques, I have follow tricks in below Article 
https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

Build the docker container

``docker  build . -t pandasai-chainlit-chat-app:latest``

To generate Image with `DOCKER_BUILDKIT`, follow below command

```DOCKER_BUILDKIT=1 docker build --target=runtime . -t pandasai-chainlit-chat-app:latest```

1. Run the docker container directly 

``docker run -d --name pandasai-chainlit-chat-app -p 8000:8000 pandasai-chainlit-chat-app ``

2. Run the docker container using docker-compose (Recommended)

``docker-compose up``


Deploy App on Google App Engine
--------------------------------
This app can be deployed on Google App Engine following below steps.

## Prerequisites

Follow below guide on basic Instructions.
[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

We added below tow configurations files 

1. `app.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

I have adopted `Dockerfile` to deploy the app on GCP APP Engine.

1. Initialise & Configure the App

``gcloud app create --project=[YOUR_PROJECT_ID]``

2. Deploy the App using

``gcloud app deploy``

3. Access the App using 

https://pandasai-chat-app-dpy4wfgkcq-ts.a.run.app/


Deploy App on Google Cloud using Cloud Run (RECOMMENDED)
--------------------------------------------------------
This app can be deployed on Google Cloud using Cloud Run following below steps.

## Prerequisites

Follow below guide on basic Instructions.
[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

We added below tow configurations files 

1. `cloudbuild.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

we are going to use `Dockerfile` to deploy the app using Google Cloud Run.

1. Initialise & Configure the Google Project using Command Prompt

`gcloud app create --project=[YOUR_PROJECT_ID]`

or set the project

`gcloud config set pandasai-app`

Set the Region if not done before

`gcloud config set compute/region australia-southeast1`


2. Enable Services for the Project

```
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. Create Service Account

```
gcloud iam service-accounts create pandasai-app-cr \
    --display-name="pandasai-app-cr"

gcloud projects add-iam-policy-binding pandasai-app \
    --member="serviceAccount:pandasai-app-cr@pandasai-app.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding pandasai-app \
    --member="serviceAccount:pandasai-app-cr@pandasai-app.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding pandasai-app \
    --member="serviceAccount:pandasai-app-cr@pandasai-app.iam.gserviceaccount.com" \
    --role="roles/run.admin"
``` 

4. Generate the Docker

`DOCKER_BUILDKIT=1 docker build --target=runtime . -t australia-southeast1-docker.pkg.dev/pandasai-app/pai-app/pandasai-chainlit-chat-app:latest`

5. Push Image to Google Artifact's Registry

Create the repository with name `pai-app`

```
gcloud artifacts repositories create pai-app \
    --repository-format=docker \
    --location=australia-southeast1 \
    --description="A PandasAI Chainlit App" \
    --async
```

Configure-docker 

`gcloud auth configure-docker australia-southeast1-docker.pkg.dev`

In order to push the `docker-image` to Artifact registry, first create app in the region of choice. 

Check the artifacts locations

`gcloud artifacts locations list`



Once ready, let us push the image to location

`docker push australia-southeast1-docker.pkg.dev/pandasai-app/pai-app/pandasai-chainlit-chat-app:latest`

6. Deploy using Cloud Run

Once image is pushed to Google Cloud Artifacts Registry. Let us deploy the image.

```
gcloud run deploy pandasai-chat-app --image=australia-southeast1-docker.pkg.dev/pandasai-app/pai-app/pandasai-chainlit-chat-app:latest \
    --region=australia-southeast1 \
    --service-account=pandasai-app-cr@pandasai-app.iam.gserviceaccount.com \
    --port=8000
```

7. Test the App Yourself

You can try the app using below link 

https://pandasai-chat-app-dpy4wfgkcq-ts.a.run.app/


## Report Feedbacks

As `pandasai-chainlit-docker-deployment-template` is a template project with minimal example. Report issues if you face any. 

## DISCLAIMER

This is a template App, when using with openai_api key, you will be charged a nominal fee depending
on number of prompts etc.
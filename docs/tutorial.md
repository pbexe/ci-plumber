## Gitlab + Openshift

???+ tip "A tip for the CLI prompts"
    When you run the CLI, you will be prompted for information. When there is text in square brackets, this is the default. This information is often based off previous information you have entered. If you leave the prompt blank, this will be used.

    eg:
    ```console
    $ ci-plumber azure create-db
    Name [my-database-779171168]:

    // If you leave that prompt blank, the value "my-database-779171168" will be used
    ```

### Initialise Gitlab

First we need to initialise the project. All of the commands can either be run interactively or using the CLI options. For this tutorial we shall be using the interactive mode.

```console
$ ci-plumber gitlab init
Gitlab url [git.cardiff.ac.uk]: <The URL to your gitlab instance>
Username: <Your username>
Email: <Your email>
Access token: <Your access token>
Docker registry url [registry.git.cf.ac.uk]: <The URL to your docker registry>
Getting remote
[12:41:23] Logging in to Gitlab
           Getting projects
[12:41:24] Matching remote with Gitlab projects
           Found project: Flask Demo
           Generating .gitlab-ci.yml
           Generating Dockerfile
           Gitlab configured!
```

This command will do several things:

1. It will ask you for the gitlab url, username, email and access token. These will be stored in order to authenticate against Gitlab.
2. It will also ask you for the docker registry url. This is the url that other plugins such as Openshift will be able to pull images from.
3. It will then try to find the project that you are working on on Gitlab.
4. It will then Genrate the .gitlab-ci.yml file and the Dockerfile if approprate for the project.

### Push changes to Gitlab

We next need to push our changes to Gitlab so that Gitlab CI will run the new configuration:

```console
// Stage the changes

$ git add .


// Commit the changes

$ git commit -m "Add .gitlab-ci.yml and Dockerfile"


// Create a new tag to trigger the pipeline

$ git tag -a v0.0.1 -m "Release v0.0.1"


// Push the changes to Gitlab

$ git push --follow-tags
```

### Deploy to Openshift

Once Gitlab is set up, we can set up the Openshift project. Openshift should pick up on the credentials left by `ci-plumber gitlab init`. We can deploy the app to Openshift using the following command:

```console
$ ci-plumber openshift deploy
Project: <A name unique to your project>
Username [c1769331]: <Your username. The default should be yours>
Password: <You won't be able to see what you're typing here. It's not broken.>
Repeat for confirmation:
[13:08:46] Logginginto GitLab
           Getting the Gitlab project
[13:08:47] Loggin in to Openshift
[13:08:49] Creating a new project
[13:08:52] Creating secrets
[13:09:11] Importing image-stream
[13:09:13] Creating a new app
[13:09:16] Exposing the service
[13:09:18] Here are the details
[13:09:20] <The details as well as the URL will be written here>
```

!!! note
    For the Cardiff University Openshift, make sure that you are on the university network. You can then log in to Openshift using `openshift.cs.cf.ac.uk` as your login URL.

### Deploy a Database

To deploy a database as well, you can use the following command:
```console
$ ci-plumber openshift create-db
Mysql password:
Mysql root password:
[13:19:28] Creating database config
           Creating MariaDB pod from openshift/mariadb-persistent template
[13:19:31] Exposing DB
[13:19:33] Getting DNS
[13:19:36] Writing config to maria.env


// You can now find the credentials in maria.env

$ cat maria.env

ADMIN_PASSWORD=<Your password>
USER=maria_user
PASSWORD=<Your password>
NAME=mariadb
HOST=<The database DNS>
```

## Gitlab + Azure

### Initialise Gitlab

To deploy to Azure, we shall use a different architecture for the project. We will begin in a similar manner to the Gitlab + Openshift section:

```console
$ ci-plumber gitlab init
Gitlab url [git.cardiff.ac.uk]: <The URL to your gitlab instance>
Username: <Your username>
Email: <Your email>
Access token: <Your access token>
Docker registry url [registry.git.cf.ac.uk]: <The URL to your docker registry>
Getting remote
[12:41:23] Logging in to Gitlab
           Getting projects
[12:41:24] Matching remote with Gitlab projects
           Found project: Flask Demo
           Generating .gitlab-ci.yml
           Generating Dockerfile
           Gitlab configured!
```

### Create a new Container Registry

This will create Gitlab credentials similarly to before. However, we will now be using Azure instead of Gitlab to store the images. We must begin by creating a new Azure container registry:

```console
$ ci-plumber azure create-registry
Registry name [registry887130626]:
Resource group name [myResourceGroup]: sub1
[16:00:16] Creating resource group sub1
[16:00:24] Creating registry registry887130626
[16:00:40] Enabling admin user
[16:00:43] Getting admin credentials
[16:00:46] Logging in to Gitlab
           Gettingthe Gitlab project
           Creating Azure access keys in CI
           Azure access keys already exist in Gitlab CI for c1769331/flask-demo
[16:00:47] Creating .gitlab-ci.yml


// Stage the changes

$ git add .


// Commit the changes

$ git commit -m "Add .gitlab-ci.yml and Dockerfile"


// Create a new tag to trigger the pipeline

$ git tag -a v0.0.1 -m "Release v0.0.1"


// Push the changes to Gitlab

$ git push
```

### Deploy our App to Azure

We have now instantiated a new Azure container registry, pointed Gitlab CI to push new images to the registry, and triggered a build which should push the new image to the registry.

Next, we need to deploy the app to Azure. We will use the following command:

```console
$ ci-plumber azure deploy
Service plan [myServicePlan]:
App name [myApp-159731108]:
[16:08:33] Creating app service plan
[16:08:43] Creating web app. This may take a while...
[16:09:20] Assigning managed identity
[16:09:28] Retrieving subscription ID
[16:09:31] Granting permission to access container registry
[16:09:42] Configuring app to use managed identity
[16:09:47] Deploying
[16:09:56] Deployed to https://myapp-159731108.azurewebsites.net
           It may take a moment to come online
```

As can be seen, the app is now deployed to Azure.

### Deploy a Database

We might also want to deploy a database for the project. We can use the following command:

```console
$ ci-plumber azure create-db
Name [my-database-779171168]:
Admin username [myadmin]:
Admin password:
Repeat for confirmation:
[16:12:32] Initialising Server. This may take a while...
[16:15:41] Created Database
           The credentials have been written to maria.env
```

Similarly to the Openshift example, the details of the database are written to `maria.env`. This file uses standard syntax for environment variables, so it can be easily loaded using whatever method you prefer. For example, [dotenv](https://saurabh-kumar.com/python-dotenv/) in Python.

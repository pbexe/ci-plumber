## Gitlab + Openshift

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

Once Gitlab is set up, we can set up the Openshift project. Openshift should pick up on the credentials left by `ci-plumber gitlab init`. We can deploy the app to Openshift using the following command:

```console
// Make sure you are logged in to Openshift

$ oc login <Your Openshift URL> -u <Your Openshift username>


// Then you can deploy the app to Openshift

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

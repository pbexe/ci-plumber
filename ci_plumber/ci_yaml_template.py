# flake8: noqa

template: str = r"""default:
  tags:
    #- comsc-ci
    - general-docker

variables:
  GIT_STRATEGY: clone

stages:
- build

build:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:debug
    entrypoint: [""]
  script:
    - mkdir -p /kaniko/.docker
    - echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json
    - /kaniko/executor --context $CI_PROJECT_DIR --dockerfile $CI_PROJECT_DIR/Dockerfile --destination $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG --destination $CI_REGISTRY_IMAGE:latest
  rules:
    - if: $CI_COMMIT_TAG
"""

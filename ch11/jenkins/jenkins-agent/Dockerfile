FROM gcr.io/kaniko-project/executor:v1.13.0 as kaniko
FROM jenkins/inbound-agent
COPY --from=kaniko /kaniko /kaniko
WORKDIR /kaniko
USER root

FROM jenkins/jenkins
USER jenkins
ENV CASC_JENKINS_CONFIG /usr/local/casc.yaml
COPY casc.yaml /usr/local/casc.yaml
RUN jenkins-plugin-cli --plugins configuration-as-code matrix-auth ssh-slaves email-ext mailer slack htmlpublisher greenballs simple-theme-plugin kubernetes git github

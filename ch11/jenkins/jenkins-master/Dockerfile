FROM jenkins/jenkins
USER jenkins
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml
COPY casc.yaml /var/jenkins_home/casc.yaml
COPY mdo-posts.groovy /usr/local/mdo-posts.groovy
RUN jenkins-plugin-cli --plugins ssh-slaves email-ext mailer slack htmlpublisher greenballs simple-theme-plugin kubernetes git github

#!/bin/sh
sudo useradd -m ansible
echo 'ansible ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers
sudo su - ansible << EOF
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
printf "${admin_password}\n${admin_password}" | sudo passwd ansible
EOF

#SwitchDin coding test

## Requirements

- Docker
- Docker compose
- Python
- Ansible
- AWS CLI

Refer to `requirements.txt` for python dependencies

## How to run in dev

`docker-compose up`

Alternatively, build and run Dockerfile (for rabbitmq), then run all three python scripts seperately

## How to deploy

1. Add VM ip address to ansible hosts
2. `ansible-playbook playbook.yml`

## Creating a VM automatically with ansible

`ansible-playbook create-instances.yml` will do this, but need access key to my AWS account for it to work.

## How to view output

SSH into VM (username is ec2-user)
Run `cd ~/src & docker-compose logs -f display`

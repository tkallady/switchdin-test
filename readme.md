# SwitchDin coding test

## Requirements

- Docker
- Docker compose
- Python
- Ansible
- AWS CLI

Refer to `requirements.txt` for python dependencies

## Project structure

There are three main python scripts

- `rn_generator.py` - generates the random numbers and sends them to broker
- `rn_processor.py` - processes the numbers and calculates averages
- `rn_display.py` - prints out the results to console as they are updated

The MQTT broker is RabbitMQ, defined in `Dockerfile`

## How to run in dev

Run `docker-compose up -d`
and then
`docker-compose logs -f display` to view output.
Note it can take a few minutes for logs to come through.

Alternatively, build and run Dockerfile (for rabbitmq), then run all three python scripts seperately. In this case need to update BROKER_HOSTNAME in config.ini to localhost.

## How to deploy

1. Add VM ip address to ansible hosts `/etc/ansible/hosts`
2. Run `ansible-playbook playbook.yml`

## Creating a VM automatically with ansible

Running `ansible-playbook create-instances.yml` will do this, but need access key to my AWS account for it to work.

## How to view output

SSH into VM (username is ec2-user)
Run `cd ~/src && docker-compose logs -f display`

# NanoPoker - Play Poker with Nano
## Overview
NanoPoker utilies [Nano On Tap](https://github.com/silverstar194/NanoOnTap) to create a flow state system modeling a poker game.
If you're unfamilar with [Nano On Tap](https://github.com/silverstar194/NanoOnTap) I suggest reading the [Nano On Tap Overview](https://github.com/silverstar194/NanoOnTap) before continuing.

## Production **RECOMMENDED**
### Prerequisites
* Docker
* [Nano Node](https://docs.nano.org/running-a-node/node-setup/)
* [PoW Provider](https://nanocenter.org/projects/dpow)
* [Hardware and NanoOnTap Setup](https://github.com/silverstar194/NanoPoker/wiki)

### Docker usage 
The provided production/example stack is dockerized and includes:
* gunicorn (dg01 container)
* nginx (ng01 container)
* postgres (ps01 container)

The dockerized setup is meant to be used as a quickly deployable sample.

#### Setup
1. Clone NanoPoker repo
```sh
git clone https://github.com/silverstar194/NanoOnTap.git
```
2. Create and start containers. Database will be created and initalized automatically.
```sd
docker-compose build && docker-compose up -d
```
3. Check everything deployed. Go to http://localhost:8001/admin/. You should see a login screen.
![Login Screen](https://i.imgur.com/kP3uT3i.png)
4. Create Django superuser
```sh
docker exec -it $(docker inspect --format="{{.Id}}" dg02) python /NanoPoker/manage.py createsuperuser
```
5. Import Nano Poker JSON template by sending a POST request `POST action/template/import` including the JSON in `poker_template.json` as the request bobdy. This imports and defines the Poker flow state.

6. Restart the docker container to bootstrap the Nano Wallet and Nano Accounts from Nano Node. This automaticlly creates a new wallet and needed accounts on the Node.

## Wiki
Please see wiki for more [information and guides.](https://github.com/silverstar194/NanoPoker/wiki)

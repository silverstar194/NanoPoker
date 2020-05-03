# NanoPoker - Play Poker with Nano
## Overview
NanoPoker utilies [Nano On Tap](https://github.com/silverstar194/NanoOnTap) to create a flow state system modeling a poker game.
If you're unfamilar with [Nano On Tap](https://github.com/silverstar194/NanoOnTap) I suggest reading the [Nano On Tap Overview](https://github.com/silverstar194/NanoOnTap) before continuing.

## Production **RECOMMENDED**
### Prerequisites
* Docker
* [Nano Node](https://docs.nano.org/running-a-node/node-setup/)
* [PoW Provider](https://nanocenter.org/projects/dpow) 

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
```
POST action/template/import
```
6. Restart the docker container to bootstrap the Nano Wallet and Nano Accounts from Nano Node. This automaticlly creates a new wallet and needed accounts on the Node.

## Flow State Definition
### Json Template

## Flow State Reprograming

## NFC Hardware Setup
See the Medium article for hardware setup. TODO

### Audrino
### NFC Stickers
### NFC Readers

### Bare Bones Architecture

### Sources
[Dumping NFC Tag Information](https://playground.arduino.cc/Learning/MFRC522/)

[MFRC-522 Circuit Layout](https://randomnerdtutorials.com/security-access-using-mfrc522-rfid-reader-with-arduino/)

### Shopping List
https://www.amazon.com/gp/product/B002KL8J8W/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1
https://www.amazon.com/gp/product/B0775XQXRB/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1
https://www.amazon.com/gp/product/B01IB7UOFE/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1
https://www.amazon.com/gp/product/B07WD326SN/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1

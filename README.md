<p align="center"><img src="https://github.com/avinashshenoy97/brownie-points/blob/master/extras/browniepoints_logo_black.png" alt="BrowniePoints Logo">

<h5 align="center"> A social currency turned into a crypto currency! </h5>

</p>


![Cryptocurrency](https://img.shields.io/badge/crypto-currency-gold.svg)
![Python Version](https://img.shields.io/badge/python-3.7-blue.svg)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
![OpenSource](https://img.shields.io/badge/open-source-brightgreen.svg)


## Setup

`cd` into the repository and:

```bash
pip3 install -r requirements.txt
```

Start the first node with the command:

```bash
python3 BrowniePoints -f <IP_OF_FIRST_NODE> 8000
```

where `8000` is the port number used by the _rendezvous server_ for the underlying peer-to-peer network.

New nodes can be started and added to the p2p network using:

```bash
python3 BrowniePoints -w <IP_OF_FIRST_NODE> 8000
```

Every node exposes a REST API for accessing information about the blockchain. This API listens on port `16000` by default. This can be changed with the `-p` flag.

All peers on the network listen on port `50500` for broadcasted messages.

## Usage

### User Interfaces

2 UIs are also provided with **BrowniePoints**. To start these, `cd` into `walletUI` or `explorerUI` and start the web server using:

```bash
python3 manage.py runserver 0.0.0.0:PORT
```

### Mining

Any node can be made to mine the transactions on the transactions pool by making an empty `PUT` request to `/control/mineBlock` to the node that should be credited with the reward.

An example **CURL** command:

```bash
curl --request PUT <IP_OF_NODE>:16000/control/mineBlock
```

When a valid block is mined, the node will be credited with 50 BrowniePoints and will proceed to broadcast the new block to all other nodes.


## License

[MIT License](https://github.com/avinashshenoy97/brownie-points/blob/master/LICENSE)


#### NOTE

##### This project was done as part of a course on "Software Engineering" at PES University.
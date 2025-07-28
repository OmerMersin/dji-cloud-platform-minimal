# DJI Cloud API Example

![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![MQTT](https://img.shields.io/badge/MQTT-1883-orange)

A minimal example demonstrating how to fetch OSD data from DJI drones via the DJI Cloud API, publish it over MQTT, and expose a FastAPI dashboard.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running EMQX (MQTT)](#running-emqx-mqtt)
7. [Usage](#usage)
8. [Sample Output](#sample-output)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)

---

## Overview

This project consists of two main components:

* **`mqtt_client.py`**: Connects to an MQTT broker, subscribes to DJI topics (`sys/#`, `thing/#`), parses JSON payloads, handles `update_topo` replies, and prints OSD telemetry.
* **`server.py`**: Starts the MQTT client in the background and launches a FastAPI server to serve a static dashboard and expose configuration/health endpoints.

---

## Features

* MQTT client with:

  * Automatic subscription to `sys/#` and `thing/#` topics.
  * Callbacks for status (`update_topo`) and OSD messages.
  * Clear logs prefixed with `[MQTT]` and `[OSD]`.
  * Retry logic for DNS/connect errors.
* FastAPI server with:

  * `/api/config` endpoint returning DJI & MQTT settings.
  * `/api/health` endpoint with server timestamp.
  * Static dashboard served at `/` from `public/dashboard.html`.
  * Global error handlers for 404 and 500.

---

## Prerequisites

* Python 3.9 or higher
* Docker (for local EMQX broker)
* Your PC and DJI Smart Controller on the same local network

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OmerMersin/dji-cloud-platform.git
   cd dji-cloud-platform
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Rename `.env.example` to `.env` and set the following variables:

```dotenv
DJI_APP_ID=<your_dji_app_id>
DJI_APP_KEY=<your_dji_app_key>
DJI_LICENSE=<your_dji_license>
HOST_ADDR=<your_broker_host_or_ip>
MQTT_USERNAME=<mqtt_username>
MQTT_PASSWORD=<mqtt_password>
```

*Note*: `HOST_ADDR` is used by `mqtt_client.py` to determine the broker address. The MQTT port defaults to `1883`.

---

## Running EMQX (MQTT)

To run a local EMQX broker via Docker:

```bash
docker run -d --name emqx \
  -p 1883:1883 \
  -p 8083:8083 \
  -p 8084:8084 \
  -p 8883:8883 \
  -p 18083:18083 \
  emqx:5.0.20
```

1. Open the management console: [http://localhost:18083/](http://localhost:18083/)
2. Default credentials: `admin` / `public`
3. (Optional) Create additional users.

---

## Usage

1. Ensure your DJI Smart Controller and PC are on the same network.
2. Run the server (which also starts the MQTT client):

   ```bash
   python server.py
   ```
3. Access the dashboard at: [http://localhost:3000/](http://localhost:3000/)
4. Fetch configuration: GET [http://localhost:3000/api/config](http://localhost:3000/api/config)
5. Check health: GET [http://localhost:3000/api/health](http://localhost:3000/api/health)

---

## Sample Output

```text
[MQTT] Connecting to localhost:1883 ...
[MQTT] Connected to localhost:1883 with result code 0
[MQTT] Subscribed to topics: sys/#, thing/#
[MQTT] Received message on topic: thing/product/<sn>/osd
[OSD] Lat: 0, Lon: 0, Height: 16.16, Head: 10.4, Pitch: -0.4, Roll: 0.2
[OSD] Additional data:
{ '61-0-0': { 'gimbal_pitch': 0, 'gimbal_yaw': 117.8, ... },
  'firmware_version': '03.31.0000',
  ... }
```

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make your changes and commit: `git commit -m 'Add new feature'`.
4. Push to your branch: `git push origin feature/your-feature`.
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contact

* **Author**: Omer Mersin ([omermersin02@gmail.com](omermersin02@gmail.com))
* **GitHub**: [https://github.com/OmerMersin/dji-cloud-platform](https://https://github.com/OmerMersin/dji-cloud-platform)

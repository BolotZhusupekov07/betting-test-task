Bet-Maker and Line-Provider Services
====================================

1.  **Line-Provider**: Provides information about events available for betting.

2.  **Bet-Maker**: Allows users to place bets on events fetched from the Line-Provider.


Line-Provider Service
---------------------

### Domain - http://localhost:8000/
### Docs - http://localhost:8000/docs

### Event Attributes:

*   **Event ID**: A unique string or number identifying the event.

*   **Coefficient**: Positive decimal with two digits of precision.

*   **Deadline**: A timestamp indicating the cutoff time for bets.

*   **Status**: One of the following:

    *   NEW
    *   FINISHED_WIN
    *   FINISHED_LOSE

### Features:

*   Events are stored in database (PostgreSQL).
*   APIs to create and update events dynamically.

Bet-Maker Service
-----------------


### Domain - http://localhost:5000/
### Docs - http://localhost:5000/docs

### Endpoints

#### **GET /events**

*   Fetches the list of active events from the Line-Provider Service.
*   Caches events for **3 seconds** to reduce load using Redis.
*   **Response**: A list of all active events.

#### **POST /bet**

*   Creates a new bet for a specified event.
*   **Request Body** (JSON):
    *   event\_id: Unique identifier of the event (UUID).
    *   amount: Positive decimal (two decimal places) indicating the bet amount.
*   **Validation**:
    *   Event validity is verified via request to the Line-Provider Service.
*   **Response**: A unique identifier for the created bet.

#### **GET /bets**

*   Returns a history of all bets, including:
    *   Bet ID
    *   Event ID
    *   Bet status:
        *   NEW
        *   WON
        *   LOST

*   **Response**: JSON array of bet details.


### Webhook from Line-Provider
*  Bets state are updated from Line-Provider webhook, when events state are updated.

### Data Storage

*   Information about bets is stored in PostgreSQL.

Deployment and Infrastructure
-----------------------------

*   Both services are built using **FastAPI** with **Python 3.12.3**.
*   Fully asynchronous operations ensure efficiency.
*   Services and associated infrastructure are **dockerized** and launched via **Docker Compose**.

Additional Notes
----------------

*   **Standards**: Adheres to PEP8, with type hints and thorough testing with unit tests.
*   **Enhancements**:
    *   Dynamic interaction between services.
    *   Support for caching and efficient validation.




## Info

Project Language: Python 3.12.3

Project Framework: FastAPI 0.110.1


### Running Server
```bash
docker compose up --build
```

### Running Tests in Bet-Maker
```bash

cd bet-maker/
docker compose -f docker-compose.unittest.yaml up --build --abort-on-container-exit


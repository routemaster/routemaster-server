# Setup

    $ virtualenv3 env
    $ env/bin/pip install -e .
    $ env/bin/server.py --debug /tmp/routemaster-db

# API

See routemaster/db.py for the definitions of the models.

## Sessions

The requests will contain a sessionId header which the server will validate and
use to determine how certain requests are handled.

## Fetching data

*   `GET /journey/<int:id>`

    Can return 403 if the **Journey** is not public.

*   `GET /place/<int:id>`

    Includes a list of high scoring journeys.

*   `GET /place/nearby/<float:latitude>,<float:longitude>`

*   `GET /route/<int:id>`

*   `GET /user/<int:id>`

*   `GET /user/<int:id>/journeys`

    Returns a list of the user's recent public **Journeys**.

## Storing data

*   `POST /journey` – store a recorded journey

    Required data:

        {
          "startTimeUtc": ...,
          "endTimeUtc": ...,
          "startPlaceId": ...,
          "endPlaceId": ...,
          "waypoints": [
            {
              "timeUtc": ...,
              "accuracyM": ...,
              "latitude": ...,
              "longitude": ...,
              "heightM": ...
            },
            ...
          ]
        }

*   `POST /user` – create a new user ?

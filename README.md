# Local setup

    $ virtualenv3 env
    $ env/bin/pip install -e .
    $ env/bin/debug-server.py /tmp/routemaster-db

# Deploying to routemaster.lumeh.org

Install Fabric on your system and run

    $ fab deploy

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

*   `GET /account/<int:id>`

*   `GET /account/<int:id>/journeys`

    Returns a list of the account's recent public **Journeys**.

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

*   `POST /account` – create a new account ?

# Scoring

The efficiency score is an integer from 0 to 100. We first calculate the
straight-line distance between the starting and ending locations. Then we
calculate the distance the user walked by summing the distances between adjacent
recorded waypoints. The efficiency score is then

    min(0, ceil(200 * (straight-line distance)^2 / (walked distance)^2 - 100))

The purpose of the min(0, (...) - 100) is to make it easier to get low scores.
Previously the formula was just (100 * ...), which meant you'd have to walk an
infinate distance in order to get a score of 0.

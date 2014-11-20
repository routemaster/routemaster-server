# Usage

## Local setup

    $ virtualenv3 env
    $ env/bin/pip install -e .
    $ env/bin/debug-server.py /tmp/routemaster-db

## Testing

    $ env/bin/python -m unittest

## Deploying to routemaster.lumeh.org

Install Fabric on your system and run

    $ fab deploy

# API

See routemaster/db.py for the definitions of the models. Accounts and journeys
are identified by random [UUIDs](https://docs.python.org/3/library/uuid.html),
with the exception of the test Account ("Hermann Dörkschneider"), whose id is
`test`.

## Sessions

The requests will contain an accountId header which the server will use to
determine how certain requests are handled.

## Fetching data

*   `GET /account/<uuid>`

*   `GET /account/<uuid>/recent`

    Returns a list of the account's recent public **Journeys**.

*   `GET /journey/<uuid>`

    Can return 403 if the **Journey** is not public.

*   `GET /route/<int:id>/top`

    Returns a list of the top-scoring journeys for the route.

*   `GET /route/<int:id>/recent`

    Returns a list of the most recent journeys for the route.

## Storing data

*   `POST /journey` – store a recorded journey

    Required data:

        {
          "id": ...,
          "visibility": ...,
          "startTimeUtc": ...,
          "stopTimeUtc": ...,
          "startPlaceId": ...,
          "stopPlaceId": ...,
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
straight-line distance between the starting and stopping locations. Then we
calculate the distance the user walked by summing the distances between adjacent
recorded waypoints. The efficiency score is then

    min(0, ceil(200 * (straight-line distance)^2 / (walked distance)^2 - 100))

The purpose of the min(0, (...) - 100) is to make it easier to get low scores.
Previously the formula was just (100 * ...), which meant you'd have to walk an
infinate distance in order to get a score of 0.

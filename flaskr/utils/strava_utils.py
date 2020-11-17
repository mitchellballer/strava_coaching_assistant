import configparser
from flaskr.db import get_db
from flask import flash, g


class print_stuff:

    # function that just prints current info about our athlete, state of tokens
    def print_current_state(athlete_id, bearer_token, bearer_token_expiration, refresh_token, strava_id):
        print("Printing current state")
        print(f"Athlete id: {athlete_id}")
        print(f"strava bearer token: {bearer_token}")
        print(f"strava bearer token expiration: {bearer_token_expiration}")
        print(f"strava refresh token: {refresh_token}")
        print(f"strava athlete id: {strava_id}")

    def hello_world():
        print("Hello world")
        flash("hello world!")


class db_utils:

    # save given activity to database for given athlete
    # only save activity if it doesn't already exist in the database
    # input is a single activity in json form provided by strava
    def save_activity(activity, athlete_id):
        title = activity['name']
        start = activity['start_date'].replace('T', ' ').replace('Z', '')
        description = 'sample description' #activity['description']
        distance = activity['distance']
        duration = activity['elapsed_time']
        strava_id = activity['id']
        db = get_db()
        error = None

        if not activity:
            error = 'no activity given'
        elif not strava_id:
            error = 'no strava activity id given'
        elif db.execute('SELECT id FROM activity WHERE id = ?', (strava_id,)).fetchone() is not None:
            error = 'activity ID: {} already exists in the database'.format(strava_id)

        if error is None:
            db.execute(
                'INSERT INTO activity (id, start_date, title, description, distance, duration, athlete_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (strava_id, start, title, description, distance, duration, athlete_id)
            )
            db.commit()
            return True
        else:
            flash(error)
            return False

    def check_prerequisites():
        # load client properties from config.properties
        config = configparser.ConfigParser()
        config_file = 'config.properties'
        config.read(config_file)
        id = config['CLIENT']['client_id']
        secret = config['CLIENT']['client_secret']
        # make sure we found client properties
        error = None

        if not id:
            error = 'No client id. Please load client ID into config.properties on the server'
        if not secret:
            error = 'No client secret. Please load client ID into config.properties on the server'
        if error is not None:
            flash(error)

        # load athlete properties from session
        athlete_id = g.athlete['id']
        bearer_token = g.athlete['strava_bearer_token']
        token_expiration = g.athlete['strava_bearer_token_expiration']
        refresh_token = g.athlete['strava_refresh_token']
        strava_id = g.athlete['strava_athlete_id']

        return id, secret, athlete_id, bearer_token, token_expiration, refresh_token, strava_id

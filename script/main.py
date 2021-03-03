"""
Copyright 2021 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""
from tool import log as _log
import requests, shelve, time, os
from itertools import count
from config import TOKEN, BASE_DIR
from datetime import datetime
log = _log("MAIN")

db = shelve.open( os.path.join( BASE_DIR, "data", "data.slv" ) )

url = "https://api-football-v1.p.rapidapi.com/v2/countries"
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': TOKEN
    }

def timeit(f):

    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        log.info("Time %s %s", str(te-ts), str(f))
        return result

    return timed

def get_live():
    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/live"
    response = requests.get( url, headers=headers )
    # [x["fixture_id"] for x in res if x["awayTeam"]["team_name"] == "FC Copenhagen"]
    return response.json()["api"]["fixtures"]


@timeit
def work():
    try:
        result = get_live()
    except Exception as e:
        result = []
        log.error("Error", exc_info=True)
    timestamp = datetime.now().timestamp().__int__()
    db[ str(timestamp) ] = result

def main():
    try:
        for c in count():
            if c % 100 == 0:
                db.__dict__["dict"].reorganize()
            work()
            time.sleep(60)
    finally:
        db.close()
        log.info("db close")

if __name__ == '__main__':
    main()

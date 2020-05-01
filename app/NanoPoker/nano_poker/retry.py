import time
import logging
import json


logger = logging.getLogger(__name__)


def retry_post(func, retries=5, pause=.1):
    res = None
    for i in range(retries):
        try:
            res = func()
            json.loads(res.text)

            if res.status_code != 200:
                raise Exception("Post failed")

            return res
        except Exception as e:
            logger.exception(res.text)
            logger.exception(e)
            if i < retries - 1: # i is zero indexed
                time.sleep(pause)
                pause = pause * 1.5
                continue
            else:
                raise

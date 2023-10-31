import logging

import uvicorn

logger = logging.getLogger(__name__)

def main(conf):
    logger.info(f"Starting {{ project_name }} server on http://{conf.host}:{str(conf.port)} (Press CTRL+C to quit)")
    uvicorn.run("app.server.routes:app", port=conf.port, host=conf.host, )
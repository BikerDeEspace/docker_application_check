import config as config
import os

gen = (name for name in config.DOCKER_COMPOSE_FILENAMES if os.path.exists(name))


print(next(gen))
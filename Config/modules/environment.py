import environ
from Config.basepath import *

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    env.read_env(env_file)
else:
    raise Exception("No local .env files found.")
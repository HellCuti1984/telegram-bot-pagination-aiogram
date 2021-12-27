from os import getenv
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')


CONTENT = []

min_index = 0
max_index = len(CONTENT) - 1

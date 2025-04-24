import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GCP_KEY = os.getenv("GCP_KEY")
CSE_ID = os.getenv("CSE_ID")

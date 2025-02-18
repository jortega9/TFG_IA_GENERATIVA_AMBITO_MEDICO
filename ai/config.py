import os
from dotenv import load_dotenv

class Config:
    
	load_dotenv()
 
	OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

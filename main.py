import sys
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    uvicorn.run(f'apps.{sys.argv[1]}.main:app', port=3000, host='0.0.0.0', reload=True)


from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import httpx

app = FastAPI()
#Now, let's initialize the MongoDB connection. Make sure you have MongoDB installed and running on your local machine,
#  or provide the appropriate connection details if your MongoDB instance is hosted elsewhere:



client = MongoClient('mongodb://localhost:27017/')
db = client['weather']
collection = db['weather_data']
#Next, we'll define a data model/schema using pydantic to represent the weather data we want
#  to store in MongoDB. In this example, we'll include fields like temperature, humidity, 
# and weather description. Feel free to adjust the schema based on the data provided by the weather API:



class WeatherData(BaseModel):
    temperature: float
    humidity: float
    description: str
#Now, let's create an endpoint 
# that interacts with the weather API to fetch weather data and store it in MongoDB:



@app.get('/weather')
async def get_weather(latitude: float, longitude: float):
    # Make a request to the weather API
    api_key = 'your-api-key'  # Replace with your actual API key
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}'
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant weather data
            temperature = data['current']['temp_c']
            humidity = data['current']['humidity']
            description = data['current']['condition']['text']
            
            # Create a WeatherData instance
            weather_data = WeatherData(
                temperature=temperature,
                humidity=humidity,
                description=description
            )
            
            # Store the weather data in MongoDB
            collection.insert_one(weather_data.dict())
            
            return weather_data
    except (httpx.HTTPError, KeyError):
        raise HTTPException(status_code=500, detail='Failed to fetch weather data')
    #In this example, we're using the WeatherAPI to retrieve weather data based on
    #  latitude and longitude. Replace 'your-api-key' with your actual API key.
    #Now, you can start the FastAPI application by running the following command:
        
    # (uvicorn app:app --reload)
        #You should see output indicating that the server is running. You can then access the API endpoint 
        # at http://localhost:8000/weather?latitude=<latitude>&longitude=<longitude>, replacing <latitude> and <longitude> 
        # with the desired coordinates. 
        # The weather data will be fetched from the API, stored in MongoDB, and returned as a response.
        #Please note that this is a basic example, and you might need to adapt it to suit your specific needs, 
        #such as adding authentication, handling different error scenarios, or customizing the data model/schema.
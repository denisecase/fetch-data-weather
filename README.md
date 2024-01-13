# fetch-data-weather

Fetch weather data

## Get an API Key

- Go to <https://openweathermap.org/api>. Sign up and get a free API key.
- Note the rate limits and adhere to them carefully or you could be charged.
- See [How to start use the One Call 3.0?](https://openweathermap.org/faq#onecall)

## Get Latitude and Longitude

- Given location, state, country code, find latitude and longitude at <https://openweathermap.org/api/geocoding-api>

## Project Virtual Environment

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

VS Code menu / View / Command Palette... / Python: Select Interpreter / .venv\Scripts\python.exe

## Run As a Script

```powershell
py -m fetch_data_weather
```

## See location.properties

```properties
location=Austin,TX,US
location01=Austin,TX,US
location02=Cupertino,CA,US
location03=Dublin,,IE
location04=Ely,NV,US
location05=Folsom,CA,US
location06=Kansas City,MO,US
location07=Maryville,MO,US
location08=Minneapolis,MN,US
location09=Olathe,KS,US
location10=Seattle,WA,US
location11=Spokane,WA,US
location12=Wichita,KS,US
```
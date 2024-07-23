from pydantic import BaseModel


class WeatherForecastResponseLocation(BaseModel):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


class WeatherForecastResponseCondition(BaseModel):
    text: str
    icon: str
    code: int


class WeatherForecastResponseCurrent(BaseModel):
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: float
    condition: WeatherForecastResponseCondition
    wind_mph: float
    wind_kph: float
    wind_degree: float
    wind_dir: str
    humidity: float
    cloud: int
    feelslike_c: float
    feelslike_f: float


class WeatherForecastResponse(BaseModel):
    location: WeatherForecastResponseLocation
    current: WeatherForecastResponseCurrent

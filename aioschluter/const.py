""" constants for aioschluter """

API_BASE_URL = "https://ditra-heat-e-wifi.schluter.com"
API_AUTH_URL = API_BASE_URL + "/api/authenticate/user"
API_GET_THERMOSTATS_URL = API_BASE_URL + "/api/thermostats"
API_SET_THERMOSTAT_URL = API_BASE_URL + "/api/thermostat"
API_APPLICATION_ID = 7
HTTP_UNAUTHORIZED: int = 401
HTTP_OK: int = 200
REGULATION_MODE_SCHEDULE = 1
REGULATION_MODE_MANUAL = 2
REGULATION_MODE_AWAY = 3

from production import *

# use production config, but with these changes:

TRANSPARENT_CLASSROOM_BASE_URL = "http://localhost:3000"

HUBS['CAMBRIDGE']['SURVEY_MONKEY_COLLECTOR_ID'] = '7CKNP7Y'
HUBS['SANDBOX']['SURVEY_MONKEY_COLLECTOR_ID'] = '7CKNP7Y'

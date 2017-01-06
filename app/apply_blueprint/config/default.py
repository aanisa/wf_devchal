import os

SURVEY_MONKEY_OAUTH_TOKEN=os.environ['SURVEY_MONKEY_OAUTH_TOKEN']

SURVEY_MONKEY_SURVEY_ID='111419034'
SURVEY_MONKEY_COLLECTOR_ID='FQDVNM3'

ANSWER_KEY = {
    'PARENTS': [
        {
            'FIRST_NAME': {'SURVEY_MONKEY': '69078793', 'TC': 'first_parent_name.first'}
            'LAST_NAME': {'SURVEY_MONKEY': '77425064', 'TC': 'first_parent_name.last'} ,
            'EMAIL': {'SURVEY_MONKEY': '69078871', 'TC': 'first_parent_email'},
            'PHONE': {'SURVEY_MONKEY': '69079428', 'TC': 'first_parent_mobile_number'},
            'ADDRESS': {'SURVEY_MONKEY': '69078976', 'TC': 'first_parent_address'}
        },
        {
            'FIRST_NAME': {'SURVEY_MONKEY': '69079990', 'TC': 'second_parent_name.first'},
            'LAST_NAME': {'SURVEY_MONKEY': '77425213', 'TC': 'second_parent_name.last'},
            'EMAIL': {'SURVEY_MONKEY': '69079992', 'TC': 'second_parent_email'},
            'PHONE': {'SURVEY_MONKEY': '69079993', 'TC': 'second_parent_mobile_number'},
            'ADDRESS': {'SURVEY_MONKEY': '69079994', 'TC': 'second_parent_address'}
        }
    ],
    'CHILD': {
        'FIRST_NAME': {'SURVEY_MONKEY': '69082546', 'TC': 'child_name.first'},
        'LAST_NAME': {'SURVEY_MONKEY': '77425286', 'TC': 'child_name.last'},
        'DOB': {'SURVEY_MONKEY': '69082734', 'TC': 'child_birth_date'},
        'GENDER': {'SURVEY_MONKEY': '69083456', 'TC': 'child_gender'}
    },
    'SCHOOLS': '69085210',
    'QUESTIONS': [
        {'SURVEY_MONKEY': '69092809', 'TC': 'how_hear'},
        {'SURVEY_MONKEY': '69092811', 'TC': 'caregivers'},
        {'SURVEY_MONKEY': '69092815', 'TC': 'siblings'},
        {'SURVEY_MONKEY': '69092816', 'TC': 'disposition'},
        {'SURVEY_MONKEY': '69092817', 'TC': 'social_style'},
        {'SURVEY_MONKEY': '69092820', 'TC': 'parenting_style'},
        {'SURVEY_MONKEY': '69092823', 'TC': 'typical_weekday'},
        {'SURVEY_MONKEY': '69092825', 'TC': 'typical_weekend'},
        {'SURVEY_MONKEY': '69092827', 'TC': 'ideal_school'},
        {'SURVEY_MONKEY': '69092836', 'TC': 'other_schools'},
        {'SURVEY_MONKEY': '69092837', 'TC': 'montessori'},
        {'SURVEY_MONKEY': '69092839', 'TC': 'what_age'},
        {'SURVEY_MONKEY': '69092840', 'TC': 'specialists'},
        {'SURVEY_MONKEY': '69092841', 'TC': 'involvement'},
        {'SURVEY_MONKEY': '69092842', 'TC': 'enrich'},
        {'SURVEY_MONKEY': '69092843', 'TC': 'anything_else'}
    ]
}

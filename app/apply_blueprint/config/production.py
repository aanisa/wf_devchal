import os
import re

TRANSPARENT_CLASSROOM_BASE_URL = "https://www.transparentclassroom.com"

SURVEY_MONKEY_OAUTH_TOKEN=os.environ['SURVEY_MONKEY_OAUTH_TOKEN']

phone_valid = lambda p: not p or re.match('^\D*(\d\D*){6,}$', p) != None

HUBS = {
    'CAMBRIDGE': {
        'TRANSPARENT_CLASSROOM_API_TOKEN': os.environ['TRANSPARENT_CLASSROOM_API_TOKEN_CAMBRIDGE'],
        'SURVEY_MONKEY_SURVEY_ID': '113377045',
        'SURVEY_MONKEY_COLLECTOR_ID': '7CRLTCY',
        'ANSWER_KEY': {
            'PARENTS': [
                {
                    'FIRST_NAME': {'SURVEY_MONKEY': "83225144", 'TRANSPARENT_CLASSROOM': 'first_parent_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "83225148", 'TRANSPARENT_CLASSROOM': 'first_parent_name.last'} ,
                    'EMAIL': {'SURVEY_MONKEY': "83225145", 'TRANSPARENT_CLASSROOM': 'first_parent_email'}, # Validated at SurveyMonkey
                    'PHONE': {'SURVEY_MONKEY': "83225147", 'TRANSPARENT_CLASSROOM': 'first_parent_mobile_number', 'VALIDATOR': phone_valid},
                    'ADDRESS': {'SURVEY_MONKEY': "83225146", 'TRANSPARENT_CLASSROOM': 'first_parent_address'}
                },
                {
                    'FIRST_NAME': {'SURVEY_MONKEY': "83225149", 'TRANSPARENT_CLASSROOM': 'second_parent_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "83225153", 'TRANSPARENT_CLASSROOM': 'second_parent_name.last'},
                    'EMAIL': {'SURVEY_MONKEY': "83225150", 'TRANSPARENT_CLASSROOM': 'second_parent_email'}, # Validated at SurveyMonkey
                    'PHONE': {'SURVEY_MONKEY': "83225151", 'TRANSPARENT_CLASSROOM': 'second_parent_mobile_number', 'VALIDATOR': phone_valid},
                    'ADDRESS': {'SURVEY_MONKEY': "83225152", 'TRANSPARENT_CLASSROOM': 'second_parent_address'}
                }
            ],
            'QUESTIONS': [
                # Parent/Guardian page questions
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'how_hear'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'caregivers'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'how_many_children_how_old'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'parenting_style'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'typical_weekday'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'typical_weekend'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'ideal_school'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'montessori'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'what_age'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'involvement'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'enrich'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'anything_else_family'},
                # Members in household pages questions
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'members_in_household'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'},
                {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}
            ],
            'CHILDREN': [
                {
                    'FIRST_NAME': {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': ''},
                    'QUESTIONS': [
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': '', 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                }
            ]
        }
    }
}

HUBS['SANDBOX'] = HUBS['CAMBRIDGE']

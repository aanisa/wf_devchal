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
        'MAPPING': {
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
            'ANSWERS': [
                # Parent/Guardian page questions
                {'SURVEY_MONKEY': "83225159", 'TRANSPARENT_CLASSROOM': 'how_hear'},
                {'SURVEY_MONKEY': "83225160", 'TRANSPARENT_CLASSROOM': 'caregivers'},
                {'SURVEY_MONKEY': "83233417", 'TRANSPARENT_CLASSROOM': 'how_many_children_how_old'},
                {'SURVEY_MONKEY': "83225164", 'TRANSPARENT_CLASSROOM': 'parenting_style'},
                {'SURVEY_MONKEY': "83225165", 'TRANSPARENT_CLASSROOM': 'typical_weekday'},
                {'SURVEY_MONKEY': "83225166", 'TRANSPARENT_CLASSROOM': 'typical_weekend'},
                {'SURVEY_MONKEY': "83225167", 'TRANSPARENT_CLASSROOM': 'ideal_school'},
                {'SURVEY_MONKEY': "83225169", 'TRANSPARENT_CLASSROOM': 'montessori'},
                {'SURVEY_MONKEY': "83225170", 'TRANSPARENT_CLASSROOM': 'what_age'},
                {'SURVEY_MONKEY': "83225172", 'TRANSPARENT_CLASSROOM': 'involvement'},
                {'SURVEY_MONKEY': "83225173", 'TRANSPARENT_CLASSROOM': 'enrich'},
                {'SURVEY_MONKEY': "83230265", 'TRANSPARENT_CLASSROOM': 'anything_else_family'},
                # Members in household pages questions
                {'SURVEY_MONKEY': "83225197", 'TRANSPARENT_CLASSROOM': 'members_in_household'},
                {'SURVEY_MONKEY': "83225179", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 2 member household
                {'SURVEY_MONKEY': "83225181", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 3
                {'SURVEY_MONKEY': "83225183", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 4
                {'SURVEY_MONKEY': "83225185", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 5
                {'SURVEY_MONKEY': "83225187", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 6
                {'SURVEY_MONKEY': "83225189", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 7
                {'SURVEY_MONKEY': "83225191", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 8
                {'SURVEY_MONKEY': "83225193", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}, # 9
                {'SURVEY_MONKEY': "83225195", 'TRANSPARENT_CLASSROOM': 'income_less_than_free_reduced_threshold'}  # 10
            ],
            'CHILDREN': [
                {
                    'FIRST_NAME': {'SURVEY_MONKEY': "83225154", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "83225157", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "83225155", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "83225156", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "83225158", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "83225175", 'TRANSPARENT_CLASSROOM': 'schools_ranking'}
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "83225196", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "83225162", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "83225163", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "83225168", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "83225171", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "83225174", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                }
            ]
        }
    }
}

HUBS['SANDBOX'] = HUBS['CAMBRIDGE']

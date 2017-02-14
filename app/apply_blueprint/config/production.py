import os
import re

TRANSPARENT_CLASSROOM_BASE_URL = "https://www.transparentclassroom.com"

SURVEY_MONKEY_OAUTH_TOKEN=os.environ['SURVEY_MONKEY_OAUTH_TOKEN']

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
                    'EMAIL': {'SURVEY_MONKEY': "83225145", 'TRANSPARENT_CLASSROOM': 'first_parent_email'},
                    'PHONE': {'SURVEY_MONKEY': "83225147", 'TRANSPARENT_CLASSROOM': 'first_parent_mobile_number'},
                    'ADDRESS': {'SURVEY_MONKEY': "83225146", 'TRANSPARENT_CLASSROOM': 'first_parent_address'}
                },
                {
                    'FIRST_NAME': {'SURVEY_MONKEY': "83225149", 'TRANSPARENT_CLASSROOM': 'second_parent_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "83225153", 'TRANSPARENT_CLASSROOM': 'second_parent_name.last'},
                    'EMAIL': {'SURVEY_MONKEY': "83225150", 'TRANSPARENT_CLASSROOM': 'second_parent_email'},
                    'PHONE': {'SURVEY_MONKEY': "83225151", 'TRANSPARENT_CLASSROOM': 'second_parent_mobile_number'},
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
                { # first
                    'FIRST_NAME': {'SURVEY_MONKEY': "83225154", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "83225157", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "83225155", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "83225156", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "83225158", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "83225175", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "83225196", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "83225162", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "83225163", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "83225168", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "83225171", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "83225174", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # second
                    'FIRST_NAME': {'SURVEY_MONKEY': "85155794", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85155795", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85155796", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85155797", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85156539", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85156744", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85155799", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85157346", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85157347", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85157348", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85157349", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "30960542", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # third
                    'FIRST_NAME': {'SURVEY_MONKEY': "85177332", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85177333", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85177334", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85177335", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85177608", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85177822", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85177337", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85178346", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85178347", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85178348", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85178349", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85178350", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # forth
                    'FIRST_NAME': {'SURVEY_MONKEY': "85178901", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85178902", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85178903", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85178904", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85179294", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85179474", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85178906", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85179986", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85179987", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85179988", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85179989", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85179990", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # fifth
                    'FIRST_NAME': {'SURVEY_MONKEY': "85180297", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85180298", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85180299", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85180300", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85180590", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85180822", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85180302", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85181208", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85181209", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85181210", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85181211", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85181212", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # sixth
                    'FIRST_NAME': {'SURVEY_MONKEY': "85181774", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85181775", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85181776", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85181777", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85182120", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85182362", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85181779", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85183100", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85183101", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85183102", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85183103", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85183104", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # seventh
                    'FIRST_NAME': {'SURVEY_MONKEY': "85183680", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85183681", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85183682", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85183683", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85184012", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85184210", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85183685", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85184598", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85184599", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85184600", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85184601", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85184602", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # eigth
                    'FIRST_NAME': {'SURVEY_MONKEY': "85185043", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85185044", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85185045", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85185046", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85185660", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85186062", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85185048", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85186343", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85186344", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85186345", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85186346", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85186348", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
                { # ninth
                    'FIRST_NAME': {'SURVEY_MONKEY': "85186840", 'TRANSPARENT_CLASSROOM': 'child_name.first'},
                    'LAST_NAME': {'SURVEY_MONKEY': "85186841", 'TRANSPARENT_CLASSROOM': 'child_name.last'},
                    'DOB': {'SURVEY_MONKEY': "85186842", 'TRANSPARENT_CLASSROOM': 'child_birth_date'},
                    'GENDER': {'SURVEY_MONKEY': "85186843", 'TRANSPARENT_CLASSROOM': 'child_gender'},
                    'SCHOOLS': {'SURVEY_MONKEY': "85187425", 'TRANSPARENT_CLASSROOM': 'schools'},
                    'SCHOOLS_RANKING': {'SURVEY_MONKEY': "85187659", 'TRANSPARENT_CLASSROOM': 'schools_ranking'},
                    'ANSWERS': [
                        {'SURVEY_MONKEY': "85186845", 'TRANSPARENT_CLASSROOM': 'ethnicity'},
                        {'SURVEY_MONKEY': "85188214", 'TRANSPARENT_CLASSROOM': 'disposition'},
                        {'SURVEY_MONKEY': "85188215", 'TRANSPARENT_CLASSROOM': 'social_style'},
                        {'SURVEY_MONKEY': "85188216", 'TRANSPARENT_CLASSROOM': 'other_schools'},
                        {'SURVEY_MONKEY': "85188217", 'TRANSPARENT_CLASSROOM': 'specialists'},
                        {'SURVEY_MONKEY': "85188218", 'TRANSPARENT_CLASSROOM': 'anything_else_child'}
                    ]
                },
            ]
        }
    }
}

HUBS['SANDBOX'] = HUBS['CAMBRIDGE']
HUBS['SANDBOX']['TRANSPARENT_CLASSROOM_API_TOKEN'] = os.environ['TRANSPARENT_CLASSROOM_API_TOKEN_SANDBOX'],

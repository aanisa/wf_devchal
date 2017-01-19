import os

survey_monkey_oauth_token=os.environ['survey_monkey_oauth_token']
transparent_classroom_api_token=os.environ['transparent_classroom_api_token']

hubs = {
    'cambridge': {
        'survey_monkey_survey_id': '111419034',
        'survey_monkey_collector_id': 'FQDVNM3',
        'answer_key': {
            'parents': [
                {
                    'first_name': {'survey_monkey': '69078793', 'transparent_classroom': 'first_parent_name.first'},
                    'last_name': {'survey_monkey': '77425064', 'transparent_classroom': 'first_parent_name.last'} ,
                    'email': {'survey_monkey': '69078871', 'transparent_classroom': 'first_parent_email'},
                    'phone': {'survey_monkey': '69079428', 'transparent_classroom': 'first_parent_mobile_number'},
                    'address': {'survey_monkey': '69078976', 'transparent_classroom': 'first_parent_address'}
                },
                {
                    'first_name': {'survey_monkey': '69079990', 'transparent_classroom': 'second_parent_name.first'},
                    'last_name': {'survey_monkey': '77425213', 'transparent_classroom': 'second_parent_name.last'},
                    'email': {'survey_monkey': '69079992', 'transparent_classroom': 'second_parent_email'},
                    'phone': {'survey_monkey': '69079993', 'transparent_classroom': 'second_parent_mobile_number'},
                    'address': {'survey_monkey': '69079994', 'transparent_classroom': 'second_parent_address'}
                }
            ],
            'child': {
                'first_name': {'survey_monkey': '69082546', 'transparent_classroom': 'child_name.first'},
                'last_name': {'survey_monkey': '77425286', 'transparent_classroom': 'child_name.last'},
                'dob': {'survey_monkey': '69082734', 'transparent_classroom': 'child_birth_date'},
                'gender': {'survey_monkey': '69083456', 'transparent_classroom': 'child_gender'}
            },
            'schools': {'survey_monkey': '69085210'},
            'questions': [
                {'survey_monkey': '78278744', 'transparent_classroom': 'ethnicity'},
                {'survey_monkey': '78280009', 'transparent_classroom': 'members_in_household'},
                {'survey_monkey': '78282222', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78289530', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78290409', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78290754', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78291057', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78291263', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78291851', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78292095', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '78292399', 'transparent_classroom': 'income_less_than_free_reduced_threshold'},
                {'survey_monkey': '69092809', 'transparent_classroom': 'how_hear'},
                {'survey_monkey': '69092811', 'transparent_classroom': 'caregivers'},
                {'survey_monkey': '69092815', 'transparent_classroom': 'siblings'},
                {'survey_monkey': '69092816', 'transparent_classroom': 'disposition'},
                {'survey_monkey': '69092817', 'transparent_classroom': 'social_style'},
                {'survey_monkey': '69092820', 'transparent_classroom': 'parenting_style'},
                {'survey_monkey': '69092823', 'transparent_classroom': 'typical_weekday'},
                {'survey_monkey': '69092825', 'transparent_classroom': 'typical_weekend'},
                {'survey_monkey': '69092827', 'transparent_classroom': 'ideal_school'},
                {'survey_monkey': '69092836', 'transparent_classroom': 'other_schools'},
                {'survey_monkey': '69092837', 'transparent_classroom': 'montessori'},
                {'survey_monkey': '69092839', 'transparent_classroom': 'what_age'},
                {'survey_monkey': '69092840', 'transparent_classroom': 'specialists'},
                {'survey_monkey': '69092841', 'transparent_classroom': 'involvement'},
                {'survey_monkey': '69092842', 'transparent_classroom': 'enrich'},
                {'survey_monkey': '69092843', 'transparent_classroom': 'anything_else'}
            ]
        }
    }
}

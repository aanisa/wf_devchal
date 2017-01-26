Blueprint Heroku config/env vars:

  heroku config:set survey_monkey_oauth_token=TBD
  heroku config:set transparent_classroom_api_token=TBD

Update config map if changes to Survey Monkey or Transparent Classroom form

Google Account + Calendly Setup

  Create Google Account:
    Create Google apps account named "SCHOOL-NAME-appointments"
    In incognito window:
      Log in to new account

  Set up Calendly:
    Log in to Calendly as user with Admin or Owner privs
    Add new Google account as user

    In incognito window from above:
      Open Calendly invite email, click link, sign up/accept.
      Set timezone
      Update event types with appropriate days of week/times of days

  Set up DB:
    Update seeds with correct URLs, email addresses

  Add teachers to Google Account:
    In incognito window (from above):
      Add/authorize forwarding addresses
      For each forwarding address:
        Create filter
          Forward email sent to the account's address to each forwarding address
      In calendar, share with forwarding address, with "make changes" permission

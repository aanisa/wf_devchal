Global Heroku config/env vars:

  heroku config:set APP_CONFIG_MODE=production
  heroku config:set MAIL_USERNAME=TBD
  heroku config:set MAIL_PASSWORD=TBD


TODO:
  Automatically prefix table names in blueprints (flask_sqlalchemy is causing problems)
  Config is still a global namspace; isolate each blueprint's config
  Add flask cli command to create scaffolding blueprint w. empty req'd files
  blueprint_name in tests feels leaky
  requirements.txt in the blueprints, composited to root
  webpack config in the blueprints, composited to root
  post_compile in the blueprints, composited to root
  nltk_data dir in root is leaky
  make 500 global and apply everywhere

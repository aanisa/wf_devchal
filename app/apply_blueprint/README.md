To create Calendly webhooks:

curl --header "X-TOKEN: FILL_IN_TOKEN_HERE" --data "url=http://requestb.in/qdsf4jqd&events[]=invitee.created&events[]=invitee.canceled" https://calendly.com/api/v1/hooks

http://requestb.in/qdsf4jqd?inspect


 `TCPlugins` into the JS global namespace, and has a prop `userApiToken`



TODO:

Finish UI
Server that serves up script for better URL handling? else something...
Use JS variables to get classroom and teacher id, use API for ACL
Update to use classroom ID in API call
Error message page

Reminders
Incomplete application

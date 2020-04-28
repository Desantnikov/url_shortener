# url_shortener
Simple url shotrener service to practice django and django rest framework skills

Endpoints: 

/api/url/ - GET, POST 

/api/url/<short_id>/ - GET, PUT, DELETE 

/<short_id>/ - GET

/api/url/ POST:

{"url": {"full_url": <full_url>, "shortened_url": "shortened_url"}}

Random if no shortened_url specified

# shrt
A URL shortener written in Django with Postgres and Nginx

The application is fully containerized so once retrieved you just need to run docker compose to bring everything up.
It is set up to run on port 1337 by default. However that is changeable in the docker compose file.

To build and run use `docker-compose up --build -d`

Note: Debug mode is on by default when source is cloned, and the secret key is just set to 'secret key'. Both
of these would need to be changed before deploying this app. They are editable in the `.env.dev` file. The Postgres
database information should also be edited.

## The API

There is only one table in the database which has 4 columns. The integer primary key of each url,
the url that that id redirects to, the expiry date and the view count.

Currently the only methods implemented are GET, POST, PATCH and DELETE. However only the POST method
is accessible through the basic provided front end app, which will add a new url to the database. In the
future mostl likely a way to edit the redirect url, and delete entries all together would be added. For
now you have to use `CURL`.

## The Front End

 There is a basic front end included in the package. The only thing it provides is a form for adding new 
 redirects and a display/copy button for the shortened url.
 
 ## Commands
 
 Also included is a django command which will delete any old/expired commands from the database.
 
 `docker-compose exec web python manage.py clean_urls`
 
 ## Future Considerations
 
 There are a few concerns with this project that I did not have time to directly address: Including limiting the number of requests per second
 so the urls could not be used in some type of DDOS attack, as well as ussues with how Django handles primary keys. Django
 uses a sequence for primary key ids, which means even if you delete old entries it still wont use those now available ids.
 
 If I were to rewrite this application I would not use Django as the back end framework. The scope of this project was small, and Django has a lot
 of overhead. This makes it good for large scale applications but not so much for something like this (It felt a little like using a sledgehammer
 on a finishing nail). A better choice would be either Flask, with no ORM (just using psycopg2) or Flask with SQLAlchemy.

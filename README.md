# Welcome to URL Shortener

Create your own shortened URL or have one Automatically Generated

## Setup

1. Copy and complete both Docker and Django env file
2. Docker-compose up
3. Create and migrate new or use current local settings file

## API Routes

|                |Route                          |Content                         |
|----------------|-------------------------------|-----------------------------|
|                |`/api/url-short`               |URL + Alias + Total Count List|
|                |`/api/url-only`                |Alias List|
|                |`/api/visited`                 |URL Alias List which has been used daily|
|                |`/api/sites-visit-today`       |List Sites Been Used Today|
|                |`/api/top-three-visit`         |List Top Three Sites Used|



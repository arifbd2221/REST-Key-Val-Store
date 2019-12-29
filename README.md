# REST-Key-Val-Store

Used Tech Stack

## 1.Django
## 2.Django Rest-Framework
## 3.Memcached

## Running on your Machine
First install requirements.txt file by the following command
```
pip install -r requirements.txt
```
***
After the successfull installation goto keyvalstore/keyvalstore/settings.py
Then inside setting.py put these code snippets
  
  ```
  CACHE_TTL = 60 * 5

  CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': CACHE_TTL,
    }
  }
  ```
  ->You can set CACHE_TTL as per your requirement.
  ->You can set LOCATION as per your requirement.
 ***
 
 Now run the following command to create django models table inside sqlite database.
 ```
 python manage.py migrate
 ```
 Finally run the below command to start the server
 ```
 python manage.py runserver
 ```

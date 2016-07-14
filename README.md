# flask-restful-login-example

####INSTALLATION
```
git clone https://github.com/melihcolpan/flask-restful-login
cd flask-restful-login
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m main
```

#### For requests using httpie: *[https://github.com/jkbrzt/httpie]()*

##### Register:

```sh
http POST :5000/v1/auth/register username=test_name password=test_password email=example@example.com
```

##### Login:

```sh
http POST :5000/v1/auth/login email=example@example.com password=test_password
Got access token and refresh token!
```
###### Response: Got access token and refresh token!

##### Logout:

```sh
http POST :5000/v1/auth/logout Authorization:"bearer ACCESS_TOKEN" refresh_token=REFRESH_TOKEN
```

##### Test requiring authentication handler

```sh
http GET :5000/data Authorization:"bearer ACCESS_TOKEN"
```

------------------------------------------------------------------------------------------------------------------------

#### For requests using curl: *[https://curl.haxx.se/download.html]()*

##### Register:

```sh
curl -H "Content-Type: application/json" --data '{"username":"test_name","password":"test_password", "email":"example@example.com"}' http://localhost:5000/v1/auth/register
```

##### Login:

```sh
curl -H "Content-Type: application/json" --data '{"email":"example@example.com", "password":"test_password"}' http://localhost:5000/v1/auth/login
```
###### Response: Got access token and refresh token!

##### Logout:

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"refresh_token":"REFRESH_TOKEN"}' http://localhost:5000/v1/auth/logout

```

##### Test requiring authentication handler

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/data
```

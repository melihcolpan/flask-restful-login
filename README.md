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
http POST :5000/v1/auth/register username=example_username password=example_password email=example@example.com
```

##### Login:

```sh
http POST :5000/v1/auth/login email=example@example.com password=example_password
```

###### Response: Got access token and refresh token!

##### Logout:

```sh
http POST :5000/v1/auth/logout Authorization:"bearer ACCESS_TOKEN" refresh_token=REFRESH_TOKEN
```

###### Note: Test user and admin users are created in database initializer class.

##### Test user login: 

```sh
http POST :5000/v1/auth/login email=test_email@example.com password=test_password
```

##### Test admin login: 

```sh
http POST :5000/v1/auth/login email=admin_email@example.com password=admin_password
```

##### Test admin requiring authentication example handlers

```sh
http GET :5000/users Authorization:"bearer ACCESS_TOKEN"
http GET :5000/data_admin Authorization:"Bearer ACCESS_TOKEN"
```

##### Test user requiring authentication handler

```sh
http GET :5000/data_user Authorization:"Bearer ACCESS_TOKEN"
```


------------------------------------------------------------------------------------------------------------------------


#### For requests using curl: *[https://curl.haxx.se/download.html]()*

##### Register:

```sh
curl -H "Content-Type: application/json" --data '{"username":"example_name","password":"example_password", "email":"example@example.com"}' http://localhost:5000/v1/auth/register
```

##### Login:

```sh
curl -H "Content-Type: application/json" --data '{"email":"example@example.com", "password":"example_password"}' http://localhost:5000/v1/auth/login
```

###### Response: Got access token and refresh token!

##### Logout:

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"refresh_token":"REFRESH_TOKEN"}' http://localhost:5000/v1/auth/logout
```

###### Note: Test user and admin users are created in database initializer class.

##### Test user login: 

```sh
curl -H "Content-Type: application/json" --data '{"password":"test_password", "email":"test_email@example.com"}' http://localhost:5000/v1/auth/login
```

##### Test admin login: 

```sh
curl -H "Content-Type: application/json" --data '{"password":"admin_password", "email":"admin_email@example.com"}' http://localhost:5000/v1/auth/login
```

##### Test admin requiring authentication example handlers

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/users
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/data_admin
```

##### Test user requiring authentication handler

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/data_user
```

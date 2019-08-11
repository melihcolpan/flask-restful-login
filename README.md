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

#### For requests using httpie: *[https://httpie.org/doc]()*

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

##### User login: 

```sh
http POST :5000/v1/auth/login email=test_email@example.com password=test_password
```

##### Admin login: 

```sh
http POST :5000/v1/auth/login email=admin_email@example.com password=admin_password
```

##### Super admin login: 

```sh
http POST :5000/v1/auth/login email=sa_email@example.com password=sa_password
```

##### Super admin requiring authentication example handlers

```sh
http GET :5000/user_add Authorization:"bearer ACCESS_TOKEN"

http GET :5000/users Authorization:"Bearer ACCESS_TOKEN" usernames==test_username,admin_username emails==test_email@example.com,admin_email@example.com start_date==01.01.1993 end_date==01.01.2050
```

##### Admin requiring authentication example handlers

```sh
http GET :5000/data_admin Authorization:"Bearer ACCESS_TOKEN"
```

##### User requiring authentication handler

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

##### User login: 

```sh
curl -H "Content-Type: application/json" --data '{"password":"test_password", "email":"test_email@example.com"}' http://localhost:5000/v1/auth/login
```

##### Admin login: 

```sh
curl -H "Content-Type: application/json" --data '{"password":"admin_password", "email":"admin_email@example.com"}' http://localhost:5000/v1/auth/login
```

##### Super admin login: 

```sh
curl -H "Content-Type: application/json" --data '{"password":"sa_password", "email":"sa_email@example.com"}' http://localhost:5000/v1/auth/login
```

##### Test super admin requiring authentication example handlers

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/user_add

curl -X GET 'localhost:5000/users?usernames=test_username,admin_username&emails=test_email@example.com,admin_email@example.com&start_date=01.01.1993&end_date=01.01.2050' -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" 
```

##### Test admin requiring authentication example handlers

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/data_admin
```

##### Test user requiring authentication handler

```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/data_user
```

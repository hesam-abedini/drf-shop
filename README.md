# User API
### Creating A User
#### API EndPoint
    http://127.0.0.1:8000/api/user/create/

- **method :** POST

#### Payload
```python
payload={
	"email":"test@example.com",
	"password":"Testing1",
	"name":"test test",
	"address":{
		"state":"Tehran",
		"city":"Tehran",
		"address_1":"Azadi",
		"address_2":"",
		"postal_code":"1234567",
		"phone_number":"09356732430"
        }
}
```
- **password :** The length of the password has to be at least 5, and it needs to have at least 1 upper case letter,1 lower case letter and 1 number. 
- **address_2 :** address_2 can be null

#### Response
```json
{
    "id": 1,
    "email": "test@example.com",
    "name": "test test",
    "user_permissions": [],
    "address": {
        "state": "Tehran",
        "city": "Tehran",
        "address_1": "Azadi",
        "address_2": "",
        "postal_code": "1234567",
        "phone_number": "09356732430"
    },
    "is_active": true,
    "is_staff": false,
    "is_superuser": false
}
```
### Generating A User Token
#### API EndPoint
    http://127.0.0.1:8000/api/user/token/

- **method :** POST

#### Payload
```python
payload={
	"email":"test@example.com",
	"passowrd":"Testing1"
}
```
#### Response
```json
{
    "refresh": "JWT refresh token",
    "access": "JWT access token"
}
```
### Getting User List
Only super users and staff( is_staff , is_superuser ) can get the user list
#### API EndPoint
    http://127.0.0.1:8000/api/user/
- **method :** GET
- **Authorization :** Bearer Token

#### Query Params
- **search :** search in names and emails
- **ordering :** you can order by  name , email , is_active , is_staff , is_superuser default is id
- **page_size :** page size for pagination default is 20
- **is_staff :** 0 for filtering by False and 1 for filtering for True
- **is_active :** 0 for filtering by False and 1 for filtering for True
- **is_superuser :** 0 for filtering by False and 1 for filtering for True
- **state :** filter by state
- **city :** filter by city

```
http://127.0.0.1:8000/api/user/?search=hesam&ordering=name&page_size=5&is_active=1
```
### User Detail
Only The Owner Of This Profile , super users and staff( is_staff , is_superuser ) can get the user detail

#### API EndPoint
    http://127.0.0.1:8000/api/user/{id}
- **method :** GET
- **Authorization :** Bearer Token
- **id :** User ID

### User Update
Only The Owner Of This Profile , super users and staff( is_staff , is_superuser ) can update the profile

#### API EndPoint
    http://127.0.0.1:8000/api/user/{id}
- **method :** PUT And PATCH
- **Authorization :** Bearer Token
- **id :** User ID
#### Payload Example
```python
payload={
	"name":"test",
	"address":{
		"state":"esfehan"
	},
	"is_active",
	"is_superuser",
	"is_staff"
}
```
- **is_active :** Only super user and staff can change active status
- **is_staff :** Only super user can give staff permission
- **is_superuser :** Only super user can give superuser permission

### User Deletion
Only super users can delete users

#### API EndPoint
    http://127.0.0.1:8000/api/user/{id}
- **method :** DELETE
- **Authorization :** Bearer Token
- **id :** User ID


### User Password Reset Request
sends a password reset email
#### API EndPoint
        http://127.0.0.1:8000/api/user/password-reset/
- **method :** POST
#### Payload
```python
payload={
	"email":"test@example.com"
}
```

### User Password Reset
reset the password
#### API EndPoint
            http://127.0.0.1:8000/api/user/password-reset/{encoded_id}/{token}/
- **method :** PATCH

#### Payload

```python
payload={
	"password":"Testing2"
}
```

# Product API

### Creating Category
Only super user and staff

#### API EndPoint
         http://127.0.0.1:8000/api/products/category/
- **method :** POST
- **Authorization :** Bearer Token

#### Payload
```python
payload={
	"name":"test",
	"description":"testing"
}
```

#### Response

```json
{
    "id": 1,
    "name": "test",
    "description": "testing"
}
```

### Category Detail
#### API EndPoint
    http://127.0.0.1:8000/api/products/category/{id}/
- **method :** GET
- **id :** Category ID

### Getting Category List
#### API EndPoint
         http://127.0.0.1:8000/api/products/category/
- **method :** GET

### Category Update
Only super users and staff( is_staff , is_superuser ) can update categories

#### API EndPoint
    http://127.0.0.1:8000/api/products/category/{id}/
- **method :** PUT And PATCH
- **Authorization :** Bearer Token
- **id :** Category ID

### Category Deletion
Only super users and staff( is_staff , is_superuser ) can delete categories

#### API EndPoint
    http://127.0.0.1:8000/api/products/category/{id}/
- **method :** DELETE
- **Authorization :** Bearer Token
- **id :** Category ID

### Creating Brand
Only super user and staff

#### API EndPoint
         http://127.0.0.1:8000/api/products/brand/
- **method :** POST
- **Authorization :** Bearer Token

#### Payload
```python
payload={
	"name":"test",
	"description":"testing"
}
```

#### Response

```json
{
    "id": 1,
    "name": "test",
    "description": "testing"
}
```

### Brand Detail
#### API EndPoint
    http://127.0.0.1:8000/api/products/brand/{id}/
- **method :** GET
- **id :** Brand ID

### Getting Brand List
#### API EndPoint
         http://127.0.0.1:8000/api/products/brand/
- **method :** GET

### Brand Update
Only super users and staff( is_staff , is_superuser ) can update brands

#### API EndPoint
    http://127.0.0.1:8000/api/products/brand/{id}/
- **method :** PUT And PATCH
- **Authorization :** Bearer Token
- **id :** Brand ID

### Brand Deletion
Only super users and staff( is_staff , is_superuser ) can delete Brands

#### API EndPoint
    http://127.0.0.1:8000/api/products/brand/{id}/
- **method :** DELETE
- **Authorization :** Bearer Token
- **id :** Brand ID

### Creating Product
Only super user and staff

#### API EndPoint
         http://127.0.0.1:8000/api/products/
- **method :** POST
- **Authorization :** Bearer Token

#### Payload
```python
payload={
	"name":"test",
	"description":"testing",
	"other_product_details":"",
	"price":12.50,
	"color":"red",
	"category_id":1,
	"brand_id":1
}
```
- **other_product_details :** can be null


#### Response

```json
{
    "id":1,
    "name": "test",
    "description": "testing",
    "other_product_details": "",
    "price": "12.50",
    "color": "red",
    "image": null,
    "category": {
        "id": 1,
        "name": "test",
        "description": "testing"
    },
    "brand": {
        "id": 1,
        "name": "test",
        "description": "testing"
    }
}
```
### Getting Product List

#### API EndPoint

    http://127.0.0.1:8000/api/products/

- **method :** GET

#### Query Params

- **search :** search in product names
- **ordering :** you can order by  price default is id
- **page_size :** page size for pagination default is 20
- **category :** filter by category id
- **brand :** filter by brand id or list of brand ids

```
http://127.0.0.1:8000/api/products/?category=1,brand=1,2
```
### Getting Product Detail

#### API EndPoint

    http://127.0.0.1:8000/api/products/{id}/

- **method :** GET
- **id :** Product ID

### Updating Product

#### API EndPoint

    http://127.0.0.1:8000/api/products/{id}/update/

- **method :** PUT And PATCH
- **Authorization :** Bearer Token
- **id :** Product ID

### Adding Or Updating Product Image

#### API EndPoint

    http://127.0.0.1:8000/api/products/{id}/update-image/

- **method :** PATCH
- **Authorization :** Bearer Token
- **id :** Product ID

#### Payload
```python
payload={
	"image":image_file
}
```

### Adding Or Updating Product Image

#### API EndPoint

    http://127.0.0.1:8000/api/products/{id}/update-image/

- **method :** PATCH
- **Authorization :** Bearer Token
- **id :** Product ID

### Product Deletion

#### API EndPoint

    http://127.0.0.1:8000/api/products/{id}/delete/

- **method :** DELETE
- **Authorization :** Bearer Token
- **id :** Product ID

### Creating Order
creating order for the user
#### API EndPoint
         http://127.0.0.1:8000/api/products/order/
- **method :** POST
- **Authorization :** Bearer Token

#### Payload 
a list of product ids with quantity
```python
payload=[
	{
	"product":1,
	"quantity":1
	},
	{
	"product":2,
	"quantity":1
	}
]
```
- **product :** Product ID

### Getting Order List
getting order list for the user or all the orders if superuser
#### API EndPoint
         http://127.0.0.1:8000/api/products/order/
- **method :** GET
- **Authorization :** Bearer Token

### Getting Order Detail
#### API EndPoint
         http://127.0.0.1:8000/api/products/order/{id}/
- **method :** GET
- **Authorization :** Bearer Token
- **id :** Order ID


### Creating Comment
#### API EndPoint
         http://127.0.0.1:8000/api/products/comment/
- **method :** POST
- **Authorization :** Bearer Token

#### Payload
```python
payload={
	"content":"test",
	"product_id":1.
	"reply_to_id":null
}
```
- **product_id :** Id of the product that is being commented on
- **reply_to_id :** Id of the comment that is being replied to can be null if comment is not a reply


### Getting Comment List
getting comments for the product
#### API EndPoint
         http://127.0.0.1:8000/api/products/{id}/comment/
- **method :** POST
- **Authorization :** Bearer Token
- **id :** Product ID

#### Query Params

- **page_size :** page size for pagination default is 20


### Updating Comment
#### API EndPoint
         http://127.0.0.1:8000/api/products/{comment/{id}/update/
- **method :** PATCH
- **Authorization :** Bearer Token
- **id :** Comment ID

### Deleting Comment
#### API EndPoint
         http://127.0.0.1:8000/api/products/{comment/{id}/delete/
- **method :** DELETE
- **Authorization :** Bearer Token
- **id :** Comment ID


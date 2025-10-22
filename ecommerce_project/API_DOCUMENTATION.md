# eCommerce API Documentation

## Base URL
```
http://127.0.0.1:8000/
```

## Authentication

### Get JWT Token
**Important**: Use the web registration to create your account first at `/register/`, then use those credentials here.

**Endpoint**: `POST /api/v1/auth/login/`

**Request**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Example**:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"vendor1","password":"yourpassword"}'
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Note**: If you get "No active account found", make sure:
1. You created an account via web registration first
2. The username and password are correct
3. The account is active

### Refresh Token
**Endpoint**: `POST /api/v1/auth/refresh/`

**Request**:
```json
{
  "refresh": "your_refresh_token"
}
```

**Response**:
```json
{
  "access": "new_access_token"
}
```

### Using Tokens

Add the access token to all subsequent requests:
```
Authorization: Bearer {access_token}
```

---

## API Endpoints

### Stores API

#### 1. List All Stores
**Endpoint**: `GET /api/stores/`

**Authentication**: Optional (public can view)

**Example**:
```bash
curl http://127.0.0.1:8000/api/stores/
```

**Response**:
```json
[
  {
    "id": 1,
    "name": "Tech Store",
    "description": "Electronics and gadgets",
    "logo": "/media/store_logos/logo.jpg"
  }
]
```

#### 2. Create Store (Vendor Only)
**Endpoint**: `POST /api/stores/`

**Authentication**: Required (Vendor only)

**Request Body**:
```json
{
  "name": "My New Store",
  "description": "Store description here",
  "logo": null
}
```

**Example**:
```bash
curl -X POST http://127.0.0.1:8000/api/stores/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics Plus",
    "description": "Best electronics in town"
  }'
```

**Response**:
```json
{
  "id": 2,
  "name": "Electronics Plus",
  "description": "Best electronics in town",
  "logo": null
}
```

#### 3. Get Store Details
**Endpoint**: `GET /api/stores/{id}/`

**Example**:
```bash
curl http://127.0.0.1:8000/api/stores/1/
```

#### 4. Update Store (Vendor Owner Only)
**Endpoint**: `PUT /api/stores/{id}/`

**Authentication**: Required (Must be store owner)

**Request Body**:
```json
{
  "name": "Updated Store Name",
  "description": "Updated description"
}
```

**Example**:
```bash
curl -X PUT http://127.0.0.1:8000/api/stores/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Store Pro",
    "description": "Premium electronics"
  }'
```

#### 5. Delete Store (Vendor Owner Only)
**Endpoint**: `DELETE /api/stores/{id}/`

**Authentication**: Required (Must be store owner)

**Example**:
```bash
curl -X DELETE http://127.0.0.1:8000/api/stores/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Products API

#### 1. List All Products
**Endpoint**: `GET /api/products/`

**Authentication**: Optional

**Example**:
```bash
curl http://127.0.0.1:8000/api/products/
```

**Response**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": "999.99",
    "stock": 10,
    "store": 1,
    "image": "/media/products/laptop.jpg"
  }
]
```

#### 2. Create Product (Vendor Only)
**Endpoint**: `POST /api/products/`

**Authentication**: Required (Vendor only)

**Request Body**:
```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": "99.99",
  "stock": 50,
  "store": 1
}
```

**Example**:
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": "29.99",
    "stock": 100,
    "store": 1
  }'
```

**Note**: The `store` must be owned by the authenticated vendor.

#### 3. Get Product Details
**Endpoint**: `GET /api/products/{id}/`

**Example**:
```bash
curl http://127.0.0.1:8000/api/products/1/
```

#### 4. Update Product (Vendor Owner Only)
**Endpoint**: `PUT /api/products/{id}/` or `PATCH /api/products/{id}/`

**Authentication**: Required (Must own the store)

**Request Body**:
```json
{
  "name": "Updated Product Name",
  "price": "89.99",
  "stock": 75
}
```

**Example**:
```bash
curl -X PATCH http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": "79.99",
    "stock": 50
  }'
```

#### 5. Delete Product (Vendor Owner Only)
**Endpoint**: `DELETE /api/products/{id}/`

**Example**:
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Reviews API

#### 1. List All Reviews
**Endpoint**: `GET /api/reviews/`

**Example**:
```bash
curl http://127.0.0.1:8000/api/reviews/
```

#### 2. Create Review (Authenticated Users)
**Endpoint**: `POST /api/reviews/`

**Authentication**: Required

**Request Body**:
```json
{
  "product": 1,
  "rating": 5,
  "comment": "Great product!"
}
```

**Example**:
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "rating": 5,
    "comment": "Excellent quality and fast shipping!"
  }'
```

---

## Complete Workflow Example

### 1. Create Account (Web Only)
Visit: http://127.0.0.1:8000/register/
- Register as a Vendor
- Username: vendor1
- Password: mypassword123

### 2. Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "vendor1",
    "password": "mypassword123"
  }'
```

Save the `access` token.

### 3. Create a Store
```bash
curl -X POST http://127.0.0.1:8000/api/stores/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Electronics Store",
    "description": "Quality electronics at great prices"
  }'
```

Note the store `id` from the response.

### 4. Create a Product
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop with RTX graphics",
    "price": "1299.99",
    "stock": 15,
    "store": 1
  }'
```

### 5. Update Product
```bash
curl -X PATCH http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": "1199.99",
    "stock": 12
  }'
```

### 6. List Your Stores
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/stores/
```

---

## Permissions Summary

| Endpoint | Method | Public | Buyer | Vendor |
|----------|--------|--------|-------|--------|
| `/api/stores/` | GET | ✅ Read | ✅ Read | ✅ Read |
| `/api/stores/` | POST | ❌ | ❌ | ✅ Create |
| `/api/stores/{id}/` | PUT/PATCH | ❌ | ❌ | ✅ Own only |
| `/api/stores/{id}/` | DELETE | ❌ | ❌ | ✅ Own only |
| `/api/products/` | GET | ✅ Read | ✅ Read | ✅ Read |
| `/api/products/` | POST | ❌ | ❌ | ✅ Create |
| `/api/products/{id}/` | PUT/PATCH | ❌ | ❌ | ✅ Own only |
| `/api/products/{id}/` | DELETE | ❌ | ❌ | ✅ Own only |
| `/api/reviews/` | GET | ✅ Read | ✅ Read | ✅ Read |
| `/api/reviews/` | POST | ❌ | ✅ Create | ✅ Create |
| `/api/reviews/{id}/` | PUT/PATCH | ❌ | ✅ Own only | ✅ Own only |
| `/api/reviews/{id}/` | DELETE | ❌ | ✅ Own only | ✅ Own only |

---

## Troubleshooting

### "No active account found"
- Make sure you registered via web first: `/register/`
- Check username and password are correct
- Ensure account is active

### "Authentication credentials were not provided"
- Add `Authorization: Bearer {token}` header
- Make sure token hasn't expired
- Get new token if needed

### "You do not have permission"
- Check you're logged in as the correct user type (Vendor for stores/products)
- Vendors can only modify their own resources
- Reviews require authentication

### Token Expired
- Use the refresh endpoint with your refresh token
- Or login again to get new tokens

---

## Testing with Python

```python
import requests

# 1. Login
response = requests.post('http://127.0.0.1:8000/api/v1/auth/login/', json={
    'username': 'vendor1',
    'password': 'mypassword123'
})
token = response.json()['access']

# 2. Create Store
headers = {'Authorization': f'Bearer {token}'}
store_response = requests.post('http://127.0.0.1:8000/api/stores/', 
    headers=headers,
    json={'name': 'My Store', 'description': 'Great products'}
)
store_id = store_response.json()['id']

# 3. Create Product
product_response = requests.post('http://127.0.0.1:8000/api/products/',
    headers=headers,
    json={
        'name': 'Laptop',
        'description': 'Gaming laptop',
        'price': '999.99',
        'stock': 10,
        'store': store_id
    }
)

print('Product created:', product_response.json())
```

---

## Response Formats

### Success Response
```json
{
  "id": 1,
  "name": "Resource name",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

Or:
```json
{
  "field_name": ["Error message for this field"]
}
```

---

## Available Endpoints Summary

```
Authentication:
POST   /api/v1/auth/login/          - Get JWT token
POST   /api/v1/auth/refresh/        - Refresh JWT token

Stores:
GET    /api/stores/                 - List all stores
POST   /api/stores/                 - Create store (Vendor)
GET    /api/stores/{id}/            - Get store details
PUT    /api/stores/{id}/            - Update store (Owner)
PATCH  /api/stores/{id}/            - Partial update (Owner)
DELETE /api/stores/{id}/            - Delete store (Owner)

Products:
GET    /api/products/               - List all products
POST   /api/products/               - Create product (Vendor)
GET    /api/products/{id}/          - Get product details
PUT    /api/products/{id}/          - Update product (Owner)
PATCH  /api/products/{id}/          - Partial update (Owner)
DELETE /api/products/{id}/          - Delete product (Owner)

Reviews:
GET    /api/reviews/                - List all reviews
POST   /api/reviews/                - Create review (Authenticated)
GET    /api/reviews/{id}/           - Get review details
PUT    /api/reviews/{id}/           - Update review (Owner)
PATCH  /api/reviews/{id}/           - Partial update (Owner)
DELETE /api/reviews/{id}/           - Delete review (Owner)
```

---

## Field Requirements

### Store Creation
- `name` (required, string, max 100 chars, unique)
- `description` (optional, text)
- `logo` (optional, image file)

### Product Creation
- `name` (required, string, max 255 chars)
- `description` (required, text)
- `price` (required, decimal, format: "99.99")
- `stock` (required, integer, >= 0)
- `store` (required, integer, your store ID)
- `image` (optional, image file)

### Review Creation
- `product` (required, integer, product ID)
- `rating` (required, integer, 1-5)
- `comment` (required, text)

---

## Complete Example Session

```bash
# Step 1: Register via web browser at http://127.0.0.1:8000/register/
# Create vendor account: username=vendor1, password=Test123!

# Step 2: Get JWT Token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"vendor1","password":"Test123!"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# Step 3: Create Store
STORE=$(curl -s -X POST http://127.0.0.1:8000/api/stores/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech Haven","description":"Latest tech products"}')

echo "Store created: $STORE"

# Step 4: Create Product (replace store ID)
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Mechanical Keyboard",
    "description":"RGB mechanical gaming keyboard",
    "price":"89.99",
    "stock":25,
    "store":1
  }'

# Step 5: List all products
curl http://127.0.0.1:8000/api/products/

# Step 6: Update product price
curl -X PATCH http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price":"79.99"}'
```

---

## Notes

- **Authentication**: JWT tokens expire after 1 hour (configurable)
- **Permissions**: Vendors can only modify their own stores/products
- **Validation**: All fields are validated server-side
- **Images**: For image uploads, use multipart/form-data instead of JSON
- **Pagination**: Large lists are paginated (10 items per page by default)

---

## Error Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Deleted successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - No permission
- `404 Not Found` - Resource doesn't exist

---

For more details, visit the browsable API at: http://127.0.0.1:8000/api/

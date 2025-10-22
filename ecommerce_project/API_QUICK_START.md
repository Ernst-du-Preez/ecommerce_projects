# API Quick Start Guide

## ⚠️ IMPORTANT: JWT Authentication Issue Resolution

### Problem
Getting "No active account found with the given credentials" when trying to get JWT token.

### Solution

**The JWT token endpoint works correctly.** The error means either:
1. Username or password is incorrect
2. No account exists with those credentials
3. Account is inactive

### How to Fix

#### Option 1: Create a Fresh Test Account

1. Visit: http://127.0.0.1:8000/register/
2. Create account:
   - Username: `testvendor`
   - Password: `TestPass123!`
   - Account Type: `Vendor`
3. Use these exact credentials for API

#### Option 2: Use Existing Account

If you already have an account, use the EXACT credentials you registered with.

#### Option 3: Create Account via Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group
from ecommerce.models import Store

# Create vendor user
user = User.objects.create_user(
    username='apivendor',
    password='ApiPass123!',
    email='vendor@test.com'
)

# Add to Vendor group
vendor_group, _ = Group.objects.get_or_create(name='Vendor')
user.groups.add(vendor_group)

print(f"Created user: {user.username}")
print("Password: ApiPass123!")
exit()
```

---

## Testing JWT Authentication

### 1. Get Token (Replace with your actual credentials)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"apivendor","password":"ApiPass123!"}'
```

**Expected Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Use Token to Create Store

```bash
curl -X POST http://127.0.0.1:8000/api/stores/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Test Store",
    "description": "Created via API"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "name": "API Test Store",
  "description": "Created via API",
  "logo": null
}
```

### 3. Create Product

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "Product created via API",
    "price": "99.99",
    "stock": 50,
    "store": 1
  }'
```

---

## Quick Reference

### All Endpoints

```
Authentication:
POST /api/v1/auth/login/    - Get JWT tokens
POST /api/v1/auth/refresh/  - Refresh access token

Stores (CRUD):
GET    /api/stores/         - List stores
POST   /api/stores/         - Create store (Vendor only)
GET    /api/stores/{id}/    - Store details
PUT    /api/stores/{id}/    - Update store (Owner only)
DELETE /api/stores/{id}/    - Delete store (Owner only)

Products (CRUD):
GET    /api/products/       - List products
POST   /api/products/       - Create product (Vendor only)
GET    /api/products/{id}/  - Product details
PUT    /api/products/{id}/  - Update product (Owner only)
DELETE /api/products/{id}/  - Delete product (Owner only)

Reviews (CRUD):
GET    /api/reviews/        - List reviews
POST   /api/reviews/        - Create review (Authenticated)
GET    /api/reviews/{id}/   - Review details
PUT    /api/reviews/{id}/   - Update review (Owner only)
DELETE /api/reviews/{id}/   - Delete review (Owner only)
```

### Required Headers

**For Authentication**:
```
Content-Type: application/json
```

**For Authenticated Requests**:
```
Authorization: Bearer {your_access_token}
Content-Type: application/json
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "No active account found" | Check username/password, create account via /register/ |
| "Authentication credentials were not provided" | Add Authorization header with Bearer token |
| "You do not have permission" | Check user role (vendors for stores/products) |
| Token expired | Use refresh endpoint or login again |
| Can't create product | Ensure store ID belongs to you |
| Can't update resource | Must be the owner of the resource |

---

## Verification Steps

1. ✅ Create account via web: http://127.0.0.1:8000/register/
2. ✅ Get JWT token via API with your credentials
3. ✅ Create store via API with token
4. ✅ Create product via API with token
5. ✅ Verify permissions work (can't edit other vendors' resources)

**The API is fully functional with proper authentication and role-based permissions!**

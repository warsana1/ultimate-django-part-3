# Storefront API

A production-ready e-commerce REST API built with Django REST Framework. Supports product browsing, shopping carts, order management, JWT authentication, async task processing, and Redis caching.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 3.2 + Django REST Framework |
| Database | MySQL |
| Auth | JWT (djangorestframework-simplejwt + Djoser) |
| Async Tasks | Celery + Redis |
| Caching | Redis (django-redis) |
| Static Files | WhiteNoise |
| Production Server | Gunicorn |

## Project Structure

```
storefront3/
├── storefront/          # Django project config (settings, URLs, Celery)
│   └── settings/
│       ├── common.py    # Shared settings
│       ├── dev.py       # Development overrides
│       └── prod.py      # Production overrides
├── store/               # Core e-commerce app
├── core/                # Custom user model and auth serializers
├── tags/                # Generic tagging system (content types)
├── likes/               # Generic likes system (content types)
├── playground/          # Sandbox for experimentation
└── locustfiles/         # Load testing scripts
```

## Data Models

- **Product** — title, slug, description, unit price, inventory, collection, promotions, images
- **Collection** — groups products; can have a featured product
- **Customer** — linked 1:1 to User; has phone, birth date, membership tier (Bronze / Silver / Gold)
- **Cart** — UUID-identified, anonymous; holds CartItems
- **Order** — links a Customer to OrderItems; tracks payment status (Pending / Complete / Failed)
- **Review** — belongs to a Product; has name, description, date
- **Tag / TaggedItem** — generic tagging via Django content types
- **LikedItem** — generic likes via Django content types

## API Endpoints

| Endpoint | Description | Auth Required |
|---|---|---|
| `GET /store/products/` | List products (filter, search, sort, paginate) | No |
| `POST /store/products/` | Create product | Admin |
| `GET /store/products/{id}/` | Get product detail | No |
| `PUT/PATCH/DELETE /store/products/{id}/` | Update or delete product | Admin |
| `GET/POST /store/products/{id}/reviews/` | List or create reviews | No |
| `GET/POST /store/products/{id}/images/` | List or upload product images | No |
| `GET/POST /store/collections/` | List or create collections | No / Admin |
| `GET/POST /store/carts/` | Create a cart | No |
| `GET /store/carts/{uuid}/` | Get cart with items and total | No |
| `DELETE /store/carts/{uuid}/` | Delete cart | No |
| `GET/POST /store/carts/{uuid}/items/` | List or add cart items | No |
| `PATCH/DELETE /store/carts/{uuid}/items/{id}/` | Update quantity or remove item | No |
| `GET /store/customers/` | List all customers | Admin |
| `GET/PUT /store/customers/me/` | Get or update own profile | Authenticated |
| `GET /store/customers/{id}/history/` | View customer history | `view_history` permission |
| `GET/POST /store/orders/` | List own orders or create from cart | Authenticated |
| `PATCH/DELETE /store/orders/{id}/` | Update payment status or cancel | Admin |
| `POST /auth/users/` | Register new user | No |
| `POST /auth/jwt/create/` | Obtain JWT token pair | No |
| `POST /auth/jwt/refresh/` | Refresh access token | No |

### Filtering / Search / Ordering (Products)

| Parameter | Example | Description |
|---|---|---|
| `collection_id` | `?collection_id=3` | Filter by collection |
| `unit_price__gt` | `?unit_price__gt=10` | Price greater than |
| `unit_price__lt` | `?unit_price__lt=50` | Price less than |
| `search` | `?search=laptop` | Search title and description |
| `ordering` | `?ordering=unit_price` | Sort by field (`-` prefix for descending) |

Pagination: 10 items per page via `?page=N`.

## Setup

### Prerequisites

- Python 3.14+
- MySQL
- Redis

### Install dependencies

```bash
pipenv install --dev
pipenv shell
```

### Environment variables

Create a `.env` file in the project root:

```env
DB_NAME=storefront
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DJANGO_LOG_LEVEL=INFO
```

For production, also set:

```env
SECRET_KEY=your-production-secret-key
```

### Database

```bash
python manage.py migrate
```

Seed sample data:

```bash
python manage.py seed_db
```

### Run development server

```bash
python manage.py runserver
```

## Running in Production

```bash
gunicorn storefront.wsgi --env DJANGO_SETTINGS_MODULE=storefront.settings.prod
```

Collect static files before deploying:

```bash
python manage.py collectstatic
```

## Background Tasks (Celery)

Start the Celery worker:

```bash
celery -A storefront worker --loglevel=info
```

Start the Celery beat scheduler:

```bash
celery -A storefront beat --loglevel=info
```

Monitor tasks with Flower:

```bash
celery -A storefront flower
```

A scheduled task (`notify_customers`) runs every 5 seconds as an example.

## Testing

Run all tests:

```bash
pytest
```

Watch mode:

```bash
ptw
```

## Load Testing

```bash
locust -f locustfiles/browse_products.py
```

Then open `http://localhost:8089` and configure the target host and user count.

## Authentication

This API uses JWT tokens. Include the token in request headers:

```
Authorization: JWT <access_token>
```

Access tokens expire after 1 day. Use `/auth/jwt/refresh/` to get a new one.

## Permissions

| Role | Can Do |
|---|---|
| Anonymous | Read products, collections; manage own cart |
| Authenticated | Place orders, view own orders, update own profile |
| Admin (staff) | Full CRUD on products, collections, customers, orders |
| `view_history` permission | View customer history |
| `cancel_order` permission | Cancel orders |

## Developer Tools

- **Django Debug Toolbar** — available at `/__debug__/` in development
- **Django Silk** — profiling UI at `/silk/` (requires `SilkyMiddleware` to be enabled)
- **Logging** — logs to console and `general.log`; level controlled via `DJANGO_LOG_LEVEL` env var

# FarmAsyst North — Backend API

Django REST Framework API for the FarmAsyst North agri-fintech platform.

## Stack
- **Python 3.12** + **Django 5** + **Django REST Framework**
- **PostgreSQL** (production) / SQLite (dev fallback)
- **JWT auth** via `djangorestframework-simplejwt`
- **MTN MoMo** + **Paystack** payment integrations
- **Hubtel SMS** notifications (Twilio fallback)
- **AWS S3 / Cloudflare R2** file storage

## Apps
| App | Responsibility |
|-----|---------------|
| `accounts` | Custom User model, FarmerProfile, InvestorProfile, KYC, auth |
| `farms` | Farm profiles, daily activity logs, audit reports |
| `credit` | Applications, documents, agreements, workflow |
| `payments` | Disbursements, repayment schedules, MoMo/Paystack |
| `marketplace` | Produce listings, orders, reviews |
| `training` | Training modules, enrolments, progress tracking |
| `notifications` | In-app notifications, SMS hooks |
| `investors` | Reserved for Phase 6 impact analytics |

## Setup

```bash
git clone <repo>
cd farmasyst-north-api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in your values
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Base URL
```
http://localhost:8000/api/v1/
```

## Key Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register farmer/investor/consumer |
| POST | `/auth/login/` | Get JWT tokens |
| POST | `/auth/refresh/` | Refresh access token |
| POST | `/auth/logout/` | Blacklist refresh token |
| GET/PUT | `/auth/me/` | Current user profile |

### Farmer
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PUT | `/profiles/farmer/` | Farmer KYC profile |
| CRUD | `/farms/` | Farm management |
| CRUD | `/farms/{id}/activity-logs/` | Daily farm logs |
| CRUD | `/credit/applications/` | Credit applications |
| POST | `/credit/applications/{id}/submit/` | Submit draft |
| POST | `/credit/applications/{id}/documents/` | Upload documents |
| GET | `/credit/agreements/` | View contracts |
| POST | `/credit/agreements/{id}/sign/` | Sign contract |
| GET | `/payments/schedules/` | Repayment schedule |
| POST | `/payments/initiate-repayment/` | Pay via MoMo/Paystack |

### Investor
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PUT | `/profiles/investor/` | Investor KYC profile |
| GET | `/farms/` | Browse farmer farms |
| GET | `/credit/agreements/` | Portfolio agreements |
| POST | `/credit/agreements/{id}/sign/` | Sign contract |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| CRUD | `/users/` | User management |
| POST | `/users/{id}/verify/` | Verify farmer/investor |
| POST | `/users/{id}/suspend/` | Suspend account |
| GET | `/credit/applications/` | All applications |
| POST | `/credit/applications/{id}/approve/` | Approve application |
| POST | `/credit/applications/{id}/reject/` | Reject with reason |
| CRUD | `/payments/disbursements/` | Trigger disbursements |

### Marketplace
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/marketplace/produce/` | Browse produce |
| CRUD | `/marketplace/orders/` | Place/manage orders |
| POST | `/webhooks/paystack/` | Paystack webhook |

## Environment Variables
See `.env.example` for all required variables.

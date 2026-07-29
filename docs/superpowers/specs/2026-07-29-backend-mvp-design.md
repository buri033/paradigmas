# DuckBank Backend MVP — Design Spec

**Date:** 2026-07-29  
**Stack:** Django 5.x + DRF + PostgreSQL + JWT  
**Scope:** Replace Supabase with a Python backend; connect existing frontend to REST API.

---

## 1. Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.x + Django REST Framework |
| Database | PostgreSQL 16 |
| Auth | JWT (djangorestframework-simplejwt) |
| Admin | Django Admin (built-in) |
| CORS | django-cors-headers |
| Env vars | python-decouple |
| Cron | django-crontab (for interest calculations) |

### App Structure

```
backend/
├── manage.py
├── requirements.txt
├── duckbank/               # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # User management & auth
├── accounts/               # Digital accounts & balances
├── transactions/            # Transfers, deposits, withdrawals, contacts
├── savings/                # Savings boxes (11% compound annual)
├── loans/                  # Loans, cards, simulator
├── notifications/          # Notifications
└── money_requests/         # P2P money requests
```

### Frontend-Backend Connection

- Replace all mock data and `localStorage` usage with `fetch()` calls to `http://localhost:8000/api/`
- JWT tokens stored in `localStorage` for auth
- Create a shared `api.js` module in the frontend

---

## 2. Data Models

### users — Profile

Extends Django's built-in `auth.User` with a `Profile` model.

| Field | Type | Notes |
|-------|------|-------|
| user | OneToOneField(User) | Cascade delete |
| rut | CharField(12) | Unique, nullable |
| phone | CharField(15) | Nullable |
| avatar_url | URLField | Nullable |
| role | CharField | 'user' or 'admin', default 'user' |
| account_tier | CharField | 'basic', 'prime', 'gold', default 'prime' |
| hide_balance | BooleanField | Default False — show/hide balance toggle |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

**Signal:** On User creation, auto-create Profile and a default "Cuenta Vista" Account.

### accounts — Account

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| account_type | CharField | 'vista', 'ahorro', 'corriente' |
| account_number | CharField(20) | Unique, auto-generated |
| alias | CharField(50) | Nullable — "Cuenta Vista", "Ahorro Vacaciones" |
| balance | BigIntegerField | CLP, default 0 |
| currency | CharField(3) | Default 'CLP' |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### transactions — Transaction

| Field | Type | Notes |
|-------|------|-------|
| account | FK(Account) | Cascade |
| user | FK(Profile) | Cascade |
| type | CharField | 'income', 'expense', 'transfer' |
| amount | BigIntegerField | CLP |
| description | CharField(200) | |
| category | CharField(50) | Nullable |
| icon | CharField(10) | Default '💰' |
| reference | CharField(50) | Nullable |
| destination_name | CharField(100) | Nullable — for transfers |
| destination_account | CharField(20) | Nullable — for transfers |
| created_at | DateTimeField | auto_now_add |

**Signal:** On Transaction creation, update Account.balance (+income, -expense/transfer).

### transactions — Contact

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| name | CharField(100) | |
| bank | CharField(50) | |
| rut | CharField(12) | Nullable |
| account_number | CharField(20) | |
| avatar_color | CharField(7) | Default '#6366f1' |
| created_at | DateTimeField | auto_now_add |

### savings — SavingsBox

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| name | CharField(100) | "Viaje a Europa" |
| balance | BigIntegerField | CLP, default 0 |
| interest_rate | DecimalField(5,2) | Default 11.00 (11%) |
| is_active | BooleanField | Default True |
| created_at | DateTimeField | auto_now_add |

### savings — SavingsBoxInterestLog

| Field | Type | Notes |
|-------|------|-------|
| box | FK(SavingsBox) | Cascade |
| period_start | DateField | |
| period_end | DateField | |
| interest_earned | BigIntegerField | CLP earned in this period |
| balance_before | BigIntegerField | |
| balance_after | BigIntegerField | |
| created_at | DateTimeField | auto_now_add |

**Interest calculation:** Daily cron job computes `balance * (1 + rate/365)` for each active box, logging the result. This implements compound interest at 11% annual, capitalized daily.

### loans — Loan

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| loan_name | CharField(100) | "Crédito de Consumo" |
| total_amount | BigIntegerField | |
| remaining | BigIntegerField | Saldo pendiente |
| monthly_fee | BigIntegerField | Cuota mensual |
| interest_rate | DecimalField(5,2) | Tasa mensual % |
| total_quotas | IntegerField | |
| paid_quotas | IntegerField | Default 0 |
| next_due_date | DateField | |
| status | CharField | 'active', 'paid', 'defaulted' |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### loans — Card

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| card_name | CharField(50) | "Duck Visa Signature" |
| card_type | CharField | 'credit', 'debit' |
| last_four | CharField(4) | |
| cvv | CharField(3) | |
| credit_limit | BigIntegerField | |
| used_amount | BigIntegerField | Default 0 |
| expiry_date | CharField(5) | "12/28" |
| card_network | CharField(20) | Default 'Visa' |
| status | CharField | 'active', 'locked', 'cancelled' |
| color | CharField(7) | Default '#6366f1' |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### notifications — Notification

| Field | Type | Notes |
|-------|------|-------|
| user | FK(Profile) | Cascade |
| title | CharField(100) | |
| message | TextField | |
| type | CharField | 'info', 'success', 'warning', 'error' |
| is_read | BooleanField | Default False |
| created_at | DateTimeField | auto_now_add |

### money_requests — MoneyRequest

| Field | Type | Notes |
|-------|------|-------|
| requester | FK(Profile, related_name='requests_made') | |
| target | FK(Profile, related_name='requests_received') | |
| amount | BigIntegerField | CLP |
| description | CharField(200) | |
| status | CharField | 'pending', 'accepted', 'rejected', 'expired' |
| created_at | DateTimeField | auto_now_add |
| responded_at | DateTimeField | Nullable |

**On accept:** Auto-create a transfer transaction from target's account to requester's account.

---

## 3. API Endpoints

### Auth (users app)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login → JWT access + refresh |
| POST | `/api/auth/refresh/` | Refresh JWT token |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| GET | `/api/profile/` | Get current user's profile |
| PATCH | `/api/profile/` | Update profile (including hide_balance) |

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/` | List user's accounts |
| GET | `/api/accounts/{id}/` | Account detail |
| POST | `/api/accounts/{id}/toggle-balance/` | Toggle hide_balance |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List transactions (paginated, filterable) |
| POST | `/api/transactions/` | Create transaction |
| POST | `/api/transfers/` | Transfer between accounts |
| POST | `/api/deposits/` | Deposit to account |
| POST | `/api/withdrawals/` | Withdraw from account |

### Contacts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/contacts/` | List contacts |
| POST | `/api/contacts/` | Add contact |
| DELETE | `/api/contacts/{id}/` | Delete contact |

### Savings Boxes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/savings-boxes/` | List user's savings boxes |
| POST | `/api/savings-boxes/` | Create savings box |
| GET | `/api/savings-boxes/{id}/` | Detail with interest earned |
| POST | `/api/savings-boxes/{id}/deposit/` | Deposit money into box |
| POST | `/api/savings-boxes/{id}/withdraw/` | Withdraw money from box |
| GET | `/api/savings-boxes/{id}/interest-log/` | Interest calculation history |

### Loans & Cards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/loans/` | List user's loans |
| POST | `/api/loans/{id}/pay-quota/` | Pay a loan quota |
| POST | `/api/loans/simulate/` | Credit simulator (no model) |
| GET | `/api/cards/` | List user's cards |
| POST | `/api/cards/{id}/toggle-lock/` | Lock/unlock card |
| POST | `/api/cards/{id}/pay/` | Pay card balance |

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | List (filterable by unread) |
| POST | `/api/notifications/{id}/read/` | Mark as read |
| POST | `/api/notifications/read-all/` | Mark all as read |

### Money Requests (P2P)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/money-requests/` | List sent & received |
| POST | `/api/money-requests/` | Create request |
| POST | `/api/money-requests/{id}/accept/` | Accept (auto-transfer) |
| POST | `/api/money-requests/{id}/reject/` | Reject |

---

## 4. Business Logic

### Interest Calculation (Cajitas)

- Daily cron at 00:00 UTC calculates compound interest: `new_balance = balance * (1 + rate/36500)`
- Each calculation creates a `SavingsBoxInterestLog` entry
- API endpoint shows projected earnings at current rate

### Credit Simulator

- POST with `amount` (CLP) and `term` (months)
- Uses French amortization formula: `monthly_fee = amount * (r * (1+r)^n) / ((1+r)^n - 1)` where `r` is monthly rate
- Returns: monthly_fee, total_cost, total_interest

### Show/Hide Balance

- `Profile.hide_balance` field controls visibility
- When `True`, `/api/accounts/{id}/balance/` returns `"***"` instead of the number
- Frontend toggle button calls `/api/accounts/{id}/toggle-balance/`

### Transfer Flow

1. Validate sender has sufficient balance
2. Create expense transaction on sender's account
3. Create income transaction on receiver's account
4. Update both account balances atomically (database transaction)

### Money Request Flow

1. Requester creates a `MoneyRequest` → target gets a Notification
2. Target accepts → auto-transfer from target to requester
3. Target rejects → status changes, requester gets Notification

---

## 5. Frontend Integration Plan

- Replace all mock data in each JS file with API calls
- Create `js/api.js` with:
  - `getAPI()`, `postAPI()`, `patchAPI()`, `deleteAPI()` — wrappers with JWT headers
  - Token management: save/access/refresh JWT
- Each page JS file calls `api.js` functions instead of using hardcoded data
- Keep existing CSS and HTML structure unchanged

---

## 6. Seed Data

Django fixtures with:
- 3 investment funds (Conservador, Balanceado, Agresivo)
- Demo user: `admin@duckbank.cl` / `admin123` (role=admin)
- Demo user: `juan@duckbank.cl` / `juan123` (role=user, tier=prime)
- Pre-loaded account with $4,850,900 CLP balance (matching current mock)
- Sample transactions, cards, loans, and notifications
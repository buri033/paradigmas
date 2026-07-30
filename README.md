# 🦆 DuckBank - Banca en Línea

DuckBank es una aplicación bancaria digital que combina un frontend responsivo en HTML/CSS/JS con un backend RESTful en Django. El proyecto implementa gestión de usuarios, cuentas digitales, transferencias, depósitos, retiros, cajitas de ahorro (11% anual compuesto), créditos, tarjetas, simulador de crédito, notificaciones y solicitudes de dinero P2P.

---

## 📁 Estructura del Proyecto

```text
bank-paradigmas/
├── README.md                          # ← Este archivo
├── backend/                           # 🐍 Django + DRF (API REST)
│   ├── duckbank/                      # Configuración del proyecto Django
│   │   ├── settings.py               # Settings: JWT, CORS, DB, apps instaladas
│   │   ├── urls.py                   # URLs raíz: auth, users, accounts, etc.
│   │   └── wsgi.py
│   ├── users/                         # App: registro, login, perfil, ocultar saldo
│   │   ├── models.py                 # Profile (rut, role, account_tier, hide_balance)
│   │   ├── views.py                  # RegisterView, LogoutView, ProfileView, ToggleBalanceView
│   │   ├── serializers.py            # RegisterSerializer, ProfileSerializer, UserSerializer
│   │   ├── signals.py                # Auto-crear Profile al registrar User
│   │   ├── urls.py                   # /api/auth/register, /api/auth/logout, /api/profile/
│   │   └── management/commands/
│   │       └── create_seed_data.py   # Datos de prueba: admin@duckbank.cl, juan@duckbank.cl
│   ├── accounts/                      # App: cuentas digitales
│   │   ├── models.py                 # Account (UUID, tipo, número, saldo, moneda)
│   │   ├── views.py                  # AccountListView, AccountDetailView
│   │   ├── serializers.py            # AccountSerializer con display_balance ('***' si hide_balance)
│   │   ├── signals.py                # Auto-crear "Cuenta Vista" con saldo inicial
│   │   └── urls.py                   # /api/accounts/
│   ├── transactions/                  # App: transferencias, depósitos, retiros, contactos
│   │   ├── models.py                 # Transaction + Contact
│   │   ├── views.py                  # TransferView (atómica), DepositView, WithdrawalView, ContactCRUD
│   │   ├── serializers.py            # TransactionSerializer, TransferSerializer, etc.
│   │   ├── signals.py                # Auto-actualizar saldo al crear transacción
│   │   └── urls.py                   # /api/transactions/, /api/transfers/, /api/deposits/, etc.
│   ├── savings/                       # App: cajitas de ahorro (11% anual compuesto)
│   │   ├── models.py                 # SavingsBox + SavingsBoxInterestLog
│   │   ├── views.py                  # CRUD cajitas, depositar, retirar, historial interés
│   │   ├── serializers.py            # SavingsBoxSerializer con projected_annual_earnings
│   │   ├── urls.py                   # /api/savings/
│   │   └── management/commands/
│   │       └── calculate_interest.py # Cron diario: balance * (1 + rate/36500)
│   ├── loans/                         # App: créditos, tarjetas, simulador
│   │   ├── models.py                 # Loan (amortización francesa) + Card (crédito/débito)
│   │   ├── views.py                  # LoanList, PayQuota, SimulateLoan, CardList, ToggleLock, PayCard
│   │   ├── serializers.py            # SimulateLoanSerializer con fórmula francesa
│   │   └── urls.py                   # /api/loans/, /api/cards/
│   ├── notifications/                  # App: notificaciones
│   │   ├── models.py                 # Notification (info/success/warning/error, is_read)
│   │   ├── views.py                  # List (filtro unread), MarkRead, MarkAllRead
│   │   ├── serializers.py
│   │   └── urls.py                   # /api/notifications/
│   ├── money_requests/                 # App: solicitar dinero P2P
│   │   ├── models.py                 # MoneyRequest (pending/accepted/rejected/expired)
│   │   ├── views.py                  # Create, Accept (transferencia atómica), Reject
│   │   ├── serializers.py
│   │   └── urls.py                   # /api/money-requests/
│   ├── .env                           # Variables de entorno (NO en git)
│   ├── requirements.txt               # Dependencias Python
│   └── manage.py
├── paradigmas/                         # 🎨 Frontend (HTML/CSS/JS)
│   ├── index.html                     # Dashboard Principal
│   ├── login.html                     # Inicio de Sesión
│   ├── register.html                  # Registro de Usuario
│   ├── forgot-password.html           # Recuperación de Contraseña
│   ├── transfers.html                 # Transferencias Monetarias
│   ├── savings.html                   # Cajitas de Ahorro
│   ├── cards.html                     # Tarjetas de Crédito
│   ├── loans.html                     # Gestión de Créditos
│   ├── simulator.html                 # Simulador de Préstamos
│   ├── investments.html               # Inversiones → redirige a cajitas
│   ├── applications.html              # Solicitud de Productos
│   ├── admin.html                     # Panel Administrativo
│   ├── css/                           # Estilos por página
│   └── js/
│       ├── api.js                     # 🌐 Cliente API (JWT, endpoints, manejo de tokens)
│       ├── auth.js                    # Login/registro/logout vía API
│       ├── common.js                  # Utilidades, formatCurrency(COP), toast, logout
│       ├── dashboard.js               # Carga cuentas, transacciones, notificaciones
│       ├── transfers.js               # Transferencias y contactos vía API
│       ├── savings.js                 # CRUD cajitas vía API
│       ├── cards.js                   # Tarjetas: listar, bloquear, pagar vía API
│       ├── loans.js                   # Créditos y pago de cuota vía API
│       ├── simulator.js               # Simulador: llama LoansAPI.simulate
│       ├── investments.js             # Redirige a savings (cajitas = MVP de inversión)
│       ├── applications.js            # Placeholder para solicitudes
│       └── admin.js                   # Verificación de rol admin
└── ESTUDIO_SUSTENTACION.txt           # 📝 Guía de estudio para sustentación
```

---

## 🏗️ Arquitectura

```
┌─────────────────┐       HTTP/JSON        ┌──────────────────────┐
│   Frontend      │ ◄──────────────────►   │   Backend Django      │
│   HTML/CSS/JS   │    REST API (JWT)      │   + DRF               │
│   paradigmas/   │                        │   backend/            │
└─────────────────┘                        └──────────┬───────────┘
                                                      │
                                           ┌──────────▼───────────┐
                                           │   Base de Datos      │
                                           │   SQLite (dev)       │
                                           │   PostgreSQL (prod)  │
                                           └──────────────────────┘
```

- **Frontend**: HTML5 + CSS3 + Vanilla JS, consume la API via `api.js` con JWT
- **Backend**: Django 5.x + Django REST Framework, 7 apps independientes
- **Auth**: JWT (access 60 min, refresh 1 día) con blacklist al logout
- **Moneda**: COP (Peso Colombiano), locale `es-CO`, timezone `America/Bogota`

---

## 🛠️ Apps del Backend

| App | Funcionalidad | Endpoints principales |
|-----|---------------|----------------------|
| `users` | Registro, login, logout, perfil, mostrar/ocultar saldo | `/api/auth/login/`, `/api/auth/register/`, `/api/profile/` |
| `accounts` | Cuentas digitales con saldo y alias | `/api/accounts/` |
| `transactions` | Transferencias (atómicas), depósitos, retiros, contactos | `/api/transfers/`, `/api/deposits/`, `/api/withdrawals/` |
| `savings` | Cajitas con interés compuesto 11% anual | `/api/savings/`, `/api/savings/{id}/deposit/` |
| `loans` | Préstamos, tarjetas, simulador de crédito | `/api/loans/`, `/api/cards/`, `/api/loans/simulate/` |
| `notifications` | Notificaciones por tipo, marcar leídas | `/api/notifications/` |
| `money_requests` | Solicitar dinero P2P, aceptar, rechazar | `/api/money-requests/` |

---

## 🚀 Cómo Ejecutar

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py create_seed_data    # Crea datos de prueba
python manage.py runserver           # http://127.0.0.1:8000
```

### Frontend

Abre `paradigmas/login.html` en el navegador (o usa Live Server en puerto 5500).

### Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|-----------|-----|
| `admin@duckbank.cl` | `admin123` | Administrador |
| `juan@duckbank.cl` | `juan123` | Usuario |

---

## 💰 Funcionalidades Clave

### Interés Compuesto (Cajitas)
- Tasa anual del **11%** con capitalización diaria
- Fórmula diaria: `balance × (1 + rate/36500)`
- Ganancia proyectada: `balance × ((1 + rate/365)^365 - 1)`
- Cron diario: `python manage.py calculate_interest`

### Simulador de Crédito (Amortización Francesa)
- Cuota mensual: `M = P × r × (1+r)^n / ((1+r)^n - 1)`
- Donde P = monto, r = tasa mensual, n = plazo en meses
- Muestra cuota, costo total y total de intereses

### Transferencias Atómicas
- Usa `@db_transaction.atomic` para garantizar consistencia
- Si falla cualquier paso, se revierte todo (rollback)

### Solicitudes de Dinero P2P
- Un usuario solicita dinero a otro por email
- Al aceptar: se ejecuta transferencia atómica + notificación automática
- Al rechazar: se envía notificación al solicitante

---

## 📋 API Endpoints Completos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login → JWT tokens |
| POST | `/api/auth/refresh/` | Renovar access token |
| POST | `/api/auth/register/` | Registro de usuario |
| POST | `/api/auth/logout/` | Logout (blacklist refresh) |
| GET/PATCH | `/api/profile/` | Ver/editar perfil |
| POST | `/api/profile/toggle-balance/` | Mostrar/ocultar saldo |
| GET | `/api/accounts/` | Listar cuentas |
| GET | `/api/accounts/{id}/` | Detalle de cuenta |
| GET/POST | `/api/transactions/` | Listar/crear transacciones |
| POST | `/api/transfers/` | Transferir dinero |
| POST | `/api/deposits/` | Depositar dinero |
| POST | `/api/withdrawals/` | Retirar dinero |
| GET/POST | `/api/contacts/` | Listar/crear contactos |
| DELETE | `/api/contacts/{id}/` | Eliminar contacto |
| GET/POST | `/api/savings/` | Listar/crear cajitas |
| GET | `/api/savings/{id}/` | Detalle de cajita |
| POST | `/api/savings/{id}/deposit/` | Depositar a cajita |
| POST | `/api/savings/{id}/withdraw/` | Retirar de cajita |
| GET | `/api/savings/{id}/interest-logs/` | Historial de intereses |
| GET | `/api/loans/` | Listar créditos |
| POST | `/api/loans/{id}/pay-quota/` | Pagar cuota |
| POST | `/api/loans/simulate/` | Simular crédito |
| GET | `/api/cards/` | Listar tarjetas |
| POST | `/api/cards/{id}/toggle-lock/` | Bloquear/desbloquear |
| POST | `/api/cards/{id}/pay/` | Pagar tarjeta |
| GET | `/api/notifications/` | Listar notificaciones |
| GET | `/api/notifications/?unread=true` | Solo no leídas |
| POST | `/api/notifications/{id}/read/` | Marcar como leída |
| POST | `/api/notifications/read-all/` | Marcar todas leídas |
| GET | `/api/money-requests/` | Listar solicitudes |
| POST | `/api/money-requests/create/` | Crear solicitud |
| POST | `/api/money-requests/{id}/accept/` | Aceptar solicitud |
| POST | `/api/money-requests/{id}/reject/` | Rechazar solicitud |

---

## 🔧 Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Backend | Python 3.13, Django 5.x, Django REST Framework |
| Auth | djangorestframework-simplejwt (JWT) |
| DB (dev) | SQLite |
| DB (prod) | PostgreSQL (psycopg2-binary) |
| CORS | django-cors-headers |
| Env | python-decouple |
| Cron | django-crontab |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |

---

## 📜 Licencia

Proyecto educativo — DuckBank © 2024
# 📦 Django Payments & Authentication Demo

This is a demonstration project built with **Django**, showcasing a complete and realistic application flow:

- user registration and authentication
- social login (Google / OpenID via Django Allauth)
- Stripe payments (new card and saved card)
- PayPal payments

The project is intentionally kept in a **simple and transparent stack**  
(Django templates + minimal JavaScript), without SPA frameworks.

---

## 🧱 Technology Stack

- Python **3.11+**
- Django **5.x**
- Django Allauth
- Stripe (Elements, token-based flow)
- Bootstrap / custom CSS
- jQuery

---

## 🔐 Authentication & User Accounts

### Django Allauth

The project uses **django-allauth** to handle:

- user registration
- login / logout
- password reset
- email address management
- authentication via external providers

### Enabled providers

- Google
- OpenID (optional)

---

### Social Applications (Admin)

Social providers are configured **exclusively via Django Admin**:

```
Admin → Social applications → Add
```

For Google:

- Provider: `Google`
- Client ID
- Secret
- Sites: assign to the active Site

⚠️ **Provider icons are NOT supplied by Allauth**  
SVGs / icons must be handled manually in the frontend.

---

## ✉️ Email (Feature Switch)

In local development, email sending is **disabled** to avoid SMTP issues.

Enable email sending via `.env`:

```env
EMAILS_ENABLED=1
```

Default (disabled):

```env
EMAILS_ENABLED=0
```

---

## 💳 Payments

### Feature Switch

Payments can be globally enabled/disabled via environment variable:

```env
PAYMENTS_ENABLED=1
```

Disable all payments (Stripe & PayPal):

```env
PAYMENTS_ENABLED=0
```

This allows safe local development without hitting payment providers.

---

### Stripe

Supported flows:

1. Saved card payment
2. New card payment (Stripe Elements)

Environment variables

```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

Frontend decisions

- Context-aware error handling
- Hidden forms ignored
- No duplicated DOM ids
- Multiple Stripe forms supported safely

---

### PayPal

PayPal integration is handled server-side with a redirect + execute flow.

Typical flow:

1. Create PayPal payment
2. Redirect user to PayPal
3. Execute payment on return
4. Validate ownership and status in backend

PayPal credentials must be configured in environment variables (sandbox or live).

---

## ▶️ Running the Project

The project uses **pyproject.toml**.

```sh
python -m venv venv
source venv/bin/activate
pip install .
```

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin panel:

```
http://127.0.0.1:8000/admin/
```

---

## 🧠 Notes

- No SPA framework by design
- Backend-driven flow
- Frontend kept explicit and debuggable
- Feature switches preferred over conditional logic

---

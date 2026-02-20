# Spots

> Curate and discover the best places through personalized, ranked lists.

![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?logo=amazonaws&logoColor=white)

---

## About

Spots is a social ranking platform where you create and share curated lists of your favorite places — restaurants, coffee shops, hikes, bookstores, or anywhere worth remembering. Browse trending lists from the community, follow friends, and build a living map of the spots that matter to you.

---

## Features

- **Email-verified accounts** — Secure sign-up flow backed by AWS Cognito with email verification
- **Flexible sign-in** — Log in with either your username or email address
- **Protected routes** — The home feed is only accessible to authenticated users

---

## Roadmap

- **Database integration** — Persist lists, spots, and user profiles
- **Create & rank lists** — Build ordered lists of your favorite spots with names, notes, and rankings
- **Friend activity feed** — See what spots and lists people you follow are sharing
- **Search** — Find spots and lists across the community

---

## Tech Stack

**Frontend**
- React
- TypeScript
- Vite
- Tailwind CSS
- Framer Motion
- React Router
- AWS Amplify

**Backend**
- FastAPI
- Uvicorn
- python-jose
- httpx
- python-dotenv

**Auth**
- AWS Cognito (User Pools, JWT verification via JWKS)

---

## Prerequisites

- **Node.js** >= 18 and **npm**
- **Python** >= 3.11
- An **AWS Cognito** User Pool with a public app client (no client secret)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/geoffrey0953/spots.git
cd spots
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```env
AWS_REGION=us-west-2
COGNITO_USER_POOL_ID=<your-user-pool-id>
```

### 3. Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:
```env
VITE_COGNITO_REGION=us-west-2
VITE_COGNITO_USER_POOL_ID=<your-user-pool-id>
VITE_COGNITO_APP_CLIENT_ID=<your-app-client-id>
```

---

## Running Locally

Open two terminals:

**Terminal 1 — Backend** (from `backend/` with venv active):
```bash
uvicorn main:app --reload
```

**Terminal 2 — Frontend** (from `frontend/`):
```bash
npm run dev
```

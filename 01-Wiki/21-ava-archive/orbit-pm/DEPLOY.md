# Orbit — Deployment Guide

## 1. Environment Setup
Create a `.env` file in the root directory:

```bash
# Database (Supabase Transaction Pooler URL)
DATABASE_URL="postgresql://postgres.[ref]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Direct Connection (for migrations)
DIRECT_URL="postgresql://postgres.[ref]:[password]@aws-0-us-east-1.supabase.co:5432/postgres"

# NextAuth
NEXTAUTH_SECRET="openssl rand -base64 32"
NEXTAUTH_URL="http://localhost:3000"
```

## 2. Install Dependencies
```bash
npm install
npm install @prisma/client
npm install -D prisma
```

## 3. Database Migration
Push the schema to your database:
```bash
npx prisma db push
```

## 4. Run Development Server
```bash
npm run dev
```

## 5. Production Build
```bash
npm run build
npm start
```

---
*Orbit Project Management System v1.0*

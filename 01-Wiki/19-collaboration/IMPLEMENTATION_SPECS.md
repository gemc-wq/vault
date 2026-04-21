# Ecell Tech — Implementation Specifications
## For Harry (Antigravity Development)

---

## Tech Stack Recommendation

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Next.js 14 (App Router) | SSR for SEO, API routes, React Server Components |
| **Styling** | Tailwind CSS | Already used in wireframes, rapid development |
| **UI Components** | shadcn/ui | Accessible, customizable, Tailwind-based |
| **Animation** | Framer Motion | Smooth interactions, gesture support |
| **CMS** | Sanity or Contentful | Flexible content management for marketing team |
| **Auth** | NextAuth.js + OAuth | SSO integration for B2B portal |
| **Database** | PostgreSQL (Supabase) | Reliable, scalable, good B2B fit |
| **File Storage** | AWS S3 or Cloudflare R2 | Product images, client assets |
| **Search** | Algolia | Product catalog search |

---

## Project Structure

```
app/
├── (marketing)/              # Public marketing pages
│   ├── page.tsx              # Homepage
│   ├── about/
│   ├── solutions/
│   │   ├── it-asset-protection/
│   │   ├── corporate-gifting/
│   │   └── license-partnerships/
│   ├── products/
│   ├── case-studies/
│   └── contact/
├── (portal)/                 # B2B Client Portal (auth required)
│   ├── dashboard/
│   ├── orders/
│   ├── quotes/
│   ├── users/               # Team management
│   └── settings/
├── (admin)/                  # Admin dashboard
│   ├── dashboard/
│   ├── orders/
│   ├── products/
│   ├── clients/
│   └── analytics/
├── api/                      # API routes
│   ├── auth/
│   ├── orders/
│   ├── quotes/
│   └── webhooks/
├── layout.tsx
└── globals.css

components/
├── ui/                       # shadcn components
├── marketing/                # Marketing page sections
│   ├── hero.tsx
│   ├── solutions-grid.tsx
│   ├── product-showcase.tsx
│   └── trust-bar.tsx
├── portal/                   # Portal components
└── shared/                   # Shared components

lib/
├── utils.ts
├── api.ts                    # API client
├── auth.ts                   # Auth helpers
└── constants.ts

types/
├── index.ts                  # TypeScript types

tailwind.config.ts
next.config.js
```

---

## Tailwind Config (Proposal A)

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary palette
        primary: {
          DEFAULT: "#0F4C81",
          light: "#3B82F6",
          dark: "#0A3A63",
          foreground: "#FFFFFF",
        },
        // Secondary
        graphite: {
          DEFAULT: "#2C3E50",
          light: "#3D5266",
          dark: "#1A252F",
        },
        // Tertiary
        steel: {
          DEFAULT: "#64748B",
          light: "#94A3B8",
          dark: "#475569",
        },
        // Accents
        success: {
          DEFAULT: "#10B981",
          light: "#34D399",
          dark: "#059669",
        },
        gold: {
          DEFAULT: "#D4AF37",
          light: "#E5C158",
          dark: "#B8941F",
        },
        // Backgrounds
        background: {
          light: "#FAFAF9",
          dark: "#1A1D23",
        },
        // shadcn defaults
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        foreground: "hsl(var(--foreground))",
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

---

## Key Components to Build

### 1. Navigation (`components/marketing/navbar.tsx`)
```typescript
// Features:
// - Glass-morphism background
// - Logo + nav items
// - CTA buttons
// - Mobile hamburger menu
// - Dark mode toggle
```

### 2. Hero Section (`components/marketing/hero.tsx`)
```typescript
// Features:
// - Animated headline
// - Badge stack (AI-First, Zero MOQ)
// - Dual CTAs
// - Equipment badges (Mimaki, Canon)
// - Hero image/video
```

### 3. Solutions Grid (`components/marketing/solutions-grid.tsx`)
```typescript
// Features:
// - Two-tier cards (Merchant vs Enterprise)
// - Feature lists with checkmarks
// - Hover animations
// - CTA buttons
```

### 4. Product Catalog (`components/marketing/product-showcase.tsx`)
```typescript
// Features:
// - 4-category grid
// - Hover zoom effects
// - Category icons
// - "AI READY" badges
```

### 5. Contact Form (`components/marketing/contact-form.tsx`)
```typescript
// Features:
// - Split layout (info + form)
// - Form validation
// - Volume dropdown
// - Submit handling
```

---

## Database Schema (Prisma)

```prisma
// schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// User model (B2B clients)
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  companyId     String
  company       Company   @relation(fields: [companyId], references: [id])
  role          UserRole  @default(MEMBER)
  orders        Order[]
  quotes        Quote[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

// Company model (B2B accounts)
model Company {
  id            String          @id @default(cuid())
  name          String
  domain        String?         @unique
  tier          CompanyTier     @default(MERCHANT)
  users         User[]
  orders        Order[]
  quotes        Quote[]
  addresses     Address[]
  settings      CompanySettings?
  createdAt     DateTime        @default(now())
  updatedAt     DateTime        @updatedAt
}

// Orders
model Order {
  id            String        @id @default(cuid())
  orderNumber   String        @unique
  companyId     String
  company       Company       @relation(fields: [companyId], references: [id])
  userId        String
  user          User          @relation(fields: [userId], references: [id])
  items         OrderItem[]
  status        OrderStatus   @default(PENDING)
  total         Decimal       @db.Decimal(10, 2)
  shippingAddress String
  trackingNumber String?
  createdAt     DateTime      @default(now())
  updatedAt     DateTime      @updatedAt
}

model OrderItem {
  id            String    @id @default(cuid())
  orderId       String
  order         Order     @relation(fields: [orderId], references: [id])
  productId     String
  product       Product   @relation(fields: [productId], references: [id])
  quantity      Int
  unitPrice     Decimal   @db.Decimal(10, 2)
  designUrl     String?   // Custom design file
}

// Products
model Product {
  id            String          @id @default(cuid())
  name          String
  slug          String          @unique
  category      ProductCategory
  description   String?
  basePrice     Decimal         @db.Decimal(10, 2)
  compatibleDevices String[]    // Device model IDs
  images        String[]
  orderItems    OrderItem[]
  isActive      Boolean         @default(true)
  createdAt     DateTime        @default(now())
  updatedAt     DateTime        @updatedAt
}

// Quotes (for enterprise)
model Quote {
  id            String        @id @default(cuid())
  quoteNumber   String        @unique
  companyId     String
  company       Company       @relation(fields: [companyId], references: [id])
  userId        String
  user          User          @relation(fields: [userId], references: [id])
  description   String
  estimatedVolume Int
  status        QuoteStatus   @default(PENDING)
  price         Decimal?      @db.Decimal(10, 2)
  validUntil    DateTime?
  createdAt     DateTime      @default(now())
  updatedAt     DateTime      @updatedAt
}

// Enums
enum UserRole {
  ADMIN
  MANAGER
  MEMBER
}

enum CompanyTier {
  MERCHANT
  WHOLESALE
  ENTERPRISE
}

enum OrderStatus {
  PENDING
  CONFIRMED
  IN_PRODUCTION
  SHIPPED
  DELIVERED
  CANCELLED
}

enum ProductCategory {
  PHONE_CASE
  TABLET_CASE
  LAPTOP_SLEEVE
  GAMING_SKIN
  AUDIO_CASE
}

enum QuoteStatus {
  PENDING
  REVIEWING
  APPROVED
  DECLINED
  EXPIRED
}
```

---

## API Endpoints

### Auth
- `POST /api/auth/signin` — SSO/OAuth login
- `POST /api/auth/signout` — Logout
- `GET /api/auth/session` — Get current session

### Orders
- `GET /api/orders` — List orders (filtered by company)
- `POST /api/orders` — Create order
- `GET /api/orders/:id` — Get order details
- `PATCH /api/orders/:id/status` — Update order status (admin)

### Quotes
- `GET /api/quotes` — List quotes
- `POST /api/quotes` — Request quote
- `GET /api/quotes/:id` — Get quote details
- `PATCH /api/quotes/:id` — Update quote (admin)

### Products
- `GET /api/products` — List products
- `GET /api/products/:slug` — Get product details
- `GET /api/products/compatible/:deviceId` — Get compatible products

### Webhooks
- `POST /api/webhooks/stripe` — Payment events
- `POST /api/webhooks/shipstation` — Shipping updates

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up Next.js project with shadcn
- [ ] Configure Tailwind with Proposal A colors
- [ ] Set up database (Supabase)
- [ ] Configure authentication (NextAuth)
- [ ] Deploy to Vercel staging

### Phase 2: Marketing Site (Week 2)
- [ ] Build all marketing page sections
- [ ] Implement responsive layouts
- [ ] Add dark mode
- [ ] Connect CMS for content
- [ ] Performance optimization

### Phase 3: Client Portal (Week 3-4)
- [ ] Authentication flow
- [ ] Dashboard UI
- [ ] Order management
- [ ] Quote request system
- [ ] User management (for admins)

### Phase 4: Admin & Polish (Week 5)
- [ ] Admin dashboard
- [ ] Order fulfillment workflow
- [ ] Analytics
- [ ] Testing & QA
- [ ] Production deployment

---

## Environment Variables

```bash
# Database
DATABASE_URL="postgresql://..."

# Auth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="..."
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."

# Storage
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_S3_BUCKET="ecell-global-assets"

# CMS
SANITY_PROJECT_ID="..."
SANITY_DATASET="production"
SANITY_API_TOKEN="..."

# Search
ALGOLIA_APP_ID="..."
ALGOLIA_API_KEY="..."

# Stripe (for payments)
STRIPE_SECRET_KEY="..."
STRIPE_WEBHOOK_SECRET="..."
```

---

## Performance Targets

- **Lighthouse Score:** 90+ across all categories
- **First Contentful Paint:** < 1.5s
- **Time to Interactive:** < 3s
- **Core Web Vitals:** All green

---

*Specifications prepared for Harry (Claude Opus 4.5)*
*Date: 2026-02-05*

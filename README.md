# SIMORA

## AI-Powered Business Decision Simulation Platform

> **Test the decision before you take the risk.**

SIMORA is an AI-powered business decision simulation platform designed to help merchants understand the potential impact of a business decision **before taking it in the real world**.

Instead of simply showing historical dashboards or generating generic AI advice, SIMORA creates a merchant-specific **Digital Twin** from business data and uses it to simulate different strategies, compare trade-offs, explain the reasoning, and learn from actual outcomes.

---

## The Core Idea

A merchant can ask a natural-language **"What if?"** question such as:

> **"What if I give 10% discount on headphones this weekend?"**

SIMORA transforms that question into a structured scenario, evaluates it against the merchant's historical business behavior, simulates multiple strategies, and presents the expected outcomes.

The merchant can then review the simulation, approve an action, execute it through an available workflow adapter, and later compare the prediction with the actual result.

### SIMORA Decision Loop

```text
        ┌───────────────┐
        │   SIMULATE    │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    COMPARE    │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    DECIDE     │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │      ACT      │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │     LEARN     │
        └───────┬───────┘
                │
                └──────────────→ Better future simulations
```

---

# Why SIMORA?

Traditional merchant dashboards answer:

> **"What happened?"**

Analytics tools can answer:

> **"What is happening?"**

SIMORA focuses on:

> **"What could happen if I make this decision?"**

The platform combines:

- Historical business data
- Merchant-specific behavioral patterns
- Digital Twin modeling
- Counterfactual simulation
- AI-powered scenario understanding
- Strategy comparison
- Risk analysis
- Confidence estimation
- Human approval
- Outcome tracking
- Business memory
- Model calibration

The goal is to turn business decisions into **virtual experiments** before committing real money, inventory, or margin.

---

# Key Features

## 1. Merchant Digital Twin

SIMORA builds a merchant-specific representation of business behavior from historical data.

The Digital Twin can derive signals such as:

- Product demand
- Price sensitivity
- Promotion response
- Weekend effects
- Seasonality
- Demand volatility
- Inventory velocity
- Stockout patterns
- Product relationships
- Revenue patterns
- Cost and margin behavior
- Historical promotional performance

The Digital Twin is generated from available evidence rather than relying on hardcoded business assumptions.

If there is not enough historical evidence for a particular behavior, SIMORA reports insufficient evidence and lowers confidence instead of inventing a value.

---

## 2. Natural-Language What-If Simulation

Merchants can describe a business decision naturally.

Examples:

```text
What if I give 10% discount on headphones this weekend?
```

```text
What happens if I increase the price of the keyboard by 5%?
```

```text
Should I run a bundle offer for mouse and keyboard?
```

```text
What if I promote speakers for the next 7 days?
```

SIMORA converts the request into a structured scenario.

---

## 3. Counterfactual Strategy Testing

SIMORA does not evaluate only one decision.

Depending on the scenario, it can generate meaningful alternatives such as:

- No change
- Smaller discount
- Requested discount
- Larger discount
- Bundle offer
- Alternative promotion
- Different duration
- Different product combination

Strategies are generated according to the scenario and selected business objective rather than using a fixed list for every simulation.

---

## 4. Revenue vs Profit Analysis

A decision that increases revenue does not necessarily increase profit.

SIMORA therefore evaluates multiple dimensions:

| Metric | Purpose |
|---|---|
| Units | Expected quantity sold |
| Revenue | Expected sales value |
| Cost | Expected business cost |
| Profit | Expected financial contribution |
| Margin | Profitability percentage |
| Inventory | Expected stock impact |
| Risk | Potential downside exposure |
| Confidence | Reliability of the prediction |

This helps merchants understand the trade-offs behind a decision.

---

## 5. Objective-Aware Decisions

Different merchants may optimize for different goals.

SIMORA can evaluate simulations against objectives such as:

- Maximize profit
- Maximize revenue
- Increase units sold
- Improve inventory turnover
- Minimize risk
- Balanced business objective

The system does not assume that one metric is always the correct objective.

---

## 6. Risk Analysis

SIMORA considers factors such as:

- Demand uncertainty
- Historical volatility
- Inventory exposure
- Margin compression
- Prediction uncertainty
- Scenario magnitude
- Similarity to historical situations

Risk is communicated using understandable levels and explanations rather than presenting an unexplained score.

---

## 7. Confidence & Uncertainty

SIMORA distinguishes between a strong historical signal and a weak prediction.

Confidence can depend on:

- Amount of historical data
- Data quality
- Scenario similarity
- Model uncertainty
- Prediction variance
- Historical consistency

Probabilistic simulations can provide ranges such as:

```text
P10 ───────── P50 ───────── P90
Low            Expected       High
```

Predictions are presented as estimates, not guarantees.

---

# AI Architecture

SIMORA separates AI reasoning from numerical business calculations.

```text
                  Merchant Question
                         │
                         ▼
                ┌─────────────────┐
                │ Gemini / Parser │
                │ Scenario Intent │
                └────────┬────────┘
                         │
                         ▼
                Structured Scenario
                         │
                         ▼
              ┌─────────────────────┐
              │    Digital Twin     │
              │ Historical Behavior │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Simulation Engine   │
              │ Demand / Pricing /  │
              │ Promotion / Stock   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Strategy Comparison │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ AI Explanation      │
              │ + Trade-offs        │
              └──────────┬──────────┘
                         │
                         ▼
                    Merchant
```

### Important separation

**Gemini / LLM**

Used for:

- Natural-language understanding
- Scenario extraction
- Structured intent
- Explanation
- Insight generation

The LLM should not invent financial metrics.

**Simulation Engine**

Responsible for:

- Demand estimation
- Revenue calculation
- Cost calculation
- Profit calculation
- Margin calculation
- Inventory impact
- Risk estimation
- Uncertainty
- Strategy comparison

This separation keeps financial calculations deterministic, testable, and explainable.

---

# Learning Loop

SIMORA does not stop after generating a prediction.

Once a merchant acts, the actual business outcome can be recorded.

```text
Prediction
    │
    ▼
Real Business Action
    │
    ▼
Actual Outcome
    │
    ▼
Predicted vs Actual
    │
    ▼
Error Analysis
    │
    ▼
Calibration
    │
    ▼
Business Memory
    │
    ▼
Better Future Simulations
```

SIMORA can track:

- Predicted units vs actual units
- Predicted revenue vs actual revenue
- Predicted cost vs actual cost
- Predicted profit vs actual profit
- Prediction error
- Percentage difference
- Calibration history
- Model version
- Digital Twin version

Calibration should use accumulated evidence rather than blindly changing the model after a single observation.

---

# Business Memory

SIMORA can maintain merchant-specific business memory using **Cognee**.

Memory can contain useful business knowledge such as:

- Historical decisions
- Observed outcomes
- Repeated patterns
- Merchant-specific behaviors
- Important product relationships
- Previous simulation insights
- Calibration information

If Cognee is unavailable, the application can fall back to local database-backed memory.

Business memory is intended to improve future decision simulations rather than act as generic chat history.

---

# Voice Interaction

SIMORA supports voice interaction through **ElevenLabs**.

Potential interactions include:

```text
Merchant speaks
      ↓
Scenario understood
      ↓
Simulation executed
      ↓
Results generated
      ↓
AI explanation
      ↓
Voice response
```

The application can also provide browser-based speech fallback when the external voice service is unavailable.

API credentials remain server-side.

---

# Human-in-the-Loop Execution

SIMORA is designed around a human approval step.

```text
Simulation
    ↓
Recommendation
    ↓
Merchant Review
    ↓
Approval
    ↓
Execution Adapter
    ↓
Outcome Tracking
```

The AI does not silently execute a financial or business action.

For demonstrations, a `DemoExecutor` can simulate execution.

Where available, an `N8NExecutor` can connect the approved action to an external workflow.

Demo execution must always be clearly identified as:

> **Simulated execution**

---

# Technology Stack

## Backend

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core backend language |
| FastAPI | API framework |
| Uvicorn | ASGI server |
| Pydantic v2 | Validation and schemas |
| SQLAlchemy 2.x | ORM |
| Alembic | Database migrations |
| SQLite | Local development |
| PostgreSQL | Production-compatible database |
| Pandas | Data processing |
| NumPy | Numerical computation |
| scikit-learn | Statistical/ML utilities |
| HTTPX | External API requests |
| Pytest | Testing |

## Frontend

| Technology | Purpose |
|---|---|
| React | UI |
| TypeScript | Type safety |
| Vite | Frontend tooling |
| Tailwind CSS | Styling |
| React Router | Routing |
| TanStack Query | API/server state |
| Recharts | Data visualization |
| Lucide React | Icons |
| React Hook Form | Forms |
| Zod | Validation |
| Framer Motion | Subtle animations |

## AI & Integrations

| Technology | Purpose |
|---|---|
| Gemini | Natural-language scenario understanding and explanations |
| Cognee | Business memory |
| ElevenLabs | Voice interaction |
| n8n | Optional workflow execution |
| Demo Executor | Safe hackathon/demo execution |

---

# Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                         SIMORA UI                             │
│                 React + TypeScript + Vite                    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ REST API
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                         │
├──────────────────────────────────────────────────────────────┤
│ Authentication │ Business │ Products │ Sales │ Analytics     │
│ Simulations    │ Decisions │ Outcomes │ Memory │ Insights     │
└──────────────────────────────┬───────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐  ┌──────────────┐
       │ Simulation │   │  Digital Twin│  │ AI Services  │
       │   Engine   │   │    Engine    │  │ Gemini       │
       └─────┬──────┘   └──────┬───────┘  │ ElevenLabs   │
             │                 │          │ Cognee       │
             └────────┬────────┘          └──────┬───────┘
                      │                          │
                      ▼                          ▼
               ┌──────────────┐          ┌──────────────┐
               │   Database   │          │ Integrations │
               │ SQLite/PG    │          │ n8n / Demo   │
               └──────────────┘          └──────────────┘
```

---

# Project Structure

```text
simora/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── business.py
│   │       ├── products.py
│   │       ├── sales.py
│   │       ├── dashboard.py
│   │       ├── simulation.py
│   │       ├── strategies.py
│   │       ├── decisions.py
│   │       ├── outcomes.py
│   │       ├── memory.py
│   │       ├── insights.py
│   │       ├── analytics.py
│   │       ├── voice.py
│   │       └── integrations.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models/
│   │   └── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── digital_twin_service.py
│   │   ├── simulation_service.py
│   │   ├── strategy_service.py
│   │   ├── ai_service.py
│   │   ├── memory_service.py
│   │   ├── voice_service.py
│   │   ├── outcome_service.py
│   │   ├── calibration_service.py
│   │   ├── insight_service.py
│   │   ├── analytics_service.py
│   │   └── workflow_service.py
│   │
│   ├── simulation/
│   │   ├── demand_model.py
│   │   ├── pricing_model.py
│   │   ├── promotion_model.py
│   │   ├── inventory_model.py
│   │   ├── risk_model.py
│   │   ├── monte_carlo.py
│   │   └── engine.py
│   │
│   ├── integrations/
│   │   ├── gemini.py
│   │   ├── elevenlabs.py
│   │   ├── cognee.py
│   │   └── n8n.py
│   │
│   └── tests/
│
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── pages/
│       ├── layouts/
│       ├── hooks/
│       ├── services/
│       ├── api/
│       ├── types/
│       ├── utils/
│       ├── charts/
│       └── styles/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── simulation-model.md
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# Database Model

SIMORA is designed around a relational data model.

Core entities include:

- User
- Business
- MerchantProfile
- Product
- SalesRecord
- InventoryRecord
- Promotion
- Simulation
- SimulationScenario
- SimulationStrategy
- SimulationResult
- Decision
- DecisionApproval
- WorkflowExecution
- Outcome
- Prediction
- MemoryRecord
- Insight
- DigitalTwinSnapshot
- ModelCalibration
- AuditLog
- IntegrationStatus
- Notification

Important database requirements:

- UUID identifiers
- Foreign-key relationships
- Timestamps
- Indexes
- Constraints
- Transactions
- Business-level data isolation
- Soft deletion where appropriate
- Alembic migrations

---

# Data Import

SIMORA should support merchant data through CSV import.

The import flow should provide:

```text
Upload CSV
    ↓
Preview
    ↓
Column Mapping
    ↓
Validation
    ↓
Data Quality Report
    ↓
Import
    ↓
Digital Twin Generation
```

Potential fields include:

- Date
- Product
- Quantity
- Unit price
- Unit cost
- Discount
- Revenue
- Inventory

The system should handle flexible column names through mapping rather than assuming one exact CSV format.

---

# Demo Merchant

For demonstrations, SIMORA can provide a synthetic merchant:

### Rajesh Electronics

Example products:

1. Headphones
2. Keyboard
3. Mouse
4. Smartwatch
5. Speaker
6. Monitor

The demo dataset can contain several months of synthetic historical sales data.

> **Demo data is simulated for prototype purposes.**

The simulation engine should still calculate results dynamically from the underlying dataset instead of displaying hardcoded outcomes.

---

# Simulation Engine

The simulation engine is the numerical core of SIMORA.

A simulation receives:

```text
Digital Twin
+
Historical Data
+
Product State
+
Scenario
+
Strategy
+
Objective
```

and produces:

```text
Projected Units
Projected Revenue
Projected Cost
Projected Profit
Projected Margin
Inventory Impact
Risk
Confidence
Prediction Range
Assumptions
Historical Evidence
```

### Example

Scenario:

```text
10% discount
Headphones
Weekend
3 days
```

Possible strategy comparison:

```text
Baseline
5% Discount
10% Discount
Bundle Offer
```

The actual strategies should be generated based on the scenario.

---

# Probabilistic Simulation

Where sufficient data exists, SIMORA can model uncertainty through probabilistic or Monte Carlo simulation.

Conceptually:

```text
                 Historical Data
                       │
                       ▼
               Demand Distribution
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        P10          P50          P90
          │            │            │
          └────────────┼────────────┘
                       ▼
                Result Range
```

This makes uncertainty visible instead of presenting a single number as a guaranteed outcome.

---

# Explainability

Every important simulation should answer:

> **Why did SIMORA predict this?**

Explanations can reference:

- Historical sales behavior
- Demand response
- Price sensitivity
- Promotion history
- Seasonality
- Inventory constraints
- Margin impact
- Product relationships
- Business memory
- Model assumptions
- Data quality
- Confidence limitations

The explanation should be tied to actual simulation evidence.

---

# Dashboard

The dashboard provides a business-level overview.

Typical areas include:

- Revenue
- Profit
- Units sold
- Average order value
- Margin
- Inventory turnover
- Recent decisions
- Recent simulations
- Business insights
- Quick simulation entry

A merchant should be able to move from:

```text
Dashboard
    ↓
Ask What-If Question
    ↓
Simulation Workspace
```

without navigating through unnecessary screens.

---

# Simulation Workspace

The simulation experience is the core user workflow.

Suggested structure:

```text
Scenario Input
       ↓
Scenario Understanding
       ↓
Digital Twin Context
       ↓
Simulation Progress
       ↓
Strategy Comparison
       ↓
Recommendation / Trade-offs
       ↓
Explainability
       ↓
Merchant Approval
       ↓
Execution
```

The interface should make the reasoning visible without overwhelming the merchant.

---

# Main Application Pages

```text
/
├── /login
├── /register
├── /onboarding
├── /import
├── /dashboard
├── /simulate
├── /simulations/:id
├── /strategies
├── /decisions
├── /decisions/:id
├── /outcomes
├── /memory
├── /insights
├── /products
├── /analytics
└── /settings
```

---

# UI / UX Design

SIMORA uses a premium light fintech/SaaS design language.

### Visual direction

- White / slate backgrounds
- Deep navy typography
- Electric blue primary actions
- Subtle green, amber and red semantic states
- Thin borders
- Soft shadows
- Rounded cards
- Clean data visualization
- Inter-style typography
- Lucide icons
- Responsive layouts

Avoid:

- Cyberpunk aesthetics
- Excessive neon
- Excessive gradients
- Heavy glassmorphism
- Decorative UI that reduces usability
- Fake AI animations

The design should communicate:

> **Trust + Intelligence + Business Control**

---

# Core UI Components

Reusable components should include:

- Button
- Input
- Select
- Textarea
- Modal
- Drawer
- Card
- Badge
- Tooltip
- Tabs
- Dropdown
- Toast
- MetricCard
- ChartCard
- StrategyCard
- RiskBadge
- ConfidenceBadge
- StatusBadge
- DataTable
- EmptyState
- LoadingState
- ErrorState
- VoiceButton
- SimulationProgress
- InsightCard
- Timeline
- ApprovalCard

---

# Security

SIMORA should follow secure application practices.

### API keys

Never expose API keys in the frontend.

Use environment variables:

```env
GEMINI_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
COGNEE_API_KEY=
```

### Authentication

- Password hashing
- Protected routes
- Session/JWT-based authentication
- Business-level authorization
- Secure logout
- Input validation

### Application security

- CORS configuration
- Request validation
- Safe error responses
- Rate limiting where appropriate
- Audit logging
- Secret management
- Multi-tenant data isolation

Never commit real credentials to Git.

---

# Environment Configuration

Create a `.env` file locally.

Example:

```env
PORT=8000
HOST=0.0.0.0
DEBUG=True

DATABASE_URL=sqlite:///./simora.db

GEMINI_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
COGNEE_API_KEY=
```

Use `.env.example` for the repository.

Never commit:

```text
.env
```

or real API credentials.

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd simora
```

## 2. Backend

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the backend from the project root:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Build for production:

```bash
npm run build
```

---

# Testing

Run backend tests:

```bash
pytest
```

The test suite should cover:

- Authentication
- Business isolation
- CSV import
- Data validation
- Digital Twin generation
- Scenario parsing
- Simulation calculations
- Strategy comparison
- Risk calculation
- Confidence calculation
- Approval flow
- Outcome tracking
- Calibration
- Memory fallback
- Gemini fallback
- ElevenLabs fallback

Dynamic tests should verify that simulation results change when:

- Price changes
- Inventory changes
- Historical data changes
- Discount changes
- Scenario duration changes
- Business objective changes

This helps prevent hardcoded simulation results.

---

# API Overview

Representative API areas:

```text
/auth
/business
/products
/sales
/dashboard
/simulation
/strategies
/decisions
/outcomes
/memory
/insights
/analytics
/voice
/integrations
```

The backend should expose OpenAPI documentation through FastAPI.

---

# Example End-to-End Flow

A complete demonstration can follow this flow:

```text
1. Register
       ↓
2. Create Merchant Business
       ↓
3. Load Demo Data
       ↓
4. Generate Digital Twin
       ↓
5. Open Dashboard
       ↓
6. Ask:
   "What if I give 10% discount
    on headphones this weekend?"
       ↓
7. Gemini parses scenario
       ↓
8. Digital Twin provides context
       ↓
9. Simulation Engine runs strategies
       ↓
10. Compare projected outcomes
       ↓
11. Show trade-offs
       ↓
12. Explain why the results differ
       ↓
13. Merchant approves decision
       ↓
14. Demo / n8n execution
       ↓
15. Record decision
       ↓
16. Record actual outcome
       ↓
17. Compare predicted vs actual
       ↓
18. Update calibration
       ↓
19. Store business memory
       ↓
20. Improve future simulations
```

---

# Responsible AI Principles

SIMORA should not present predictions as guarantees.

Use language such as:

- Projected
- Estimated
- Expected
- Simulation indicates
- Based on historical evidence
- Confidence is limited by available data

Avoid:

- Guaranteed profit
- Guaranteed sales
- Certain outcome
- Unexplained AI scores

When evidence is insufficient, SIMORA should say so.

---

# Production Readiness

The project should be structured so that it can move beyond a hackathon demo.

Recommended production preparation:

- PostgreSQL compatibility
- Docker support
- Environment-based configuration
- Database migrations
- API documentation
- Structured logging
- Request IDs
- Error categorization
- Secure authentication
- Business isolation
- Automated tests
- Health checks
- Integration status monitoring
- Versioned Digital Twin snapshots
- Versioned simulation models
- Audit logs

---

# Model Versioning

Simulation results should retain enough information to reproduce or understand a previous decision.

A simulation can record:

```text
simulation_id
model_version
digital_twin_version
data_range
scenario
strategy
objective
assumptions
random_seed
created_at
```

This makes historical decisions auditable and easier to compare after the underlying model changes.

---

# Hackathon Context

**Hackathon:** Paytm Build for India AI Hackathon — Delhi Edition

**Team:** Kinetix

**Project:** SIMORA

**Track:** Merchant Growth AI

SIMORA is designed around the idea of an AI business partner that helps merchants make more informed decisions using their own business data.

The project also demonstrates how partner technologies can contribute:

- **Gemini** — AI reasoning and scenario understanding
- **Cognee** — merchant business memory
- **ElevenLabs** — voice interaction
- **n8n** — optional workflow automation

---

# Demo Story

Imagine a merchant preparing for a weekend promotion.

Instead of immediately changing the price, the merchant asks:

> **"What if I give 10% discount on headphones this weekend?"**

SIMORA checks the merchant's historical behavior, builds the scenario, evaluates the available evidence, and runs multiple strategies.

The merchant can see:

```text
Baseline
vs
5% Discount
vs
10% Discount
vs
Alternative Strategy
```

The system explains:

- Expected demand change
- Revenue impact
- Profit impact
- Margin impact
- Inventory impact
- Risk
- Confidence
- Supporting historical evidence

The merchant decides whether to approve the action.

After the real-world result becomes available, SIMORA compares:

```text
Predicted
    vs
Actual
```

and stores the learning for future simulations.

That creates a continuous decision intelligence loop.

---

# Roadmap

## Phase 1 — Foundation

- FastAPI backend
- React frontend
- Database
- Authentication
- Project structure
- Configuration

## Phase 2 — Merchant Data

- Business profile
- Product management
- CSV import
- Historical sales
- Inventory

## Phase 3 — Digital Twin

- Historical analysis
- Demand behavior
- Pricing behavior
- Promotion behavior
- Inventory behavior
- Data quality
- Confidence

## Phase 4 — Simulation Engine

- Scenario parsing
- Strategy generation
- Demand modeling
- Pricing modeling
- Promotion modeling
- Inventory modeling
- Risk
- Uncertainty
- Monte Carlo simulation

## Phase 5 — AI Layer

- Gemini
- Structured scenario extraction
- Explanations
- AI-generated insights
- Fallback parser

## Phase 6 — Decision System

- Strategy comparison
- Recommendation context
- Merchant approval
- Execution adapter
- Decision history

## Phase 7 — Learning

- Actual outcomes
- Prediction error
- Calibration
- Business memory
- Cognee integration

## Phase 8 — Intelligence

- Analytics
- Product insights
- Business insights
- Trend detection
- Historical decision analysis

## Phase 9 — Voice

- ElevenLabs integration
- Voice responses
- Voice scenario input
- Browser fallback

## Phase 10 — Production

- PostgreSQL
- Docker
- Security hardening
- Observability
- Automated testing
- Deployment

---

# Project Philosophy

SIMORA is built around one principle:

> **AI should help merchants understand the consequences of a decision, not blindly make the decision for them.**

The system combines:

```text
Business Data
      +
Digital Twin
      +
Simulation
      +
AI Understanding
      +
Human Approval
      +
Real Outcome
      +
Learning
```

to create a continuous business decision intelligence system.

---

# Team

## Kinetix

**Project:** SIMORA

**Team Members:**

- Shreya Gupta — Team Leader
- Soumya Kushwah — Member

---

# License

Add the project's chosen license here.

For example:

```text
MIT License
```

if the project is released under MIT.

---

# Contributing

Contributions are welcome.

Suggested workflow:

```bash
git checkout -b feature/your-feature
```

Make changes, add tests, then open a pull request.

Before submitting:

```bash
pytest
npm run build
```

Ensure that:

- No secrets are committed
- New APIs are documented
- Business logic has tests
- UI states handle loading and errors
- Simulation calculations remain deterministic/reproducible where intended
- User/business data remains isolated

---

# Final Vision

SIMORA aims to evolve from a hackathon prototype into a merchant decision intelligence platform where business owners can ask:

> **"What happens if I do this?"**

and receive:

```text
Evidence
+
Simulation
+
Trade-offs
+
Risk
+
Confidence
+
Explanation
+
Human Control
+
Learning
```

before making the real decision.

## SIMORA

### **Test the decision before you take the risk.**

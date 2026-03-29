# Product Requirements Document (PRD)
## Epilepsy Management Platform (EMP)

> **Status**: Draft — Awaiting Review  
> **Version**: 0.1  
> **Date**: 2026-03-29  

---

## 1. Product Definition

### 1.1 What Is Being Built

The **Epilepsy Management Platform (EMP)** is a privacy-first, web-based medical decision-support system that predicts a patient's seizure risk by combining machine-learning analysis of electroencephalogram (EEG) signals with real-time lifestyle data (sleep, stress, medication adherence).

### 1.2 Who It Is For

| User Persona | Role | Core Need |
|---|---|---|
| **Neurologist / Clinician** | Primary user | Monitor assigned epilepsy patients, review risk trends, simulate risk scenarios, and take proactive clinical action. |
| **Epilepsy Patient** | Secondary user | Log daily lifestyle data, view personal risk status, and track their own health trends. |
| **ML / Data Team** | Internal operator | Retrain the XGBoost model on new EEG data and deploy updated model artefacts. |
| **Healthcare IT / Admin** | System operator | Manage user accounts, configure Supabase, and ensure HIPAA/GDPR compliance. |

### 1.3 Problem Statement

Epilepsy affects ~50 million people worldwide. Seizure prediction remains difficult because risk is multi-factorial — influenced by both neurological baseline (EEG) and daily behaviour. Clinicians currently lack real-time, data-driven tools to monitor patient risk between appointments. EMP bridges this gap by providing an always-on, ML-powered risk monitoring layer that respects patient privacy.

---

## 2. Feature List

Each feature is described in **behavioural terms**: what the user does, what the system does, and what outcome is produced.

---

### 2.1 Authentication & Role-Based Access

**F-01 — User Login**  
When a clinician or patient visits the platform and enters valid credentials, the system authenticates them via Supabase Auth, issues a JWT containing their role (`clinician` or `patient`), and redirects them to their role-specific dashboard. Invalid credentials produce a clear error message without revealing whether the email or password was wrong.

**F-02 — User Registration**  
When an administrator creates a new account, the system stores the user in Supabase Auth with the correct role claim and creates the corresponding bridge-table record linking auth identity to the medical record. Self-registration is not permitted for clinicians.

**F-03 — Role Enforcement**  
When any API request is made, FastAPI middleware validates the bearer token and rejects requests where the caller's role does not match the required permission for that endpoint (HTTP 403). Supabase Row Level Security provides a second enforcement layer at the database level.

**F-04 — Session Management**  
When a user's JWT expires, the system transparently refreshes the token if the user is still active, or redirects to the login page if the session has ended.

---

### 2.2 Patient Management (Clinician)

**F-05 — Patient List**  
When a clinician opens their dashboard, the system displays a list of patients assigned to them — showing name, medical record number (MRN), diagnosis, and current risk level — fetched via the `/patients/` endpoint. No patients belonging to other clinicians are visible.

**F-06 — Patient Detail View**  
When a clinician selects a patient, the system displays full patient demographics, recent lifestyle logs, historical risk predictions, and EEG baseline metadata.

**F-07 — Create Patient Record**  
When a clinician registers a new patient, the system creates a record in the `patients` table (medical data) and a corresponding row in `patient_accounts` (bridge table) without storing any PII in the medical tables.

---

### 2.3 Lifestyle Data Logging (Patient)

**F-08 — Daily Log Entry**  
When a patient submits their daily log, the system stores the entry in the `logs` table with the following fields: date, sleep hours, stress level (1–10 integer), and medication taken (boolean). The system confirms successful submission. Duplicate entries for the same patient on the same date are rejected.

**F-09 — Log History View**  
When a patient views their log history, the system displays a chronological list of past entries with the ability to scroll or paginate through previous records.

---

### 2.4 Seizure Risk Prediction (ML Engine)

**F-10 — Real-Time Risk Prediction**  
When a clinician or the system triggers a prediction for a patient, the backend loads the patient's pre-computed baseline EEG features from `master_eeg_features.csv`, merges them with the latest lifestyle log values to form a 68-dimensional feature vector, passes the vector to the XGBoost model, and returns a risk score (0–1 probability) with a categorical label (Low / Moderate / High).

**F-11 — SHAP Explainability**  
When a risk prediction is returned, the system also provides SHAP (SHapley Additive exPlanations) feature-importance values so the clinician can understand which factors (e.g., poor sleep, elevated stress) drove the score.

**F-12 — Risk Scenario Simulation (Clinician)**  
When a clinician adjusts lifestyle parameters in the Control Panel (e.g., changes sleep hours from 6 to 8), the system re-runs the prediction with the modified values and displays the updated risk score in real time, without writing to the database. This allows "what-if" exploration without affecting patient records.

**F-13 — Historical Risk Trend**  
When a clinician views the patient detail page, the system displays a line/area chart of risk scores over time, allowing identification of patterns (e.g., worsening risk correlated with reduced sleep).

---

### 2.5 Clinician Dashboard

**F-14 — Risk Card Summary**  
When the dashboard loads, the system renders a `RiskCard` component for each assigned patient showing current risk level (colour-coded: green/amber/red), last prediction timestamp, and a spark-line of recent trend.

**F-15 — Control Panel**  
When a clinician opens the Control Panel for a patient, the system presents sliders/inputs for sleep hours, stress level, and medication adherence, pre-filled with the patient's latest log values. Changing any value immediately triggers F-12 (scenario simulation).

---

### 2.6 Patient Dashboard

**F-16 — Personal Risk View**  
When a patient logs in, the system displays their most recent risk score, the contributing lifestyle factors, and a short plain-language explanation of the result (avoiding clinical jargon).

**F-17 — Profile View**  
When a patient selects their profile, the system displays their demographics (name, date of birth, diagnosis) in read-only form.

---

### 2.7 ML Training Pipeline

**F-18 — EEG Feature Extraction**  
When a data engineer runs `main_pipeline.py`, the system reads raw EDF files from `data/raw/eeg/`, applies a 0.5–50 Hz bandpass filter via MNE-Python, extracts 64 frequency-domain features per EEG channel, aggregates them to patient-level baselines, and writes the result to `data/processed/master_eeg_features.csv`.

**F-19 — Model Training & Export**  
When feature extraction is complete, the pipeline trains an XGBoost classifier on the processed dataset and exports the model to `models/foundation_model_v1.ubj`. Upon successful export the model file is automatically copied to `../backend-api/app/ml_engine/` so the backend can load it on next restart.

**F-20 — CSV / Manual Input Simulation Modes**  
When the backend is started in simulation mode, the system can source patient data from CSV files (`backend-api/csv_data/`) instead of live database records, enabling development and testing without a Supabase connection.

---

## 3. Technical Requirements

### 3.1 Technology Stack

| Layer | Technology | Version / Notes |
|---|---|---|
| **Patient Frontend** | React + TypeScript | React 18; built with Vite |
| **Clinician Dashboard** | React + TypeScript | React 18; built with Vite |
| **Styling** | TailwindCSS | Utility-first CSS |
| **Data Visualisation** | Recharts | Risk trend charts, spark-lines |
| **State Management** | React Context API | `AuthContext` for session state |
| **Backend API** | FastAPI | Python 3.11+ |
| **Dependency Management** | Poetry | `pyproject.toml` |
| **ML Framework** | XGBoost | Model serialised as `.ubj` |
| **ML Explainability** | SHAP | Feature-importance values |
| **Data Processing** | Pandas + NumPy | Feature engineering |
| **EEG Processing** | MNE-Python | EDF file parsing, bandpass filtering |
| **ML Pipeline Runtime** | Conda / pip | `environment.yml` or `requirements.txt` |

### 3.2 Database

| Component | Technology | Notes |
|---|---|---|
| **Primary Database** | Supabase (PostgreSQL) | Hosted; free tier supported |
| **Authentication** | Supabase Auth | JWT with custom role claims |
| **File Storage** | Supabase Storage | EDF files |
| **ORM / Client** | Supabase Python client (backend); Supabase JS client (frontend) | |

**Core Tables**

| Table | Purpose |
|---|---|
| `auth.users` | Managed by Supabase Auth; stores email and role |
| `patients` | Medical records — no PII from `auth.users` |
| `patient_accounts` | Bridge table linking `auth.users.id` ↔ `patients.patient_id` |
| `logs` | Daily lifestyle logs per patient |

**Row Level Security (RLS)** must be enabled on all tables. Clinicians may only read patients assigned to them; patients may only read/write their own records.

### 3.3 External APIs & Services

| Service | Purpose | Auth Method |
|---|---|---|
| Supabase REST/Realtime API | Data persistence and auth | `SUPABASE_URL` + `SUPABASE_KEY` (service role key for backend; anon key for frontend) |
| Supabase Auth | User identity, JWT issuance | Managed internally |
| CHB-MIT Scalp EEG Database | Training data source (offline) | Public dataset — no API key required |

No third-party payment, notification, or external ML inference APIs are required in v1.

### 3.4 Infrastructure & Deployment

- **Backend**: FastAPI served via `uvicorn`, port 8000. Stateless; horizontally scalable.
- **Clinician Dashboard**: Vite dev server on port 5173 (development); static build for production.
- **Patient Frontend**: Vite dev server on port 5174 (development); static build for production.
- **Transport Security**: TLS 1.3 for all data in transit. Supabase encrypts data at rest.

### 3.5 Browser Support

| Browser | Minimum Version |
|---|---|
| Google Chrome | Latest 2 major versions |
| Mozilla Firefox | Latest 2 major versions |
| Microsoft Edge (Chromium) | Latest 2 major versions |
| Safari | Latest 2 major versions |

Mobile browser support is desirable but not required for v1. The interfaces should be responsive at a minimum viewport width of 1024 px for the clinician dashboard and 375 px for the patient frontend.

### 3.6 Runtime Prerequisites

| Prerequisite | Minimum Version |
|---|---|
| Node.js | 18+ |
| npm | Bundled with Node 18+ |
| Python | 3.11+ |
| Poetry | Latest stable |
| Conda (optional) | For ML pipeline only |

---

## 4. Interface Parameters

### 4.1 Visual Style

- **Design language**: Clinical, clean, minimal. Prioritise readability and information density over decorative elements.
- **Colour palette**:
  - Risk levels: Green (Low), Amber/Orange (Moderate), Red (High) — consistent across all components.
  - UI chrome: Neutral whites, light greys, and a primary accent colour (to be confirmed in design review).
- **Typography**: System UI font stack or a neutral sans-serif (e.g., Inter). Body text ≥ 14 px; chart labels ≥ 12 px.
- **Spacing**: TailwindCSS default spacing scale; consistent padding within cards and panels.
- **Accessibility**: WCAG 2.1 AA colour contrast for text and interactive elements.

### 4.2 Layout Decisions

**Clinician Dashboard**
- Top navigation bar: logo, current user name, logout.
- Left sidebar or top tab bar: navigation between Patient List, individual patient views.
- Main content area: Patient List renders a grid/list of `RiskCard` components. Patient detail renders a two-column layout (patient info + charts on the left; Control Panel on the right).

**Patient Frontend**
- Single-column mobile-friendly layout.
- Top section: current risk score prominently displayed (large number or gauge).
- Middle section: today's log form or log history toggle.
- Bottom section: profile information.

### 4.3 Interaction Model

- **Risk Scenario Simulation**: Sliders or numeric inputs in the Control Panel update the predicted risk score with low latency (target < 500 ms round-trip) on every change. No explicit "submit" button needed for simulation — changes are ephemeral.
- **Daily Log Submission**: Explicit "Save" button. A success toast/snackbar confirms the save. Validation errors appear inline below the relevant field.
- **Patient Selection**: Clicking a patient row or card navigates to that patient's detail view. Browser back button returns to the patient list.
- **Data Refresh**: Patient data and risk predictions refresh automatically when the page loads. A manual "Refresh" button is acceptable but not mandatory for v1.
- **Loading States**: Skeleton screens or spinner overlays must be displayed while data is being fetched to prevent layout shift.
- **Error States**: API errors surface as dismissible banner or inline message with a human-readable explanation and a retry option.

---

## 5. Feature Completion Criteria

A feature is considered **complete** when all of the following conditions are met:

### 5.1 General Criteria (All Features)

| # | Criterion |
|---|---|
| GC-1 | The feature behaves as described in Section 2 under all documented input conditions. |
| GC-2 | All related API endpoints return correct HTTP status codes (2xx success, 4xx client error, 5xx server error) and response bodies matching the documented schema. |
| GC-3 | Role enforcement is verified: users without the required role cannot access the feature (HTTP 403 / UI gate). |
| GC-4 | No PII from `auth.users` leaks into API responses that return medical data. |
| GC-5 | The feature has automated tests (unit and/or integration) with ≥ 80% code coverage for new code paths. |
| GC-6 | The feature has been reviewed by at least one other developer and the PR has been approved. |
| GC-7 | No P0 or P1 bugs are open against the feature. |

### 5.2 Feature-Specific Criteria

| Feature | Done When… |
|---|---|
| **F-01 Login** | Valid credentials redirect the user to their dashboard within 3 seconds; invalid credentials show an error and do not redirect. |
| **F-03 Role Enforcement** | Automated tests confirm that a patient JWT cannot access clinician-only endpoints, and vice versa. |
| **F-08 Daily Log** | Duplicate log entries for the same patient + date return HTTP 409; the UI displays a clear duplicate warning. |
| **F-10 Risk Prediction** | The `/ml/predict` endpoint returns a valid risk score and label for all registered patients with at least one log entry. Response time ≤ 2 seconds (p95). |
| **F-11 SHAP Explainability** | The prediction response includes a non-empty `shap_values` object; the UI renders at least the top 5 contributing features. |
| **F-12 Scenario Simulation** | Changing a slider in the Control Panel updates the displayed risk score within 500 ms (p95) without creating a database record. |
| **F-13 Historical Trend** | The chart renders correctly with 0 data points (empty state), 1 data point, and > 30 data points. |
| **F-18 EEG Extraction** | Running `main_pipeline.py` produces a `master_eeg_features.csv` with the expected 64 frequency-domain features per channel for all patients in the training dataset; no EDF file is skipped without logging a warning. |
| **F-19 Model Training** | The trained model achieves Accuracy ≥ 85%, Recall ≥ 87%, and AUC-ROC ≥ 0.90 on the held-out validation set. The `.ubj` file is automatically copied to the backend directory. |
| **F-20 Simulation Mode** | The backend starts without a Supabase connection when `SIMULATION_MODE=true` is set and serves predictions from CSV data. |

### 5.3 Security Acceptance Criteria

| # | Criterion |
|---|---|
| SC-1 | All endpoints reject requests with missing or expired JWTs with HTTP 401. |
| SC-2 | Supabase RLS policies are verified by integration tests that attempt cross-user data access and confirm rejection. |
| SC-3 | No secrets (`SUPABASE_KEY`, `SUPABASE_JWT_SECRET`) are committed to source control. |
| SC-4 | All data in transit uses HTTPS (TLS 1.3). |

---

## 6. Out of Scope (v1)

The following items are explicitly **not** included in v1 and should not be built or implied:

- FDA approval or clinical certification process
- Real-time EEG streaming from hardware devices
- Push notifications or alerting (SMS, email, pager)
- Native mobile applications (iOS / Android)
- Multi-tenancy / multi-hospital support
- Billing or payment integration
- Offline / PWA support
- Automated patient self-registration

---

## 7. Open Questions

| # | Question | Owner | Due |
|---|---|---|---|
| OQ-1 | What is the target deployment environment (cloud provider, containerisation)? | Engineering Lead | TBD |
| OQ-2 | Should patients be able to edit or delete past log entries? | Product Owner | TBD |
| OQ-3 | What is the data retention policy for logs and predictions? | Legal / Compliance | TBD |
| OQ-4 | Is real-time (WebSocket) risk update required, or is polling acceptable? | Product Owner | TBD |
| OQ-5 | Which primary accent colour should be used in the UI? | Design | TBD |
| OQ-6 | Are there internationalisation (i18n) requirements for v1? | Product Owner | TBD |

---

*This document is a working draft. Please add comments and proposed changes for review before the next planning session.*

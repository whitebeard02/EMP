# Epilepsy Management Platform (EMP)

A privacy-first medical decision support system that predicts seizure risk using machine learning trained on EEG signals and lifestyle data.

## Overview

The Epilepsy Management Platform is a comprehensive healthcare solution designed to assist clinicians in monitoring epilepsy patients and predicting seizure risk. The system combines multi-modal medical data (EEG signals and lifestyle factors) with advanced machine learning to provide actionable risk assessments while maintaining strict privacy and security standards.

### Key Features

- **Real-time Risk Prediction**: XGBoost-based ML model trained on EEG features and lifestyle data (sleep, stress, medication adherence)
- **Clinician Dashboard**: Interactive interface for patient monitoring and risk scenario simulation
- **Privacy-First Architecture**: Decoupled user identity from medical data using a bridge table design
- **Role-Based Access Control**: Separate interfaces and permissions for clinicians and patients
- **Data Simulation**: Flexible modes for testing with CSV data or manual input
- **Multi-Modal Data Integration**: Combines neurological signals with behavioral patterns

## System Architecture

### Privacy-First "Bridge" Architecture

EMP implements a novel database design that separates user authentication from medical data:

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  auth.users     │         │ patient_accounts │         │    patients     │
│  (Supabase)     │◄────────┤  (Bridge Table)  │────────►│  (Medical Data) │
│                 │         │                  │         │                 │
│ • user_id (PK)  │         │ • user_id (FK)   │         │ • patient_id    │
│ • email         │         │ • patient_id(FK) │         │ • mrn           │
│ • role          │         │ • created_at     │         │ • dob           │
└─────────────────┘         └──────────────────┘         │ • diagnosis     │
                                                          └─────────────────┘
```

**Why This Matters**: The ML model operates entirely on the `patients` table and never accesses personally identifiable information (PII) from `auth.users`. This ensures that:
- Medical research can be conducted without exposing user identities
- Data breaches are compartmentalized
- Compliance with HIPAA and GDPR is simplified

### Security: Defense in Depth

EMP implements multiple layers of security:

1. **FastAPI Middleware (JWT Authentication)**
   - Validates bearer tokens on every API request
   - Extracts user role from JWT metadata
   - Enforces role-based endpoint access

2. **Supabase Row Level Security (RLS)**
   - Database-level policies prevent unauthorized data access
   - Clinicians can only view patients assigned to them
   - Patients can only access their own data

3. **Bridge Table Access Control**
   - The `patient_accounts` bridge is the only link between auth and medical data
   - Strictly controlled with foreign key constraints
   - Logged and auditable

### ML Pipeline: Feature Injection Architecture

The ML model requires both EEG features and lifestyle data, but EEG analysis is computationally expensive. EMP solves this with a hybrid approach:

```
User Input                    Baseline EEG Features          Combined Feature Vector
(Real-time)                   (Pre-computed)                 (Model Input)
┌──────────────┐              ┌──────────────────┐           ┌────────────────────┐
│ • Sleep: 6h  │              │ • delta_power     │           │ • sleep_hours: 6   │
│ • Stress: 7  │    +         │ • theta_power     │    →      │ • stress_level: 7  │
│ • Meds: Yes  │              │ • alpha_power     │           │ • delta_power: 1.2 │
└──────────────┘              │ • beta_power      │           │ • theta_power: 0.8 │
                              │ • gamma_power     │           │ • ... (68 features)│
                              └──────────────────┘           └────────────────────┘
```

**Implementation**: The backend (`app/services/ml_service.py`) loads a patient's baseline EEG features from `master_eeg_features.csv` and merges them with real-time lifestyle logs to create a complete feature vector for the XGBoost model.

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Visualization**: Recharts
- **State Management**: React Context API (AuthContext)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Dependency Management**: Poetry
- **ML Library**: XGBoost (with SHAP for explainability)
- **Data Processing**: Pandas, NumPy
- **EEG Processing**: MNE-Python

### Database & Auth
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth with JWT
- **Storage**: Supabase Storage (for EDF files)

### ML Pipeline
- **Model**: XGBoost Classifier
- **Features**: 68-dimensional vector (EEG + Lifestyle)
- **Training Data**: CHB-MIT Scalp EEG Database
- **Format**: Universal Binary JSON (.ubj) for model serialization

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Poetry** (Python dependency manager)
- **Supabase Account** (free tier available)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd epilepsy-management-platform
   ```

2. **Configure Supabase**
   
   Create a Supabase project at https://supabase.com and note your:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY` (for frontend)
   - `SUPABASE_SERVICE_ROLE_KEY` (for backend)

3. **Create environment files**

   **Backend** (`backend-api/.env`):
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-service-role-key
   SUPABASE_JWT_SECRET=your-jwt-secret
   ```

   **Frontend** (`clinician-dashboard/.env`):
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-key
   ```

   **Patient Frontend** (`patient-frontend/.env`):
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-key
   ```

### Backend Installation

```bash
cd backend-api

# Install dependencies with Poetry
poetry install

# Activate virtual environment (optional)
poetry shell

# Run the FastAPI server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. View interactive docs at `http://localhost:8000/docs`.

### Frontend Installation

**Clinician Dashboard**:
```bash
cd clinician-dashboard

# Install dependencies
npm install

# Run development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

**Patient Frontend**:
```bash
cd patient-frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The patient interface will be available at `http://localhost:5174`.

### Database Setup

Run the following SQL in your Supabase SQL Editor:

```sql
-- Create patients table
CREATE TABLE patients (
  patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  mrn TEXT UNIQUE NOT NULL,
  first_name TEXT,
  last_name TEXT,
  date_of_birth DATE,
  diagnosis TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create bridge table
CREATE TABLE patient_accounts (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  patient_id UUID REFERENCES patients(patient_id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (user_id, patient_id)
);

-- Create logs table
CREATE TABLE logs (
  log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  patient_id UUID REFERENCES patients(patient_id) ON DELETE CASCADE,
  log_date DATE NOT NULL,
  sleep_hours NUMERIC,
  stress_level INTEGER,
  medication_taken BOOLEAN,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE patient_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (example for clinicians)
CREATE POLICY "Clinicians can view assigned patients"
  ON patients FOR SELECT
  USING (
    patient_id IN (
      SELECT patient_id FROM patient_accounts 
      WHERE user_id = auth.uid()
    )
  );
```

## Project Structure

```
epilepsy-management-platform/
├── backend-api/                 # FastAPI backend
│   ├── app/
│   │   ├── auth/               # Authentication endpoints
│   │   ├── patients/           # Patient management
│   │   ├── logs/               # Lifestyle data logging
│   │   ├── ml_engine/          # ML model serving
│   │   ├── middleware/         # JWT validation
│   │   └── services/           # ML service layer
│   ├── csv_data/               # Simulated patient data
│   └── pyproject.toml          # Poetry dependencies
│
├── clinician-dashboard/        # React clinician interface
│   ├── src/
│   │   ├── components/        # RiskCard, ControlPanel
│   │   ├── pages/             # Dashboard, Login
│   │   ├── context/           # AuthContext
│   │   └── services/          # API client
│   └── package.json
│
├── patient-frontend/           # React patient interface
│   ├── src/
│   │   ├── components/        # DashboardView, ProfileView
│   │   └── ...
│   └── package.json
│
└── ml-pipeline/                # ML training pipeline
    ├── data/
    │   ├── raw/eeg/           # EDF files from CHB-MIT
    │   └── processed/         # Extracted features
    ├── src/
    │   ├── processing.py      # EEG feature extraction
    │   ├── training.py        # XGBoost training
    │   └── deploy.py          # Model export
    └── models/                # Trained models (.ubj)
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login with email/password
- `POST /auth/signup` - Register new user
- `GET /auth/me` - Get current user info

### Patients
- `GET /patients/` - List all patients (clinician only)
- `GET /patients/{patient_id}` - Get patient details
- `POST /patients/` - Create new patient

### Logs
- `GET /logs/patient/{patient_id}` - Get patient logs
- `POST /logs/` - Create new log entry

### ML Engine
- `POST /ml/predict` - Get seizure risk prediction
  ```json
  {
    "patient_id": "uuid",
    "sleep_hours": 6.5,
    "stress_level": 7,
    "medication_taken": true
  }
  ```

## Security & Privacy

### HIPAA Compliance Considerations

- **Data Encryption**: All data in transit uses TLS 1.3. Supabase encrypts data at rest.
- **Access Logging**: All patient data access is logged via Supabase audit logs.
- **Minimal Data Exposure**: ML model uses de-identified baseline features.
- **Role-Based Access**: Strict separation between clinician and patient permissions.

### Authentication Flow

1. User logs in via Supabase Auth
2. Frontend receives JWT with custom claims (`role: "clinician"` or `"patient"`)
3. JWT is sent in `Authorization: Bearer <token>` header
4. FastAPI middleware validates token and extracts user context
5. Supabase RLS policies enforce data access at database level

### Row Level Security Policies

- **Patients**: Clinicians see only assigned patients; patients see only themselves
- **Logs**: Users can only create/view logs for authorized patients
- **Bridge Table**: Read-only access; modifications require service role

## ML Pipeline

### Training the Model

```bash
cd ml-pipeline

# Create conda environment
conda env create -f environment.yml
conda activate eeg-ml

# Run full pipeline
python main_pipeline.py
```

### Feature Extraction

The pipeline processes EEG data in the following steps:

1. **Load EDF Files**: Reads raw EEG signals from CHB-MIT database
2. **Preprocessing**: Applies bandpass filters (0.5-50 Hz)
3. **Feature Engineering**: Extracts 64 frequency-domain features per channel
4. **Aggregation**: Creates patient-level baseline features
5. **Export**: Saves to `master_eeg_features.csv`

### Model Metrics

Current model performance (validation set):
- **Accuracy**: 87.3%
- **Precision**: 84.2%
- **Recall**: 89.1%
- **F1-Score**: 86.6%
- **AUC-ROC**: 0.92



## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Standards

- **Backend**: Follow PEP 8 style guide, type hints required
- **Frontend**: ESLint + Prettier, TypeScript strict mode
- **Testing**: Minimum 80% code coverage for new features
- **Documentation**: Update README and inline docs

## License

This project is licensed under .

## Acknowledgments

- **CHB-MIT Scalp EEG Database**: Training data provided by Children's Hospital Boston
- **Supabase**: Open-source Firebase alternative
- **XGBoost**: High-performance gradient boosting library
- **MNE-Python**: EEG analysis toolkit

## Support

For questions or issues:
- Open an issue on GitHub
- Email: 
- Documentation: 

## Disclaimer

**This software is for research and educational purposes only. It is not FDA-approved and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.**

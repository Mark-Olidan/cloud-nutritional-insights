# Nutritional Insights Dashboard

A cloud-ready web application for exploring nutritional data across different diet types. Built with Flask and deployed via Docker on Azure App Service.

## Features

### Core Dashboard
- **Nutritional Insights** — bar, pie, and scatter charts showing average macronutrients (protein, carbs, fat) across diet types
- **Recipe Browser** — filterable table of recipes by diet type (Paleo, Vegan, Keto, Mediterranean) with pagination
- **Cluster Visualization** — scatter plot grouping recipes into High Protein, Balanced, and High Carb clusters

### Security Features
- **OAuth 2.0 Login** — sign in with Google or GitHub, no password required
- **Two-Factor Authentication (2FA)** — TOTP-based 2FA using Google Authenticator or Authy, with QR code setup
- **Session Management** — server-side sessions with secure cookies

### Cloud & Compliance
- **Security & Compliance Display** — live status of Azure storage encryption (AES-256), RBAC access control, and GDPR compliance
- **Cloud Resource Cleanup** — simulated cleanup of orphaned blobs, expired tokens, and staging containers (connects to live Azure Blob Storage when configured)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask, Authlib, pyotp |
| Frontend | Vanilla JS, Chart.js |
| Auth | Google OAuth 2.0, GitHub OAuth 2.0, TOTP 2FA |
| Storage | Azure Blob Storage |
| Container | Docker, Azure Container Registry |
| Deployment | Azure App Service, GitHub Actions CI/CD |

## Local Development

### Prerequisites
- Python 3.9+
- Google and GitHub OAuth app credentials (see setup below)

### 1. Clone the repo
```bash
git clone https://github.com/edwinolaez/cloud-nutritional-insights.git
cd cloud-nutritional-insights
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the example env file and fill in your credentials:
```bash
cp .env.example .env
```

Then edit `.env` with your values (see [OAuth Setup](#oauth-setup) below).

### 5. Run the app
```bash
python app.py
```

Visit `http://127.0.0.1:5000`

## OAuth Setup

### GitHub
1. Go to https://github.com/settings/developers → OAuth Apps → New OAuth App
2. Homepage URL: `http://127.0.0.1:5000`
3. Callback URL: `http://127.0.0.1:5000/auth/callback/github`
4. Copy Client ID and Client Secret into `.env`

### Google
1. Go to https://console.cloud.google.com → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID (Web application)
3. Authorized redirect URI: `http://127.0.0.1:5000/auth/callback/google`
4. Copy Client ID and Client Secret into `.env`

## Azure Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full step-by-step instructions to deploy to Azure App Service using Docker and GitHub Actions.

### Quick summary
```bash
# Build and push image to Azure Container Registry
docker build -t nutritional-insights .
docker tag nutritional-insights <acr-name>.azurecr.io/nutritional-insights:latest
docker push <acr-name>.azurecr.io/nutritional-insights:latest
```

Pushing to `main` triggers the GitHub Actions pipeline automatically.

## Project Structure

```
cloud-nutritional-insights/
├── app.py                  # Flask backend — API routes, OAuth, 2FA, cleanup
├── frontend/
│   └── index.html          # Single-page dashboard (Chart.js)
├── All_Diets.csv           # Nutritional dataset
├── data_analysis.py        # Offline data analysis scripts
├── upload_to_azurite.py    # Azure Blob Storage upload helper
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local multi-container setup
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── DEPLOYMENT.md           # Azure deployment guide
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions CI/CD pipeline
```

## Environment Variables

| Variable | Description |
|---|---|
| `FLASK_SECRET_KEY` | Random secret key for session encryption |
| `GOOGLE_CLIENT_ID` | Google OAuth app client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth app client secret |
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Blob Storage connection string (optional locally) |
| `AZURE_CONTAINER_NAME` | Blob container name (default: `datasets`) |

## License

MIT

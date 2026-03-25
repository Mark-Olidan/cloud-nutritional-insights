# Azure Deployment Guide — Nutritional Insights Dashboard

## Overview

This guide walks you through deploying the app to Azure App Service using Docker.
Everything below is available on the **Azure Student subscription**.

---

## Step 1 — Install the tools

### Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop/
2. Download for Windows or Mac, run the installer.
3. Open a terminal and verify: `docker --version`

### Azure CLI
1. Go to https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
2. Download and install for your OS.
3. Verify: `az --version`
4. Log in: `az login`   (opens browser, sign in with your student account)

---

## Step 2 — Register OAuth apps (one-time setup)

### Google OAuth
1. Go to https://console.cloud.google.com/
2. Create a new project (e.g. "nutritional-insights")
3. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
4. Application type: Web application
5. Authorized redirect URI: `https://<your-app-name>.azurewebsites.net/auth/callback/google`
6. Copy the **Client ID** and **Client Secret**

### GitHub OAuth
1. Go to https://github.com/settings/developers → OAuth Apps → New OAuth App
2. Homepage URL: `https://<your-app-name>.azurewebsites.net`
3. Authorization callback URL: `https://<your-app-name>.azurewebsites.net/auth/callback/github`
4. Copy the **Client ID** and **Client Secret**

---

## Step 3 — Create Azure resources

Run these commands in your terminal (replace names as needed):

```bash
# Variables — change these
RESOURCE_GROUP="nutritional-rg"
LOCATION="canadacentral"          # close to Calgary; or use "eastus"
ACR_NAME="nutritionalinsightsacr" # must be globally unique, lowercase, no hyphens
APP_NAME="nutritional-insights"   # your App Service name
STORAGE_ACCOUNT="nutritionalstorage"
KEYVAULT_NAME="nutritional-kv"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry (Basic tier — cheapest)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Create Azure Storage Account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2

# Create the blob container
az storage container create \
  --name datasets \
  --account-name $STORAGE_ACCOUNT

# Upload the CSV to blob storage
az storage blob upload \
  --account-name $STORAGE_ACCOUNT \
  --container-name datasets \
  --name All_Diets.csv \
  --file All_Diets.csv

# Get the storage connection string (save this for later)
az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP

# Create Key Vault (optional but recommended for secrets)
az keyvault create \
  --name $KEYVAULT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Create App Service Plan (F1 = free tier)
az appservice plan create \
  --name "${APP_NAME}-plan" \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku F1

# Create the Web App wired to your ACR image
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan "${APP_NAME}-plan" \
  --deployment-container-image-name "${ACR_NAME}.azurecr.io/nutritional-insights:latest"
```

---

## Step 4 — Set environment variables on App Service

```bash
# Get your ACR credentials
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Set all environment variables (replace placeholder values)
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    FLASK_SECRET_KEY="<generate a long random string>" \
    GOOGLE_CLIENT_ID="<your-google-client-id>" \
    GOOGLE_CLIENT_SECRET="<your-google-client-secret>" \
    GITHUB_CLIENT_ID="<your-github-client-id>" \
    GITHUB_CLIENT_SECRET="<your-github-client-secret>" \
    AZURE_STORAGE_CONNECTION_STRING="<connection-string-from-step-3>" \
    AZURE_CONTAINER_NAME="datasets" \
    WEBSITES_PORT="5000"

# Allow App Service to pull from ACR
az webapp config container set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-registry-server-url "https://${ACR_NAME}.azurecr.io" \
  --docker-registry-server-user $ACR_NAME \
  --docker-registry-server-password $ACR_PASSWORD
```

---

## Step 5 — Set up GitHub Actions secrets

In your GitHub repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret name                  | Value                                                   |
|------------------------------|---------------------------------------------------------|
| `ACR_NAME`                   | Your ACR name (e.g. `nutritionalinsightsacr`)           |
| `ACR_USERNAME`               | Same as ACR name                                        |
| `ACR_PASSWORD`               | From: `az acr credential show --name <acr-name>`        |
| `AZURE_WEBAPP_NAME`          | Your App Service name                                   |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Download from Azure Portal → App Service → Overview → Get publish profile |

---

## Step 6 — Deploy

Push to main branch — GitHub Actions will:
1. Build the Docker image
2. Push it to Azure Container Registry
3. Deploy it to App Service automatically

```bash
git add .
git commit -m "Add OAuth, 2FA, security status, and cleanup features"
git push origin main
```

Watch the Actions tab in GitHub for progress.
Your app will be live at: `https://<your-app-name>.azurewebsites.net`

---

## Step 7 — Verify everything works

1. Visit your app URL
2. Click "Continue with Google" or "Continue with GitHub"
3. After OAuth completes, scan the QR code with Google Authenticator or Authy
4. Enter the 6-digit code to complete login
5. Check the Security & Compliance section shows live Azure data
6. Test the Clean Up Resources button

---

## Troubleshooting

**App shows "Application Error"**
```bash
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

**OAuth callback URL mismatch**
Make sure the redirect URI in Google/GitHub exactly matches your App Service URL,
including the `/auth/callback/google` or `/auth/callback/github` path.

**F1 free tier limitation**
The F1 tier has no custom domain SSL. OAuth providers require HTTPS — the
`*.azurewebsites.net` domain comes with a free SSL certificate, so use that URL
(not a custom domain) unless you upgrade to B1.

**2FA "Invalid code" on first setup**
Make sure your phone's clock is synced. TOTP codes are time-based and fail if
the device clock is off by more than 30 seconds.

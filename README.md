# Azure ML CI (GitHub Actions)

This repository includes a GitHub Actions workflow that builds, tests, and submits a training job to Azure ML.

Files added:
- `.github/workflows/azure-ml-ci.yml` — CI workflow that installs deps, runs tests, logs into Azure, and submits the job.
- `.azure/job.yml` — example Azure ML command job that runs `python train.py`.

Project scaffold added:
- `train.py` — example training script (scikit-learn) that saves `outputs/model.joblib`.
- `requirements.txt` — required packages.
- `tests/test_train.py` — basic pytest that validates model artifact creation.
- `.gitignore` — ignores virtualenv, outputs, caches.

Offline / Local setup (GitHub Desktop + run CI locally)

- Install Docker and GitHub Desktop for local git GUI.
- Install `act` to execute GitHub Actions locally (requires Docker):

```powershell
# on Windows (use Windows PowerShell / Git Bash)
choco install act -y   # or follow https://github.com/nektos/act
```

- Run the workflow locally (simulate push to `main`):

```bash
act -j build-and-submit -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
```

Note: `act` runs actions in Docker and cannot perform Azure login using GitHub Secrets the same way GitHub does. For local simulation, you can replace the Azure steps with mocks or run the Azure CLI steps manually after authenticating with `az login`.

Online setup (GitHub Actions -> Azure ML)

1. Create an Azure service principal and grant it rights to the target subscription/resource group:

```bash
az ad sp create-for-rbac --name "github-actions-azureml" --role Contributor --scopes /subscriptions/<SUBSCRIPTION_ID>
```

2. Store the JSON output in the repository secret `AZURE_CREDENTIALS` (Repository Settings → Secrets → Actions). The value should be the full JSON object returned by the command.

3. Ensure your workspace has `train.py` and (optionally) `requirements.txt` in the repo root. The workflow submits `.azure/job.yml` which runs `python train.py`.

4. Push to `main` or open a PR to trigger the workflow.

Notes and next steps
- Update the `Run tests` step to call your real test runner (e.g., `pytest`).
- Customize `.azure/job.yml` with compute, environment, and inputs/outputs for your pipeline.
- If you want the workflow to run a test-only path (no Azure submission) on forks, add conditional checks.

If you want, I can:
- create a minimal `requirements.txt` and example `train.py`,
- run a local test using `act` (if you have Docker), or
- update the workflow to use specific Azure ML workspace names and compute targets.

Local (no Docker) — run the steps manually

If you prefer not to use Docker or `act`, you can run the CI steps directly on your machine. This requires Python and the Azure CLI (no Docker needed):

```powershell
# 1) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install dependencies (if any)
python -m pip install --upgrade pip
if (Test-Path requirements.txt) { pip install -r requirements.txt }

# 3) Run tests (replace with your test command)
if (Get-Command pytest -ErrorAction SilentlyContinue) { pytest -q } else { Write-Host "No tests configured" }

# 4) Install Azure CLI (if not installed) — download MSI from https://learn.microsoft.com/azure/azure-cli/install-azure-cli-windows
# or use your package manager. Then login interactively:
az login

# 5) Add Azure ML CLI extension
az extension add -n ml

# 6) Submit the job to Azure ML (provide workspace and resource group)
az ml job create -f .azure/job.yml -w <YOUR_WORKSPACE> -g <YOUR_RESOURCE_GROUP>
```
Local quick start

1) Create a venv and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Run training locally:

```powershell
python train.py
```

3) Run tests:

```powershell
pytest -q
```

Notes:
- The `az ml job create` command submits the job to your Azure ML workspace. Replace `<YOUR_WORKSPACE>` and `<YOUR_RESOURCE_GROUP>` with your values.
- If you need non-interactive authentication, create a service principal and authenticate with `az login --service-principal -u <appId> -p <password> --tenant <tenant>`.
- Running locally this way executes the same Python steps as the CI workflow but performs Azure submission from your machine instead of from GitHub Actions.

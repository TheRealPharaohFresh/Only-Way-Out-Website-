# Only Way Out LLC

Static artist and company website with a Flask API and Firebase services.

## Project layout

- `frontend/` — Static HTML, CSS, browser JavaScript, and Firebase configuration.
- `frontend/functions/` — Firebase Cloud Functions.
- `backend/` — Flask download and YouTube API.
- `.github/workflows/workflow.yml` — CI checks and deployment workflow.

The static frontend has no compile/build step. Netlify hosts the frontend separately through its existing Git integration; the GitHub Actions workflow tests the repository, deploys Firebase services and the Render backend, waits for the Render deployment to become live, and smoke-tests the API.

## Local checks

Run backend tests from the repository root:

```sh
python -m pip install -r backend/requirements.txt pytest
SECRET_TOKEN=local-test-secret python -m pytest backend/test_app.py
```

Run Firebase Functions lint:

```sh
cd frontend/functions
npm ci
npm run lint
```

The workflow runs those checks for pull requests and pushes to `main`. A successful test job is required before deployment. Deployment runs only on `main` pushes or a manual workflow dispatch against `main`; pull requests never deploy.

## GitHub Actions deployment configuration

Configure these GitHub Actions secrets:

| Secret | Used for |
| --- | --- |
| `FIREBASE_TOKEN` | Deploying Firebase Functions and Firestore rules |
| `RENDER_API_KEY` | Triggering a Render deployment |
| `RENDER_SERVICE_ID` | Selecting the Render service |

The Render service must separately have `SECRET_TOKEN`, `ALLOWED_ORIGINS`, and (if view counts are enabled) `YOUTUBE_API_KEY` configured in its environment. The frontend is deployed separately through the Netlify integration.

## Dependency audit follow-up

The current Firebase Functions production dependency audit has no critical advisories, but still reports 2 high and 7 moderate vulnerabilities. The remaining high findings require a major `firebase-admin` upgrade to version 14, which is outside the compatible lockfile refresh and needs a coordinated Firebase Functions SDK/configuration migration before it can be safely deployed.

## YouTube view counts

The YouTube endpoint returns a hidden-count response below 100 views. The TrapHouse page displays the count only when it is at least 100:

```text
GET /api/youtube/youtube_views?track=keep-it-100
GET /api/youtube/youtube_views?track=for-me
```

## PayPal checkout status

The TrapHouse page currently posts PayPal Standard checkout forms for $1.99 per track. It fetches a short-lived download URL from the API and places that URL in PayPal's `return` field.

**This is not payment verification.** The download URL endpoint is currently public, so a client can request a valid download URL without completing a PayPal payment. Do not rely on this flow to restrict paid downloads until the backend verifies a PayPal order or verified IPN/webhook before issuing a download grant.

For a safe end-to-end test, configure PayPal Sandbox merchant and buyer accounts, use the Sandbox checkout endpoint and merchant account, complete a test payment, and confirm the transaction is `Completed` in the merchant Sandbox activity. Then verify the return/download and compare the downloaded audio with the intended track. Also test a cancelled/failed payment and confirm no download grant is issued. The current integration does not yet meet that last payment-gating requirement.

## Final app check

The local release check covers the backend test suite, Firebase Functions lint, the eight primary frontend pages, local media and internal links, form validation, and the TrapHouse carousel controls. It deliberately does not submit a live PayPal transaction or create real Firebase accounts.

In the pre-release live-site check, the Netlify pages and media returned HTTP 200, but `/site.css` returned 404. The deployed Render service also returned 404 for the new signed-download URL endpoint, and its YouTube view-count endpoint returned HTTP 502. These observations indicate the live services had not yet picked up all current source changes; recheck them after the deployment workflow finishes. The workflow now verifies that Render serves the download URL endpoint and the resulting audio file after deployment.

PayPal payment completion, Firebase account creation, and download authorization after a completed payment still require configured Sandbox/production credentials and payment verification. The current public download-URL endpoint is not proof of payment and must not be treated as a secure paid-download gate.

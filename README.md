# 🔥 Only Way Out LLC — Full Stack Web Platform

**Author**: Donald Clemons  
**Website**: [onlywayout.netlify.app](https://onlywayout.netlify.app)  
**Render Backend**: [Download API](https://only-way-out-website-1.onrender.com)

---

## 🎯 Overview

This is the full-stack application for **Only Way Out LLC**, a multimedia brand merging music, film, and culture through tech.

The stack includes:
- A secure Flask-based backend API for music downloads
- A Netlify-hosted static frontend for streaming and shopping
- Firebase backend automation for user onboarding
- Continuous deployment via GitHub Actions

---

## ⚙️ Technology Stack

| Tech                  | Role                                          | Usage % |
|-----------------------|-----------------------------------------------|---------|
| HTML5 + Bootstrap 5   | Static frontend (pages, carousel, layout)     | 55%     |
| Python (Flask)        | Secure file download backend                  | 15%     |
| JavaScript (Node.js)  | Firebase Functions (welcome emails)           | 20%     |
| CSS                   | Custom styling for TrapHouse and other pages  | 5%      |
| GitHub Actions        | CI/CD automation                              | 5%      |

---

## 🔐 Flask Secure Download API

**API Base URL**: `https://only-way-out-website-1.onrender.com`

### Available Endpoints:

| Endpoint                          | Method | Description                            |
|-----------------------------------|--------|----------------------------------------|
| `/`                               | GET    | Welcome route                          |
| `/download/<track>?token=XYZ123` | GET    | Secure file download with token check  |

**Environment Variable Required**:
- `SECRET_TOKEN`: Used to validate download requests.

**Example track mapping**:
```python
track_map = {
  "keep-it-100": "PharaohFresh-Keep it 100 Ft Atl Jacob.mp3",
  "for-me": "PharaohFresh-For Me.mp3"
}

🧠 Firebase Welcome Email Automation
How It Works:
New user signs up via MembershipRegistration.html.

Firebase Auth creates account and stores data in Firestore.

Firebase Function (via functions/index.js) is triggered:

Sends a branded welcome email using Mailjet API.

Email includes next steps and company branding.

💻 Static Frontend (Netlify)
Live Frontend: https://onlywayout.netlify.app

Pages:
Albums.html — Music projects

Videos.html — Video content

MembershipRegistration.html — User sign-up

TheTrap.html — Music purchase & playback

Information.html — Brand details

TrapHouse Shop Feature:
Audio preview via <audio> tag

PayPal integration for purchase

Auto-redirect to backend API with download token after payment

html
Copy
Edit
<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
  <input type="hidden" name="return" value="https://only-way-out-website-1.onrender.com/download/keep-it-100?token=keepitreal123">
</form>
🚀 Deployment (GitHub Actions + Render + Firebase)
CI/CD triggers on pushes to main:

Backend Deployment to Render:
yaml
Copy
Edit
- name: Deploy Flask backend to Render
  env:
    RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
  run: |
    curl -X POST \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      https://api.render.com/deploy/srv-xxxxxxxxxxxxxxxxxxxx
Firebase Deployment:
yaml
Copy
Edit
- name: Deploy Firebase Functions
  run: firebase deploy --only functions --token ${{ secrets.FIREBASE_TOKEN }}
📁 Project Structure
pgsql
Copy
Edit
only-way-out/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Music/
│       ├── PharaohFresh-Keep it 100 Ft Atl Jacob.mp3
│       └── PharaohFresh-For Me.mp3
├── functions/
│   ├── index.js
│   ├── package.json
│   └── .env
├── public/
│   ├── index.html
│   ├── Albums.html
│   ├── TheTrap.html
│   ├── MembershipRegistration.html
│   └── images/
├── styles/
│   ├── styles4.css
│   └── styles5.css
└── .github/workflows/
    └── deploy.yml
🔒 Secrets Required
Secret Name	Purpose
SECRET_TOKEN	Secures Flask download route
RENDER_API_KEY	Auth for Render deploys
FIREBASE_TOKEN	Deploy Firebase functions
MAILJET_API_KEY	Mailjet integration in Firebase func
MAILJET_SECRET	Mailjet secret key

🧪 Testing
Test Download Link:
bash
Copy
Edit
https://only-way-out-website-1.onrender.com/download/keep-it-100?token=keepitreal123
If successful:

File downloads immediately

Flask logs show token check passed

If invalid:

Returns 403 Unauthorized

🙌 Credits
Built with passion by Donald Clemons.
Powered by technology, hustle, and creative fire.
This ain’t just a website — it’s a movement.

🎵 Only Way Out LLC — Welcome Email Automation & Static Website
A full-stack application for Only Way Out LLC, a multimedia entertainment brand combining creative storytelling and technology. The project integrates a modern static frontend with Firebase-powered backend automation for user registration and welcome emails.

🚀 Features
🔥 Firebase Firestore: Tracks new member registrations in real-time.

✉️ Mailjet Integration: Sends automatic branded welcome emails via Firebase Functions.

🖼️ Responsive Static Website: HTML5 + Bootstrap 5 for a clean, mobile-friendly layout.

📢 Branded Content: Highlights services including Music Publishing, Film, and Record Label ventures.

🌐 SEO-Ready: Semantic HTML for improved search visibility.


| Technology           | Role                            | Usage % (approx.) |
| -------------------- | ------------------------------- | ----------------- |
| HTML5                | Structure and Content           | 55%               |
| JavaScript (Node.js) | Firebase Functions & Auth Logic | 25%               |
| CSS / Bootstrap      | Styling and Layout              | 20%               |


only-way-out/
│
├── public/
│   ├── index.html
│   ├── Albums.html
│   ├── Videos.html
│   ├── MembershipRegistration.html
│   ├── Information.html
│   ├── Login.html
│   └── /images
│
├── functions/
│   ├── index.js        # Firebase Function sending welcome emails
│   ├── package.json    # Dependencies (Mailjet, Firebase Admin, etc.)
│
├── styles/
│   ├── styles4.css
│   ├── styles5.css
│   ├── styles7.css
│
└── README.md

🧠 How It Works
User Registration via the Membership page:

Firebase Auth creates a new user.

Firestore stores basic member info.

Firebase Function triggers on document creation:

Sends a welcome email using Mailjet API.

Email includes brand messaging and next steps.

Link: https://onlywayout.netlify.app/

Author:Donald Clemons


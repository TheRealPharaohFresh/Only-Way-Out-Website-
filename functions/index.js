const {onDocumentCreated} = require("firebase-functions/v2/firestore");
const logger = require("firebase-functions/logger");
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const mailjet = require("node-mailjet");
require("dotenv").config();

admin.initializeApp();

const mj = mailjet.apiConnect(
    process.env.MAILJET_API_KEY || functions.config().mailjet.apikey,
    process.env.MAILJET_SECRET_KEY || functions.config().mailjet.secretkey,
);

exports.sendWelcomeEmail = onDocumentCreated("members/{memberId}", (event) => {
  const member = event.data.data();
  const email = member.email;
  const name = member.name;

  const request = mj.post("send", {version: "v3.1"}).request({
    Messages: [
      {
        From: {
          Email: "onlywayoutllc@gmail.com",
          Name: "Only Way Out LLC",
        },
        To: [
          {
            Email: email,
            Name: name,
          },
        ],
        Subject: "Welcome to Only Way Out!",
        TextPart: `Hi ${name}, welcome to our website!`,
        HTMLPart: `
          <h3>Hi ${name},</h3>
          <p>Welcome to our community! We're thrilled to have you on board.</p>
          <p>As a special thank you for being one of our first members, we're gifting you an exclusive promo code:</p>
          <h2 style="color:#4CAF50;">Promo Code: <strong>only1world</strong></h2>
          <p>Use this code to unlock 25–50% off unreleased music, exclusive merchandise, and even show tickets!</p>
          <p>Make sure to keep this code safe — it's your VIP pass to everything we've got coming your way.</p>
          <p>Stay tuned for more amazing surprises!</p>
        `,
      },
    ],
  });

  return request
      .then((result) => {
        logger.info("Email sent successfully:", result.body);
      })
      .catch((err) => {
        logger.error("Error sending email:", err);
      });
});


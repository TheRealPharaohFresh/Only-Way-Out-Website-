const functions = require("firebase-functions"); // ✅ config() is here
const {onDocumentCreated} = require("firebase-functions/v2/firestore");
const admin = require("firebase-admin");
const mailjet = require("node-mailjet");

admin.initializeApp();

const MJ_API_KEY =
  process.env.MAILJET_API_KEY ||
  (functions.config().mailjet && functions.config().mailjet.apikey);
const MJ_SECRET_KEY =
  process.env.MAILJET_SECRET_KEY ||
  (functions.config().mailjet && functions.config().mailjet.secretkey);

const mj = mailjet.apiConnect(MJ_API_KEY, MJ_SECRET_KEY);

exports.sendWelcomeEmail = onDocumentCreated("members/{memberId}", async (event) => {
  try {
    const member = event.data.data();
    const email = member.email;
    const name = member.name;

    const result = await mj.post("send", {version: "v3.1"}).request({
      Messages: [
        {
          From: {
            Email: "onlywayoutllc@gmail.com",
            Name: "Only Way Out LLC",
          },
          To: [{Email: email, Name: name}],
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

    console.log("Email sent successfully:", result.body);
    return {success: true};
  } catch (err) {
    console.error("Error sending email:", err);
    throw new Error("Email failed to send.");
  }
});

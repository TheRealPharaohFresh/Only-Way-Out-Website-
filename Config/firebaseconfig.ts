// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDg8lFOtXR7Qj5ERIsSHBhQtX5a9sb-06Q",
  authDomain: "only-way-out-website.firebaseapp.com",
  projectId: "only-way-out-website",
  storageBucket: "only-way-out-website.firebasestorage.app",
  messagingSenderId: "1084316758513",
  appId: "1:1084316758513:web:4727cecd5f01c9f2d65450",
  measurementId: "G-7VG8B8366R"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
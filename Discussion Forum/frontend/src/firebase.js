import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// const firebaseConfig = {
//   apiKey: "AIzaSyAm2j5QCRCCJlRX0r1qBG_be1bXdXSRdyY",
//   authDomain: "stackoverflow-3f0d8.firebaseapp.com",
//   projectId: "stackoverflow-3f0d8",
//   storageBucket: "stackoverflow-3f0d8.appspot.com",
//   messagingSenderId: "76298589116",
//   appId: "1:76298589116:web:26ce6feaf0025dbdd511b9",
//   measurementId: "G-LDJE2JW8YE",
// };
// const firebaseConfig = {
//     apiKey: "AIzaSyA3Bx63Sm2-VT1SpEq5GxgyUt87TwYQ7x8",
//     authDomain: "stack-clone-6c586.firebaseapp.com",
//     projectId: "stack-clone-6c586",
//     storageBucket: "stack-clone-6c586.appspot.com",
//     messagingSenderId: "943432979484",
//     appId: "1:943432979484:web:a386fc28de9e69b03bfbd9",
//     measurementId: "G-ZKPKEG4Y89",
// };
const firebaseConfig = {
    apiKey: "AIzaSyAYSGgcxg3FIDg5fWPXX0RpL3gaGWzeyZY",
    authDomain: "stack-over-cl.firebaseapp.com",
    projectId: "stack-over-cl",
    storageBucket: "stack-over-cl.appspot.com",
    messagingSenderId: "133836027044",
    appId: "1:133836027044:web:9403dc333353854b226231",
    measurementId: "G-LPPCMZC21J"
  };

const firebaseApp = initializeApp(firebaseConfig);
// const db = firebaseApp.firestore();
const auth = getAuth();
const provider = new GoogleAuthProvider();

export { auth, provider };
// export default db;

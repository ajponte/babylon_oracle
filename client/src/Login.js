
import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";

const Login = ({ setCredential }) => {
  return (
    <GoogleLogin
      onSuccess={credentialResponse => {
        const credentialResponseDecoded = jwtDecode(credentialResponse.credential);
        console.log(credentialResponseDecoded);
        setCredential(credentialResponse.credential);
      }}
      onError={() => {
        console.log('Login Failed');
      }}
    />
  );
};

export default Login;

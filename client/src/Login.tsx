import React from 'react';
import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";

interface LoginProps {
  setCredential: (credential: string) => void;
}

const Login: React.FC<LoginProps> = ({ setCredential }) => {
  return (
    <GoogleLogin
      onSuccess={(credentialResponse: CredentialResponse) => {
        const credentialResponseDecoded = jwtDecode<{ name: string, email: string }>(credentialResponse.credential!);
        console.log(credentialResponseDecoded);
        setCredential(credentialResponse.credential!);
      }}
      onError={() => {
        console.log('Login Failed');
      }}
    />
  );
};

export default Login;

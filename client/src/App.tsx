import React from 'react';
import Chatbot from './Chatbot';
import { CssBaseline, Container, Typography } from '@mui/material';

const App = () => {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="sm">
        <Typography variant="h4" component="h1" align="center" gutterBottom>
          Babylon
        </Typography>
        <Chatbot />
      </Container>
    </>
  );
};

export default App;

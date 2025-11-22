
import React, { useState } from 'react';
import axios from 'axios';
import { Paper, TextField, Button, List, ListItem, ListItemText, Avatar, Grid, CircularProgress } from '@mui/material';
import { deepOrange, deepPurple } from '@mui/material/colors';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5003/api/message', { user_input: input });
      setMessages(prevMessages => [...prevMessages, { text: response.data.text, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      } else if (error.request) {
        console.error('Request:', error.request);
      } else {
        console.error('Error message:', error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <List sx={{ flexGrow: 1, overflowY: 'auto', p: 2 }}>
        {messages.map((msg, index) => (
          <ListItem key={index} sx={{ justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start' }}>
            <Grid container direction={msg.sender === 'user' ? 'row-reverse' : 'row'} alignItems="center" spacing={1}>
              <Grid item>
                <Avatar sx={{ bgcolor: msg.sender === 'user' ? deepOrange[500] : deepPurple[500] }}>
                  {msg.sender === 'user' ? 'U' : 'B'}
                </Avatar>
              </Grid>
              <Grid item>
                <ListItemText
                  primary={msg.text}
                  sx={{
                    bgcolor: msg.sender === 'user' ? 'primary.light' : 'secondary.light',
                    p: 1,
                    borderRadius: 2,
                  }}
                />
              </Grid>
            </Grid>
          </ListItem>
        ))}
        {loading && (
          <ListItem sx={{ justifyContent: 'flex-start' }}>
            <Grid container direction="row" alignItems="center" spacing={1}>
              <Grid item>
                <Avatar sx={{ bgcolor: deepPurple[500] }}>
                  {'B'}
                </Avatar>
              </Grid>
              <Grid item>
                <CircularProgress size={20} />
              </Grid>
            </Grid>
          </ListItem>
        )}
      </List>
      <Grid container spacing={1} sx={{ p: 2 }}>
        <Grid item xs>
          <TextField
            fullWidth
            label="Type a message"
            variant="outlined"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={sendMessage} sx={{ height: '100%' }}>
            Send
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default Chatbot;

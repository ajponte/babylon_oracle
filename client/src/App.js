import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post('http://localhost:5001/chat', { user_input: input });
      setMessages([...newMessages, { text: response.data.response, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.error('Request:', error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', error.message);
      }
    }
  };

  return (
    <div>
      <div style={{ height: '400px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <p style={{ display: 'inline-block', padding: '5px 10px', borderRadius: '10px', backgroundColor: msg.sender === 'user' ? '#dcf8c6' : '#f1f0f0' }}>
              {msg.text}
            </p>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', marginTop: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          style={{ flex: 1, padding: '5px' }}
        />
        <button onClick={sendMessage} style={{ padding: '5px 10px' }}>Send</button>
      </div>
    </div>
  );
};

export default App;

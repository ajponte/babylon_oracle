/**
 * Express server.
 */
const express = require('express');
const axios = require('axios');
const path = require('path');
const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');
const webpackConfig = require('./webpack.config.js');

const app = express();
const compiler = webpack(webpackConfig);

// todo: move to config
const MCP_SERVER_HOST = "localhost"
const MCP_SERVER_PORT = 5003
const MCP_CHAT_URI = '/api/message'


const DEFAULT_MCP_HOST = "localhost"
const port = 3000;

app.use(express.json());

app.use(
  webpackDevMiddleware(compiler, {
    publicPath: webpackConfig.output.publicPath,
  })
);

app.use(webpackHotMiddleware(compiler));

app.post('/chat', async (req, res) => {
  var uri = `http://${DEFAULT_MCP_HOST}:${MCP_SERVER_PORT}${MCP_CHAT_URI}`
  try {
    const response = await axios.post(
      uri,
      req.body
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Error communicating with the oracle server' });
  }
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
  console.log(`Client server listening at http://localhost:${port}`);
});

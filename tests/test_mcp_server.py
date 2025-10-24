"""Test MCP Server"""

import unittest
import json
from oracle_server.app import app

class TestMcpServer(unittest.TestCase):
    """TestMcpServer"""

    def setUp(self):
        """setUp"""
        self.app = app.test_client()

    def test_health(self):
        """test_health"""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_chat_no_tool(self):
        """test_chat_no_tool"""
        response = self.app.post("/chat",
                                 data=json.dumps({"user_input": "Hello"}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": "I can help with that."})

    def test_chat_weather_tool(self):
        """test_chat_weather_tool"""
        response = self.app.post("/chat",
                                 data=json.dumps({"user_input": "[get_weather(location=London)]"}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": "The weather in London is sunny."})

    def test_chat_calculator_tool(self):
        """test_chat_calculator_tool"""
        response = self.app.post("/chat",
                                 data=json.dumps({"user_input": "[calculate(expression=2+2)]"}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": "The result of 2+2 is 4."})

if __name__ == "__main__":
    unittest.main()
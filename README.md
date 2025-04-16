# Voicebot-MCP-Server

This is a MCP Server which provides capabilities to send and receive voice messages and interact with AI client **Claude Desktop** via messaging app **WhatsApp**.

## Required Libraries:
The different libraries and dependencies required for the project are as given below:

1. MCP SDK
2. dotenv (for storing .env files)
3. requests
4. json
5. uv (for testing with MCP Inspector)
6. Flask
7. Twilio

## Steps to run:

1. Install required libraries
```
   pip install flask twilio uv dotenv
```
2. Install the MCP SDK.
```
   pip install "mcp[cli]"
```
3. Integrate the server with Claude Desktop
```
   mcp install server.py --name "VoiceBot MCP Server"
```
4. Test the server using MCP Inspector
```
   mcp dev server.py
```
5. Run the Webhook using ngrok
```
   ngrok http 5003
```

**Note: In ```whatsapp_webhook.py```, personal whatsapp numbers can be provided in ```"WHATSAPP_VERIFY_NUMBER"``` for interacting with the Claude-based MCP Server.**

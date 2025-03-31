# Messenger Chat Application

## Overview
This project is a simple chat application that utilizes WebSocket for real-time messaging. Users can log in and participate in a chat room where they can send and receive messages.

## Project Structure
```
Messenger
├── index.html        # Main chat interface with WebSocket functionality
├── login.html        # Login page for user authentication
├── css
│   └── styles.css    # Styles for the application
├── js
│   └── main.js       # JavaScript code for WebSocket connection and message handling
└── README.md         # Documentation for the project
```

## Files Description
- **index.html**: Contains the main chat interface. Displays the user's ID, a message input form, and a list of messages received via WebSocket.
- **login.html**: Provides a form for users to enter their credentials (username and password) and a button to submit the form.
- **css/styles.css**: Contains styles for both the chat interface and the login page.
- **js/main.js**: Handles the WebSocket connection and message sending for the chat interface. This file may need updates to manage user sessions after login.

## Setup Instructions
1. Clone the repository to your local machine.
2. Open the `index.html` or `login.html` file in a web browser to access the chat application.
3. Ensure that a WebSocket server is running on `ws://localhost:8000` to handle the WebSocket connections.

## Usage Guidelines
- Navigate to the `login.html` page to log in with your credentials.
- After logging in, you will be redirected to the chat interface in `index.html`.
- Use the input field to send messages, which will be displayed in real-time in the message list.

## Future Improvements
- Implement user authentication and session management.
- Enhance the user interface with better styling and responsiveness.
- Add features such as private messaging and user presence indicators.
# This is a template for a Telegram bot that replies "hi" when /p is sent
# This code does NOT run until you add token and Telegram API connection logic

def on_command_p():
    # Simulate a reply to /p command
    print("hi")

# Simulated incoming command (for demo/testing)
incoming_message = "/p"

# Check command and respond
if incoming_message == "/p":
    on_command_p()

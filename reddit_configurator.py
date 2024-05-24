import os

# Function to securely get sensitive information from user
def get_sensitive_info(prompt):
    while True:
        value = input(prompt)
        if value.strip():  # Check if input is not empty
            return value

# Your client ID
client_id = get_sensitive_info("Enter your client ID: ")

# Your client secret
client_secret = get_sensitive_info("Enter your client secret: ")

# Your user agent
user_agent = get_sensitive_info("Enter your user agent: ")

# Your Reddit username
username = get_sensitive_info("Enter your Reddit username: ")

# Your Reddit password
password = get_sensitive_info("Enter your Reddit password: ")

# Write the sensitive information to a .env file
with open(".env", "w") as f:
    f.write(f"CLIENT_ID={client_id}\n")
    f.write(f"CLIENT_SECRET={client_secret}\n")
    f.write(f"USER_AGENT={user_agent}\n")
    f.write(f"USERNAME={username}\n")
    f.write(f"PASSWORD={password}\n")
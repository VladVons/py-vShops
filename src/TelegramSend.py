import asyncio
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError, ContactAddForbiddenError

async def add_and_send(phone_number, message):
    # Set up the Telegram API client
    api_id = YOUR_API_ID
    api_hash = 'YOUR_API_HASH'
    client = TelegramClient('session_name', api_id, api_hash)

    try:
        # Connect to the Telegram API
        await client.connect()

        # Check if the phone number is registered with Telegram
        await client.send_code_request(phone_number)

        # Add the phone number to your Telegram contacts
        await client.add_contact(phone_number)

        # Send the message to the user
        await client.send_message(phone_number, message)

        # Disconnect from the Telegram API
        await client.disconnect()

        # Return a success message
        return f'Message sent to {phone_number}'

    except PhoneNumberInvalidError:
        # If the phone number is not registered, return an error message
        return f'{phone_number} is not registered with Telegram'

    except ContactAddForbiddenError:
        # If adding the contact is forbidden, return an error message
        return f'Unable to add {phone_number} to your Telegram contacts'

# Example usage
asyncio.run(add_and_send('+1234567890', 'Hello, world!'))

class TelegramIntakeAgent:
    """
    Role: First line of defense for incoming Telegram updates.
    Logic: Deterministic, rule-based check for valid text messages.
    """
    def __init__(self):
        # No initial setup or mock data loading required for this specific agent logic,
        # unlike the source example which loads accounts.json[cite: 729].
        pass

    def validate(self, raw_update: dict):
        """
        Validates a raw Telegram update dictionary.
        Returns a (Boolean success flag, message string) tuple, matching the source pattern[cite: 742].
        """
        # Check 1: Ensure the update contains a 'message' object.
        # This is a deterministic check similar to validating input existence[cite: 611, 734].
        if not raw_update or "message" not in raw_update:
             return False, "Invalid update format: Missing 'message' key."

        message = raw_update["message"]

        # Check 2: Ensure the message contains critical chat information (ID).
        # Similar to checking if a sender/receiver account exists in the source[cite: 612, 736].
        if "chat" not in message or "id" not in message["chat"]:
            return False, "Invalid message data: Missing chat ID."

        # Check 3: Ensure the message contains actual text content.
        # We reject non-text updates (like stickers or photos) at this stage.
        # This is a rule-based rejection if invalid[cite: 613].
        if "text" not in message or not message["text"].strip():
            return False, "Ignored update type: Not a valid text message."

        # If all rule-based checks pass.
        # Returns the success pattern defined in the source[cite: 742].
        return True, "Valid Telegram text message."

import pyautogui
import time
import csv
import os
import pyperclip

# --- CONFIGURATION ---
# 1. Set this to "finder" to find mouse coordinates.
# 2. Set this to "sender" to send the emails.
MODE = "sender" # "finder" or "sender"

# After running in "finder" mode, fill in the coordinates you found here.
# Make sure your Gmail window is not moved between finding coordinates and sending.
COMPOSE_BUTTON = (141, 254)
ATTACH_BUTTON = (616, 1048)
SEND_BUTTON = (483, 1048)

# --- SCRIPT ---

def get_coordinates():
    """Prints the current mouse coordinates until you stop it (Ctrl-C)."""
    print("--- Coordinate Finder Mode ---")
    print("Move your mouse to the desired location and note the X, Y coordinates.")
    print("Press Ctrl-C in your terminal to stop.")
    try:
        while True:
            x, y = pyautogui.position()
            position_str = f"X: {str(x).rjust(4)} Y: {str(y).rjust(4)}"
            print(position_str, end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCoordinates finder stopped.")

def send_emails_automated():
    """Automates sending emails with attachments using mouse clicks."""
    print("--- Email Sender Mode ---")
    print("IMPORTANT: Do not move the mouse after the script starts.")
    print("To stop the script in an emergency, move the mouse to any corner of the screen.")
    pyautogui.FAILSAFE = True

    # Give yourself a few seconds to switch to your browser window
    print("You have 3 seconds to open and focus the browser window with Gmail...")
    time.sleep(3)

    csv_file = "lista.csv"
    certificates_dir = "certificates"
    
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            name = row["NOME"]
            email = row["EMAIL"]
            certificate_file = os.path.abspath(os.path.join(certificates_dir, f"certificate_{name}.pdf"))

            if not email or not os.path.exists(certificate_file):
                print(f"Skipping {name} - Email or certificate missing.")
                continue

            print(f"Processing email for {name}...")

            # 1. Click Compose
            pyautogui.click(COMPOSE_BUTTON)
            time.sleep(2)

            # 2. Type recipient, subject, and body
            pyautogui.write(email)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('tab')
            subject = f"""Certificado de Participação - I Workshop GenTB-PróCura"""
            pyperclip.copy(subject)
            pyautogui.hotkey('ctrl', 'v') # Subject
            pyautogui.press('tab')
            body = f"""Prezado(a) {name},\n\nEm nome do Comitê de Organização, agradecemos imensamente sua presença e contribuição para o sucesso do I Workshop GenTB-PróCura!\n\nO seu Certificado de Participação está anexado a este e-mail.\n\nEsperamos contar com sua participação em futuros eventos!\n\nAtenciosamente,\n\nComitê de Organização I Workshop GenTB-PróCura"""
            pyperclip.copy(body)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)

            # 3. Click Attach and type file path
            pyautogui.click(ATTACH_BUTTON)
            time.sleep(2) # Wait for file dialog to open
            pyautogui.write(certificate_file)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5) # Wait for file to upload

            # 4. Click Send
            pyautogui.click(SEND_BUTTON)
            time.sleep(5) # Wait for email to send and window to close

            print(f"Email for {name} should be sent.")

    print("All emails processed.")


if __name__ == "__main__":
    if MODE == "finder":
        get_coordinates()
    elif MODE == "sender":
        if COMPOSE_BUTTON == (0, 0) or ATTACH_BUTTON == (0, 0) or SEND_BUTTON == (0, 0):
            print("ERROR: Please run in 'finder' mode first and update the coordinates in the script.")
        else:
            send_emails_automated()
    else:
        print("Invalid mode selected. Please set MODE to 'finder' or 'sender'.")

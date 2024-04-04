import requests

from octo_api_test import OCTOPRINT_URL, headers


def send_gcode_commands(command):
    data = {"commands": [command]}
    response = requests.post(f"{OCTOPRINT_URL}/api/printer/command", json=data, headers=headers)
    if response.status_code == 204:
        print(f"Command '{command}' sent successfully")
    else:
        print(f"Failed to send command '{command}', status code: {response.status_code}")


if __name__ == '__main__':
    # Cool down the hotend and bed
    send_gcode_commands("M104 S0") # Set hotend temperature to 0
    send_gcode_commands("M140 S0") # Set bed temperature to 0

    # Home the axes
    send_gcode_commands("G28") # Home all axes
    # Move to upper left rear corner. Adjust X, Y, and Z values according to your printer's dimensions.
    # Example for a printer with a 200x200x200mm build volume:
    # X=0 (assuming it homes to X=0), Y=200 (max Y), Z=200 (max Z). Adjust these values for your printer.
    send_gcode_commands(["G0 X0 Y200 Z200"])
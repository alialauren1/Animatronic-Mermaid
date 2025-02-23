# Animatronic-Mermaid

3 DOF Robot, using servos


## Practicing with cheaper/simpler servos: Tower Pro Micro Servo 9g SG90

The Signal Pin on Servo is connected to Pin PB_10 on Board. The Power is connected to the 5 V pin on Board. The GND is connected to a GND pin on Board

<img width="350" alt="Screenshot 2025-02-22 at 10 24 12 PM" src="https://github.com/user-attachments/assets/bd650ebe-126e-4429-be75-978fe0d2ebff" />
<img width="350" alt="Screenshot 2025-02-22 at 10 24 47 PM" src="https://github.com/user-attachments/assets/9757dcaf-6b78-4c58-b9d6-65fc7955e032" />

## STM32 Nucleo 

### Some Pins on the nucelo:

<img width="600" alt="Screenshot 2025-02-22 at 10 26 57 PM" src="https://github.com/user-attachments/assets/e5246148-01ca-4951-902b-e763e58fa461" />

### Pin Legend

<img width="300" alt="Screenshot 2025-02-22 at 10 27 13 PM" src="https://github.com/user-attachments/assets/161ca3a7-b200-474e-be77-9ff7458edc8d" />

More info: https://os.mbed.com/platforms/ST-Nucleo-L476RG/#getting-started

### To flash firmware/reset the nucleo:
1. Download the firmware.bin file from github. or use this link:
[https://micropython.org/download/?mcu=stm32l4](https://micropython.org/download/)
for our board it leads us to this:
https://micropython.org/download/NUCLEO_L476RG/ Download newest hex file and use STMCUBE programmer with rules below. 

3. Install the STM Cube Programmer
4. Unplug the Nucleo from all power sources.
5. Remove the motor driver from the top of the Nucleo. Make sure not to bend any of the pins; that is, keep the boards close to parallel as they're separated.
6. Move the jumper named JP5 from the "E5V" to the "U5V" position. That is, remove the small black rectangular shorting block and move it over one pin and reinsert it to short out the middle pin with "U5V" instead of "E5V".
7. Connect the Nucleo to your computer with the ST-Link USB port, not the one on the shoe.
8. Open the STM Cube Programmer and select the firmware file you downloaded from Canvas.
9. Press the "connect" button on the top right corner of the program. If this fails to connect its possible the board is damaged or you may have the jumper not set to "U5V".
Occasionally software running on the Nucleo can lock out the ST-Link. If you think that may be the case, then attempt to connect several times while holding down the black reset button, releasing it approximately as you click on connect in the program.
10. Once connected, press the button near the bottom left corner shaped like an eraser to perform a "full chip erase". If this step fails your Nucleo is most likely damaged.
11. If the chip erase is successful, press the "download" button to flash the interpreter firmware.
11.Once the programming is completed successfully, press the "disconnect" button in the programmer utility.
12. Disconnect the USB cord from the ST-Link.
13. Replace the jumper back on the "E5V" side so that you can use the Shoe of Brian once again.
14. Confirm that you are able to access the REPL through PuTTY and that the PYBFLASH drive mounts properly.
15. Resume your toiling on the lab

### Shoe of Bryan 
You can read about the Shoe in detail here: https://spluttflob.github.io/ME405-Support/shoe_info.html

#### If building from scratch
In addition to the PCB, you need the ferrite bead  and two 4.7k resistors. And the following: 

Component:
Vendor Option:

USB Mini-B
Mouser 710-65100516121

Screw Terminal, 5 Pin
Mouser 651-1725685

Screw Terminal, 10 Pin (Qty. 2)
Mouser 651-1725737

2x19 Receptacle Headers (Qty. 2)
Mouser 517-929975-01-19-RK

Nucleo L476RG
Mouser 511-NUCLEO-L476RG

X-NUCLEO-IHM04A1
Mouser 511-X-NUCLEO-IHM04A1


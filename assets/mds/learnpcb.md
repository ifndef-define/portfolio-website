# Learning PCB Design
What better way to learn PCB design than to make a PCB? Without knowing what I was doing, I decided to make a PCB for a possible robotics project I had in mind. I wanted to make a PCB that would be able to interface with the through-bore REV Robotics quadrature encoders, and be able to send the encoder data on request to the VEX V5 Brain via the RS-485 serial protocol, along with a 9-axis IMU. This would be in the form factor to be used as a Raspberry Pi HAT, which would allow me to use the Raspberry Pi as a controller for the VEX robot.

Obviously, I had no idea what I was doing, and I had never designed a PCB before. So I decided to start with a simple design, and work my way up to more complex designs. I started by designing a simple PCB that would be able to interface with the REV Robotics quadrature encoders, and send the encoder data to the VEX V5 Brain via the RS-485 serial protocol. However, I needed an MCU for this, and settled on the STM32G474 series. This particular MCU has built in hardware timers that would've allowed me to read the quadrature encoder data signals directly, and process the IMU data, and send it to the VEX V5 Brain.

![Learning PCB Schematic](../assets/learnpcb_schem.png)

After designing the schematic, I learned about how to place and route components on a PCB, and how to make sure that the traces are routed correctly, including proper trace width, trace spacing, and via sizes, as well as properly routing differential pairs, and making sure that the traces are routed in a way that minimizes noise and interference. I learned to design for manufacturability, and how to make sure that the PCB can be manufactured easily.

![Learning PCB Layout](../assets/learnpcb_layout.png)
![Learning PCB Render](../assets/learnpcb_render.png)

All together, this was a great learning experience for me, and I learned a lot about PCB design, and how to make sure that the PCB is designed correctly, and can be manufactured easily. While this PCB was never manufactured and still has many glaring issues, I learned a lot about PCB design, and have already gotten newer designs manufactured. I may revisit this design in the future, and make a new version of it for the VEX AI competition.
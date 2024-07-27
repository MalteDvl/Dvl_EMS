# Dvl Demo EMS

This project is for Enpal.One and Fritz Box owners.

It combines the Enpal.One API and the Fritz 200 CERT smart socket API.

Run project using "python main.py FritzPassword"

With http://localhost:5000/ you see the dashboard of your solar system as well as the current state of the Fritz power socket.

Every data collection cycle the house consumption and the socket state are checked. If the house consumption is below 1000 W and the socket is off, it is turned on. If the house consumption is above 1000 W and the socket is on, it is turned off.

![Bild (2)](https://github.com/user-attachments/assets/a44a6b8b-c13a-4fd7-a5ee-9818dc4f43cf)

![Uploading Image.jpg…]()

# FMC IOC Blocking Tool
**Author:** Mohamed Abdallah

## Overview
The **FMC IOC Blocking Tool** is a desktop automation tool designed to assist IT Cybersecurity team at COS in efficiently blocking Indicators of Compromise (IOCs) in FMC.
The tool uses Playwright to automate browser interactions.

---

## Downloading and Using the FMC Tool

### Downloading / Updating the Tool
1. Navigate to the FMC Tool GitHub repository:  
   https://github.com/Mohamed6886/COS_IOC-Blocking-Tool  
2. Click the **Releases** section on the right-hand side of the repository page.
3. Download the latest release package:  
   **`FMC.Tool.zip`**
4. Extract the ZIP file to a local directory on your machine.

---

## Included Files Overview
After extraction, the folder will contain the following:

### **FMC Tool.exe**
The executable used to launch and run the FMC IOC Blocking Tool.  
No additional setup is required to run the tool.

### **.env**
Configuration file used to store FMC environment URLs (e.g., FMC5 and FMC3).  
This file can be updated if FMC URLs change, without modifying any source code.

### **browsers/** folder
Contains a Chromium browser used by Playwright for automation.

If this folder is not present, Playwright will automatically fall back to its default browser installation location:

```C:\Users<username>\AppData\Local\ms-playwright```

---

## Launching the Tool
1. Double-click **FMC Tool.exe**.
2. The FMC Tool graphical interface will appear.

<img width="975" height="545" alt="FMC Tool Interface" src="https://github.com/user-attachments/assets/8effc946-f4c0-4dc3-8766-72f9eb60ea73" />

---

## Tool Interface Overview

### **FMC Environment Dropdown**
Allows selection between FMC environments (e.g., FMC5 or FMC3), based on values defined in the `.env` file.

### **IOC Count Field**
Specifies the number of IOCs to block during the current run.

### **Log Window**
Displays real-time status messages as the tool executes, including navigation steps, batch progress, and completion status.

---

## Running the Tool
1. Select the appropriate FMC environment from the dropdown.
2. Enter the number of IOCs to block.
3. Click **Start**.

The tool will then:
- Open a web browser window
- Navigate to FMC
- Prompt the user to manually sign in

Once authentication is complete, the automation proceeds automatically.  
No further user interaction is required.

---

## Notes
- It is recommended that **only one instance of the tool be run at a time** to avoid unexpected behavior.
- The source code is maintained in this repository to support updates, improvements, and onboarding of future interns.


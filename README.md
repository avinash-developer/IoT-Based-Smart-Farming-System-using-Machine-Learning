# Smart Farming System with IoT and AI

This repository contains the code and documentation for an Internet of Things (IoT)-enabled smart farming system that leverages Artificial Intelligence (AI) for enhanced agricultural management.

## Overview

The smart farming system integrates various sensors and AI models to monitor and improve crop health and environmental conditions. The primary components of the system include:

- **Sensors**: Flame, DHT (temperature and humidity), and soil moisture sensors for real-time monitoring.
- **Manual Input**: NPK (Nitrogen, Phosphorus, Potassium) value input for soil health assessment.
- **Image Detection**: Using the YOLO model and OpenCV for crop health assessment.
- **Crop Recommendation**: Random Forest classification system for providing crop recommendations based on sensor data and image analysis.
- **Central Processing**: Raspberry Pi serves as the central processing unit for data collection, analysis, and decision-making.
- **Animal Monitoring System**: Animals can be monitored using yolo model code can be found on camera.py. Add IP address of your webcam for the working.

## Features

- Real-time monitoring of environmental conditions and soil health.
- Image-based crop health assessment using YOLO and OpenCV.
- Crop recommendations based on sensor data and image analysis.
- Centralized control and processing with Raspberry Pi.
- Enhanced agricultural management to maximize output, minimize resource usage, and promote sustainable farming practices.
- Risk mitigation against diseases, pests, and adverse weather patterns.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/smart-farming-system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd smart-farming-system
    ```
3. Set up the Raspberry Pi and connect the sensors as per the hardware documentation.

## Usage

1. Run the main application:
    ```bash
    python main.py
    ```
2. Input the NPK values manually when prompted.
3. The system will automatically start monitoring the sensors and analyzing the data.
4. Crop health assessments and recommendations will be provided based on the collected data and image analysis.

## Publication

For more details, please refer to our publication:

- **Title**: IoT-enabled Smart Farming System with AI Capabilities
- **Journal**: International Journal for Research in Applied Science and Engineering Technology
- **DOI**: [10.22214/ijraset.2024.63365](https://doi.org/10.22214/ijraset.2024.63365)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact us at [avinashcawasthi@gmail.com](mailto:your-email@example.com).


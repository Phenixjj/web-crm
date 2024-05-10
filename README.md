# Web-CRM Project

This is a web-based Customer Relationship Management (CRM) system, designed to help businesses manage customer data and customer interaction, access business information, automate sales, marketing, and customer support.

## Technologies

This project utilizes a range of modern technologies to deliver a robust and efficient CRM system:

- **Docker**: Used for creating isolated environments to run the software and its dependencies.
- **Docker Compose**: Used for defining and running multi-container Docker applications.
- **Python**: The main programming language used for developing the application.
- **Javascript**: Used to make web pages interactive and create dynamic web content.
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **MinIO**: High performance, Kubernetes Native Object Storage.
- **Redis**: An open-source, in-memory data structure store, used as a database, cache, and message broker.
- **Ollama**: A service used in the project (replace with actual description).
- **Bot API**: A dedicated micro-service for handling bot interactions using FastAPI.


## Features

- **Customer Management**: Manage and track customer information in one place.
- **Sales Automation**: Automate your sales process.
- **Customer Support**: Provide excellent customer service with our integrated support tools.
- **Video/Text Chat**: This feature allows users to communicate effectively with each other in real-time through video or text messaging, enhancing collaboration and productivity.
- **Bot AI API**: A dedicated service for handling bot interactions with AI LLM.
- **Data Storage**: Utilizes MinIO for efficient and secure data storage.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repo
```bash
git clone https://github.com/Phenixjj/web-crm.git
```
2. Navigate to the project directory
```bash
cd web-crm
```
3. Start the services
```bash
docker-compose up -d
```

## Usage

Once the services are up and running, navigate to `http://localhost:8000` in your web browser to access the CRM system.
The Bot API can be accessed at `http://localhost:5001`.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create.
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Jean LECIGNE - [@Linkedin](https://www.linkedin.com/in/jean-lecigne-68aa0320a/)

Project Link: [https://github.com/Phenixjj/web-crm.git](https://github.com/Phenixjj/web-crm.git)


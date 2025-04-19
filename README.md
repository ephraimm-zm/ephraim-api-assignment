
# Weather App - Deployment and Load Balancer Configuration Guide

## Introduction
This application is a weather app that integrates with the OpenWeather API to fetch and display weather data for any given city. Users can input a city name, and the app will retrieve the current weather and display it on the page. The application is deployed on two web servers behind an Nginx load balancer to ensure high availability and fault tolerance.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Overview](#deployment-overview)
3. [Server Deployment](#server-deployment)
4. [Load Balancer Configuration](#load-balancer-configuration)
5. [API Integration](#api-integration)
6. [Error Handling](#error-handling)
7. [User Interaction with Data](#user-interaction-with-data)
8. [User Interface](#user-interface)
9. [Demo Video](#demo-video)
10. [API and Resource Attribution](#api-and-resource-attribution)

---

## Prerequisites
Before you begin, ensure that you have the following installed on your web servers:

1. **Ubuntu 20.04 or later**
2. **Nginx** - for load balancing.
3. **Gunicorn** - for running the Flask app.
4. **Flask** - for the app framework.
5. **Python 3** - for running Flask.
6. **OpenWeather API Key** - required for fetching weather data.

You also need access to two web servers and a load balancer (Nginx) configured to route traffic to these servers.

---

## Deployment Overview
The deployment process consists of the following steps:
1. **Install Dependencies** (Nginx, Gunicorn, Flask, etc.).
2. **Deploy the Weather App** on two web servers.
3. **Configure the Load Balancer** (Nginx) to distribute traffic between the servers.

---

## Server Deployment

1. **Clone the repository** to your server:

    ```bash
    git clone https://github.com/ephraimm-zm/ephraim-api-assignment.git
    cd weather-app
    ```

2. **Set up the environment variables:**

    Create a `.env` file with the following content:

    ```bash
    OPENWEATHER_API_KEY=your-api-key
    ```

3. **Create the Gunicorn systemd service:**

    Create a file at `/etc/systemd/system/api-assignment.service` with the following content:

    ```ini
    [Unit]
    Description=Gunicorn for API Assignment Weather App
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/weather-app
    ExecStart=/usr/local/bin/gunicorn --workers 4 --bind unix:/tmp/api-assignment.sock app:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

4. **Start the Gunicorn service:**

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start api-assignment
    sudo systemctl enable api-assignment
    ```

5. **Verify the Gunicorn service is running:**

    ```bash
    sudo systemctl status api-assignment
    ```

Repeat these steps for both web servers.

---

## Load Balancer Configuration

1. **Install Nginx** on your load balancer server:

    ```bash
    sudo apt update
    sudo apt install nginx
    ```

2. **Configure Nginx to load balance between the two servers:**

    Edit `/etc/nginx/sites-available/default` with the following configuration:

    ```nginx
    upstream app_servers {
        server 192.168.1.101;  # IP of web server 1
        server 192.168.1.102;  # IP of web server 2
    }

    server {
        listen 80;
        server_name your-domain.com;

        location /api-assignment {
            proxy_pass http://app_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Other configurations for static content
        location / {
            try_files $uri $uri/ =404;
        }
    }
    ```

3. **Restart Nginx:**

    ```bash
    sudo systemctl restart nginx
    ```

This configuration ensures that incoming traffic is evenly distributed between the two web servers.

---

## API Integration

The application integrates with the **OpenWeather API** to fetch weather data. The API key is stored securely in the `.env` file, and the app retrieves it using the `os.getenv` function.

The API request is made with the following endpoint:

```python
url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
```

## Error Handling

The app includes basic error handling:

- If the city entered by the user is not found, an error message is displayed.
- If the API fails to respond, an appropriate message is shown to the user.

---

## User Interaction with Data

Users interact with the app by entering a city name and submitting the form. The app fetches the weather data for the specified city and displays it. This interaction is simple but effective, offering users meaningful feedback based on the data.

---

## User Interface

The user interface is designed to be simple and intuitive. The form allows users to input a city name, and the results are presented in a clear format with weather data displayed in a readable and organized manner.

---

## Demo Video

Link to video showcasing the functionality of the app:

The video highlights:

- User interaction with the city input form.
- How the weather data is fetched and displayed.
- Error handling for invalid city names.

---

## API and Resource Attribution

This application uses the **OpenWeather API** for fetching weather data. You can access the API documentation here: [OpenWeather API](https://openweathermap.org/api).

---

## Conclusion

This weather app serves a practical purpose by providing users with up-to-date weather information. The deployment process, including the configuration of web servers and load balancer, ensures that the app is reliable and scalable. The integration with the OpenWeather API is secure, and the error handling guarantees a smooth user experience even in the case of issues such as invalid city names or API downtime.

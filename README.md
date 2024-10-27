
# Image Downloader CLI with Clean Architecture


## Overview

**Image Downloader CLI** is a command-line tool to download and store images based on user-defined search queries. The tool is designed using **Clean Architecture** principles for maintainability and modularity, and it supports efficient, concurrent downloading of images.

## Features

- **Asynchronous Image Downloading**
- **Image Processing with Resizing**
- **PostgreSQL Integration**
- **Google Image Search API Integration**
- **Dockerized Deployment**


## Prerequisites

- **Python 3.10** or higher
- **Docker** (for containerization)
- **PostgreSQL** (setup via Docker)
- **Google API Key** and **Custom Search Engine ID**

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/image-downloader-cli.git
   cd image-downloader-cli
   ```

2. **Environment Variables**

   Create a `.env` file in the root directory with the necessary configuration:

   ```env
   # Google API
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_cse_id

   # PostgreSQL
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_postgres_database
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432

   # Image Processing
   MAX_IMAGE_SIZE=800,600
   ```

3. **Install Dependencies**

   If running locally:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Docker Setup**

   Build the Docker image and run services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

## Usage

### Command-Line Interface

Run:

```bash
python main.py --query "cute kittens" --max-results 10
```

### Running in Docker

```bash
docker-compose run --rm image_downloader --query "turtle" --max-results 20
```

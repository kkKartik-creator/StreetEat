Streeteats: Empowering Street Food Vendors
Streeteats is a web application developed for Tutedude's Web Development Hackathon 1.0: Solving for Street Food. Our project aims to address the challenges faced by street food vendors by providing them with a platform to connect with a larger customer base, manage their business more efficiently, and gain valuable insights into the market.

🚀 Problem Statement
Street food vendors are an integral part of our culture and economy, yet they often face significant challenges that limit their growth and profitability. These challenges include:

Limited Visibility: Difficulty in reaching a wider audience beyond their immediate location.

Inefficient Operations: Lack of tools for managing orders, tracking sales, and analyzing business performance.

Market Disconnect: Limited access to real-time market data, making it difficult to make informed decisions about pricing and sourcing.

Lack of Credibility: Difficulty in building trust and credibility with customers due to the informal nature of their business.

✨ Solution
Streeteats is a comprehensive solution designed to empower street food vendors by providing them with the tools and resources they need to thrive in a competitive market. Our platform offers a range of features that help vendors overcome the challenges they face and grow their business.

🌟 Features
Vendor Profiles: A dedicated page for each vendor to showcase their menu, prices, and location, helping them attract more customers.

Real-time Market Data: Access to live market data, including pricing trends and availability of raw materials, enabling vendors to make informed decisions.

Supplier Directory: A comprehensive directory of suppliers, complete with ratings and reviews, to help vendors find the best sources for their ingredients.

Business Analytics: An intuitive dashboard that provides vendors with valuable insights into their sales, revenue, and customer behavior.

Alerts and Notifications: Real-time alerts on market trends, price fluctuations, and other important information to help vendors stay ahead of the competition.

💻 Technology Stack
Backend: Flask, Flask-SQLAlchemy

Database: SQLite

Frontend: HTML, CSS, JavaScript

Deployment: Render

🗄️ Database Schema
The application uses a SQLite database with the following tables:

raw_materials: Stores information about raw materials, including their name, category, and price.

market_regions: Contains data on different market regions and their major markets.

daily_market_data: Stores daily market data for various raw materials in different regions.

market_alerts: Keeps track of market alerts and notifications for vendors.

suppliers: A directory of suppliers with their contact information, ratings, and reviews.

vendor_ratings: Stores ratings and reviews for vendors, helping them build credibility with customers.

🚀 Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.x

Pip

Installation
Clone the repo

git clone https://github.com/your_username_/Streeteats.git](https://github.com/kkKartik-creator/StreetEat

Install Python packages

pip install -r requirements.txt

Initialize the database

python -c "from app import init_database; init_database()"

Run the application

flask run

📄 API Endpoints
The application exposes the following API endpoints:

GET /: Renders the home page.

GET /market-trends: Displays real-time market trends and data.

GET /suppliers: Provides a list of suppliers with their details.

GET /business-insights: Shows business analytics and insights for vendors.

POST /filter-vendors: Filters vendors based on various criteria.

👥 Team
TeamNullPointers

📄 License
Distributed under the MIT License. See LICENSE for more information.

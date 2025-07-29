# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
DATABASE = 'market_data.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return conn

def init_database():
    """Initialize database with tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create raw_materials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_materials (
            material_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_of_measurement TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_price REAL DEFAULT 0.0
        )
    ''')
    
    # Create market_regions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_regions (
            region_id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_name TEXT NOT NULL,
            state TEXT NOT NULL,
            major_markets TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create daily_market_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            date DATE NOT NULL,
            avg_price REAL NOT NULL,
            min_price REAL NOT NULL,
            max_price REAL NOT NULL,
            availability_percentage INTEGER,
            quality_grade_a_percent INTEGER DEFAULT 0,
            quality_grade_b_percent INTEGER DEFAULT 0,
            quality_grade_c_percent INTEGER DEFAULT 0,
            stock_level TEXT DEFAULT 'medium',
            supplier_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES raw_materials (material_id),
            FOREIGN KEY (region_id) REFERENCES market_regions (region_id)
        )
    ''')
    
    # Create market_alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            region_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES raw_materials (material_id),
            FOREIGN KEY (region_id) REFERENCES market_regions (region_id)
        )
    ''')
    
    conn.commit()
    conn.close()

## Sample data loader functions
import sqlite3
import os  
import json
def bulk_add_raw_materials():
    items = [
        # Vegetables
        ('Cabbage', 'Vegetables', 'kg', 'Fresh green cabbage', 30),
        ('Carrot', 'Vegetables', 'kg', 'Crunchy carrots', 40),
        ('Green Chilli', 'Vegetables', 'kg', 'Hot green chillies', 70),
        ('Potato', 'Vegetables', 'kg', 'Starchy potatoes', 25),
        ('Onion', 'Vegetables', 'kg', 'Pungent onions', 35),
        ('Tomato', 'Vegetables', 'kg', 'Juicy tomatoes', 40),
        ('Cauliflower', 'Vegetables', 'kg', 'Snow-white cauliflower', 45),
        ('Spinach', 'Vegetables', 'bundle', 'Fresh spinach leaves', 12),
        ('Capsicum', 'Vegetables', 'kg', 'Bell peppers in all colours', 60),
        ('Brinjal', 'Vegetables', 'kg', 'Purple eggplants', 35),

        # Spices
        ('Garlic', 'Spices', 'kg', 'Strong aroma garlic', 120),
        ('Ginger', 'Spices', 'kg', 'Zesty ginger roots', 100),
        ('Turmeric', 'Spices', 'kg', 'Ground turmeric powder', 200),
        ('Red Chilli Powder', 'Spices', 'kg', 'Fiery red powder', 300),
        ('Cumin Seeds', 'Spices', 'kg', 'Earthy cumin seeds', 250),
        ('Mustard Seeds', 'Spices', 'kg', 'Tiny black mustard', 180),
        ('Coriander Powder', 'Spices', 'kg', 'Aromatic dhaniya powder', 160),
        ('Garam Masala', 'Spices', 'kg', 'Blend of powerful masalas', 350),
        ('Fenugreek Seeds', 'Spices', 'kg', 'Bitter methi dana', 90),
        ('Asafoetida', 'Spices', 'g', 'Strong hing powder', 1500),  # Hing be like: "Main gold hoon"

        # Dairy
        ('Milk', 'Dairy', 'litre', 'Full-cream milk', 60),
        ('Paneer', 'Dairy', 'kg', 'Cottage cheese', 320),
        ('Curd', 'Dairy', 'kg', 'Thick homemade dahi', 70),
        ('Butter', 'Dairy', 'kg', 'Amul ka butter', 480),
        ('Cheese', 'Dairy', 'kg', 'Mozzarella/processed cheese', 400),

        # Staples
        ('Sugar', 'Staples', 'kg', 'Granulated sugar', 45),
        ('Salt', 'Staples', 'kg', 'Iodized table salt', 20),
        ('Wheat Flour', 'Staples', 'kg', 'Whole wheat atta', 32),
        ('Rice', 'Staples', 'kg', 'Long grain basmati', 60),
        ('Pulses', 'Staples', 'kg', 'Mixed dals - arhar, moong, chana', 85),
        ('Maida', 'Staples', 'kg', 'Refined white flour', 40),
        ('Poha', 'Staples', 'kg', 'Flattened rice', 35),
        ('Suji', 'Staples', 'kg', 'Semolina for halwa/idli', 38),
        ('Besan', 'Staples', 'kg', 'Gram flour', 120),
        ('Cooking Oil', 'Staples', 'litre', 'Refined sunflower/mustard oil', 135),

        # Leaves/Herbs
        ('Coriander', 'Leaves', 'bundle', 'Fresh coriander leaves', 10),
        ('Mint', 'Leaves', 'bundle', 'Cool pudina leaves', 12),
        ('Curry Leaves', 'Leaves', 'bundle', 'Fragrant curry patta', 15),

        # Condiments
        ('Pickle', 'Condiments', 'kg', 'Spicy mango or lemon pickle', 100),
        ('Ketchup', 'Condiments', 'litre', 'Tomato ketchup bottle', 90),
        ('Vinegar', 'Condiments', 'litre', 'Synthetic vinegar', 25),
        ('Soya Sauce', 'Condiments', 'litre', 'Dark Chinese flavour', 40),

        # Bakery / Packaged
        ('Bread', 'Bakery', 'pack', 'White or brown bread loaf', 30),
        ('Buns', 'Bakery', 'pack', 'Pav buns for vada pav', 25),
        ('Biscuits', 'Bakery', 'pack', 'Parle-G ya Marie', 10),
        ('Noodles', 'Packaged', 'pack', 'Instant noodles packet', 15),
        ('Cornflakes', 'Packaged', 'pack', 'Breakfast cereal', 80),

        # Others
        ('Tea Leaves', 'Beverages', 'kg', 'Strong chai patti', 180),
        ('Coffee', 'Beverages', 'kg', 'Instant coffee powder', 300),
        ('Ice Cubes', 'Frozen', 'kg', 'Crushed or block ice', 10),
        ('Lemon', 'Vegetables', 'kg', 'Juicy yellow lemons', 60),
        ('Green Peas', 'Frozen', 'kg', 'Frozen matar', 95),

    ]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO raw_materials (name, category, unit_of_measurement, description, raw_price)
        VALUES (?, ?, ?, ?, ?)
    ''', items)
    conn.commit()
    conn.close()


def bulk_add_regions():
    regions = [
        ('Pune', 'Maharashtra', json.dumps(['Shivaji Market', 'Mandai'])),
        ('Hyderabad', 'Telangana', json.dumps(['Bowenpally Market'])),
        ('Kolkata', 'West Bengal', json.dumps(['Sealdah', 'Koley Market'])),
        ('Ahmedabad', 'Gujarat', json.dumps(['Jamalpur Market'])),
        ('Chennai', 'Tamil Nadu', json.dumps(['Koyambedu Market'])),
        ('Delhi', 'Delhi', json.dumps(['Azadpur Mandi', 'Ghanta Ghar Market'])),
        ('Bengaluru', 'Karnataka', json.dumps(['KR Market', 'Yeshwanthpur Market'])),
        ('Mumbai', 'Maharashtra', json.dumps(['Crawford Market', 'Vashi APMC'])),
        ('Lucknow', 'Uttar Pradesh', json.dumps(['Chowk Market', 'Dubagga Mandi'])),
        ('Indore', 'Madhya Pradesh', json.dumps(['Rajkumar Market', 'Chhawani Mandi'])),
    ]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO market_regions (region_name, state, major_markets)
        VALUES (?, ?, ?)
    ''', regions)
    conn.commit()
    conn.close()

import random
from datetime import datetime, timedelta

def generate_market_data(days=90):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT material_id FROM raw_materials")
    material_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT region_id FROM market_regions")
    region_ids = [row[0] for row in cursor.fetchall()]
    
    today = datetime.today()

    for day_offset in range(days):
        date = (today - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for mat_id in material_ids:
            for reg_id in region_ids:
                avg = random.uniform(10, 100)
                minp = round(avg * 0.85, 2)
                maxp = round(avg * 1.15, 2)
                avail = random.randint(60, 100)
                grade_a = random.randint(50, 80)
                grade_b = 100 - grade_a - random.randint(5, 15)
                grade_c = 100 - grade_a - grade_b
                stock = random.choice(['low', 'medium', 'high'])
                suppliers = random.randint(2, 10)

                cursor.execute('''
                    INSERT INTO daily_market_data (
                        material_id, region_id, date,
                        avg_price, min_price, max_price,
                        availability_percentage, 
                        quality_grade_a_percent, quality_grade_b_percent, quality_grade_c_percent,
                        stock_level, supplier_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    mat_id, reg_id, date, avg, minp, maxp, avail,
                    grade_a, grade_b, grade_c, stock, suppliers
                ))
    conn.commit()
    conn.close()

def add_sample_data():
    """Add sample data to the database"""
    bulk_add_raw_materials()
    bulk_add_regions()
    generate_market_data(days=90)
    print("Sample data added successfully")
## End of sample data loader functions
###############
# def get_avg_price_index_all_materials(base_date, current_date, region):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         SELECT 
#             base.material_id,
#             base.avg_price AS base_price,
#             current.avg_price AS current_price
#         FROM 
#             daily_market_data base
#         JOIN 
#             daily_market_data current 
#         ON 
#             base.material_id = current.material_id
#         WHERE 
#             base.date = ? AND current.date = ? AND current.region_id = ?
#     ''', (base_date, current_date, region))
    
#     rows = cursor.fetchall()
#     conn.close()
    
#     indices = []
#     for row in rows:
#         material_id, base_price, current_price = row
#         if base_price and current_price and base_price != 0:
#             index = (current_price / base_price) * 100
#             indices.append(index)
    
#     if indices:
#         return round(sum(indices) / len(indices), 2)
#     else:
#         return 0.0

def get_avg_price_index_all_materials(base_date, current_date, region_id):
    conn = sqlite3.connect(DATABASE)  # change this to your actual DB
    cursor = conn.cursor()

    # Get avg_price for base_date
    cursor.execute('''
        SELECT AVG(avg_price)
        FROM daily_market_data
        WHERE date = ? AND region_id = ?
    ''', (base_date, region_id))
    base_avg = cursor.fetchone()[0]

    # Get avg_price for current_date
    cursor.execute('''
        SELECT AVG(avg_price)
        FROM daily_market_data
        WHERE date = ? AND region_id = ?
    ''', (current_date, region_id))
    current_avg = cursor.fetchone()[0]

    conn.close()

    if base_avg and current_avg and base_avg > 0:
        index = current_avg / base_avg
        return round(index, 2)
    else:
        return 0.0



def get_avg_quality_index_all_materials(base_date, current_date, region):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            base.material_id,
            base.quality_grade_a_percent AS base_quality,
            current.quality_grade_a_percent AS current_quality
        FROM 
            daily_market_data base
        JOIN 
            daily_market_data current 
        ON 
            base.material_id = current.material_id
        WHERE 
            base.date = ? AND current.date = ? AND current.region_id = ?
    ''', (base_date, current_date, region))
    
    rows = cursor.fetchall()
    conn.close()
    
    indices = []
    for row in rows:
        material_id, base_quality, current_quality = row
        if base_quality and current_quality:
            index = (current_quality / base_quality) * 100
            indices.append(index)
    
    if indices:
        return round(sum(indices) / len(indices), 2)
    else:
        return None
###############
# Database helper functions
def get_all_regions():
    """Get all market regions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM market_regions ORDER BY region_name')
    regions = cursor.fetchall()
    conn.close()
    return regions

def update_market_data(material_id, region_id, avg_price, stock_level):
    """Update market data for a specific material and region"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE daily_market_data 
        SET avg_price = ?, stock_level = ?, created_at = CURRENT_TIMESTAMP
        WHERE material_id = ? AND region_id = ? AND date = DATE('now')
    ''', (avg_price, stock_level, material_id, region_id))
    
    # If no rows were updated, insert new data
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO daily_market_data 
            (material_id, region_id, date, avg_price, min_price, max_price, stock_level)
            VALUES (?, ?, DATE('now'), ?, ?, ?, ?)
        ''', (material_id, region_id, avg_price, avg_price * 0.9, avg_price * 1.1, stock_level))
    
    conn.commit()
    conn.close()

def add_market_alert(region_id, alert_type, severity, title, message, material_id=None):
    """Add a new market alert"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO market_alerts (material_id, region_id, alert_type, severity, title, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (material_id, region_id, alert_type, severity, title, message))
    conn.commit()
    conn.close()

def get_recent_alerts(region_id=None, limit=10):
    """Get recent alerts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if region_id:
        cursor.execute('''
            SELECT ma.*, rm.name as material_name, mr.region_name
            FROM market_alerts ma
            LEFT JOIN raw_materials rm ON ma.material_id = rm.material_id
            LEFT JOIN market_regions mr ON ma.region_id = mr.region_id
            WHERE ma.region_id = ? AND ma.is_active = 1
            ORDER BY ma.created_at DESC
            LIMIT ?
        ''', (region_id, limit))
    else:
        cursor.execute('''
            SELECT ma.*, rm.name as material_name, mr.region_name
            FROM market_alerts ma
            LEFT JOIN raw_materials rm ON ma.material_id = rm.material_id
            LEFT JOIN market_regions mr ON ma.region_id = mr.region_id
            WHERE ma.is_active = 1
            ORDER BY ma.created_at DESC
            LIMIT ?
        ''', (limit,))
    
    alerts = cursor.fetchall()
    conn.close()
    return alerts

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    all_regions = get_all_regions()
    unique_regions = {region['region_name']: region for region in all_regions}.values()
    return render_template('dashboard.html', regions=unique_regions)

@app.route('/api/dashboard-data')
def dashboard_data():
    r_id = request.args.get('region_id', 1, type=int)
    days = request.args.get('days', 7, type=int)
    print(f"Fetching dashboard data for region ID: {r_id} for the last {days} days")
    # Get real data from database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get summary statistics
    cursor.execute('''
    SELECT 
        AVG(avg_price) as avg_price,
        AVG(availability_percentage) as avg_availability,
        AVG(quality_grade_a_percent) as avg_quality
    FROM daily_market_data 
    WHERE region_id = ? AND date >= DATE('now', ?)
''', (r_id, f'-{days} days'))

    
    stats = cursor.fetchone()
    
    today = datetime.now()
    base_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
    current_date = today.strftime('%Y-%m-%d')

    index = get_avg_price_index_all_materials(
    base_date=base_date,
    current_date=current_date,
    region=r_id
)

    index_last = get_avg_price_index_all_materials(
    base_date=(today - timedelta(days=2 * days)).strftime('%Y-%m-%d'),
    current_date=(today - timedelta(days=days)).strftime('%Y-%m-%d'),
    region=r_id
)

# Safe handling for zero division
    if index_last and index_last != 0:
        percent_change = ((index - index_last) / index_last) * 100
    else:
        percent_change = 0.0

# Format as currency-like string with sign and two decimal places
    sign = "+" if percent_change >= 0 else "-"
    formatted_change = f"{sign}₹{abs(percent_change):.2f}"
    
    summary = {
    'avg_price_index': float(index or 0),  # Default to 0 if index is None
    'avg_price_index_percent': str(formatted_change),  # Default to 0 if index is None
    'avg_price_trend': 'up' if index > 0 else 'down',  # Example
    'quality_score': int(stats['avg_quality']),
    'availability': int(stats['avg_availability']),
    'alert_count': random.randint(1, 5)  # Example, replace with actual count
}

    
    
    # Get top items from database
    cursor.execute("""
    SELECT rm.name, dmd.avg_price, dmd.availability_percentage, dmd.quality_grade_a_percent, dmd.stock_level
    FROM daily_market_data dmd
    JOIN raw_materials rm ON dmd.material_id = rm.material_id
    WHERE dmd.region_id = ?
      AND dmd.date >= DATE('now', ?)
    ORDER BY dmd.avg_price DESC
    LIMIT 5
""", (r_id, f"-{days} days"))  # ✅ FIXED: 2 placeholders, 2 params

    top_items_data = cursor.fetchall()
    top_items = []
    for item in top_items_data:
        cursor.execute("select last_week,last2_week,last3_week from raw_materials where name = ?", (item['name'],))
        res = cursor.fetchone()
        lw=res[0]
        l2w=res[1]
        l3w=res[2]
        cursor.execute("select raw_price from raw_materials where name = ?", (item['name'],))
        raw_price = int(cursor.fetchone()[0] if cursor.fetchone() else 0)
        
        top_items.append({
            'name': item['name'],
            'price': float(raw_price),
            # 'price': float(item['avg_price']),
            'lw': int(lw),
            'l2w': int(l2w),
            'l3w': int(l3w),
            'change': str((raw_price-int(item['avg_price']))/100),  # Calculate this based on historical data
            'trend': 'up' if raw_price > int(item['avg_price']) else 'down',
            'quality': int(item['quality_grade_a_percent'] or 80),
            'availability': item['stock_level'].title()
        })
    
    # Get price trends (sample data for now)
    price_trends = [
        {'week': 'Week 1', top_items[0]['name']: top_items[0]['price'], top_items[1]['name']: top_items[1]['price'], top_items[2]['name']: top_items[2]['price'], top_items[3]['name']: top_items[3]['price']},
        {'week': 'Week 2', top_items[0]['name']: top_items[0]['lw'], top_items[1]['name']: top_items[1]['lw'], top_items[2]['name']: top_items[2]['lw'], top_items[3]['name']: top_items[3]['lw']},
        {'week': 'Week 3', top_items[0]['name']: top_items[0]['l2w'], top_items[1]['name']: top_items[1]['l2w'], top_items[2]['name']: top_items[2]['l2w'], top_items[3]['name']: top_items[3]['l2w']},
        {'week': 'Week 4', top_items[0]['name']: top_items[0]['l3w'], top_items[1]['name']: top_items[1]['l3w'], top_items[2]['name']: top_items[2]['l3w'], top_items[3]['name']: top_items[3]['l3w']}
    ]
    conn.close()
    
    # Get alerts
    alerts_data = get_recent_alerts(r_id, 5)
    alerts = [
        {
            'title': alert['title'],
            'message': alert['message'],
            'severity': alert['severity']
        } for alert in alerts_data
    ]
    
    quality_distribution = [
        {'week': 'Week 1', 'grade_a': 60, 'grade_b': 30, 'grade_c': 10},
        {'week': 'Week 2', 'grade_a': 65, 'grade_b': 25, 'grade_c': 10},
        {'week': 'Week 3', 'grade_a': 55, 'grade_b': 35, 'grade_c': 10},
        {'week': 'Week 4', 'grade_a': 70, 'grade_b': 20, 'grade_c': 10},
    ]
    
    availability_distribution = [
        {'name': 'High Stock', 'value': 45, 'color': '#10B981'},
        {'name': 'Medium Stock', 'value': 35, 'color': '#F59E0B'},
        {'name': 'Low Stock', 'value': 15, 'color': '#EF4444'},
        {'name': 'Out of Stock', 'value': 5, 'color': '#6B7280'},
    ]
    
    return jsonify({
        'summary': summary,
        'price_trends': price_trends,
        'quality_distribution': quality_distribution,
        'availability_distribution': availability_distribution,
        'top_items': top_items,
        'alerts': alerts
    })

# API endpoints for database operations
@app.route('/api/update-price', methods=['POST'])
def update_price():
    """Update price for a material"""
    data = request.json
    material_id = data.get('material_id')
    region_id = data.get('region_id')
    avg_price = data.get('avg_price')
    stock_level = data.get('stock_level', 'medium')
    
    update_market_data(material_id, region_id, avg_price, stock_level)
    
    return jsonify({'status': 'success', 'message': 'Price updated successfully'})

@app.route('/api/add-alert', methods=['POST'])
def add_alert():
    """Add a new market alert"""
    data = request.json
    
    add_market_alert(
        region_id=data.get('region_id'),
        alert_type=data.get('alert_type'),
        severity=data.get('severity'),
        title=data.get('title'),
        message=data.get('message'),
        material_id=data.get('material_id')
    )
    
    return jsonify({'status': 'success', 'message': 'Alert added successfully'})

@app.route('/api/materials')
def get_materials():
    """Get all materials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM raw_materials ORDER BY name')
    materials = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(materials)

# Example usage functions
def example_update_operations():
    """Example of how to perform database operations"""
    
    # Update a price (like your classroom example)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE daily_market_data
        SET avg_price = ?, stock_level = ?
        WHERE material_id = ? AND region_id = ?
    ''', (35.50, "high", 1, 1))
    conn.commit()
    conn.close()
    
    # Add a new alert
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO market_alerts (region_id, alert_type, severity, title, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (1, "price_spike", "high", "Price Alert", "Onion prices increased by 20%"))
    conn.commit()
    conn.close()
    
    # Query with conditions
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rm.name, dmd.avg_price, dmd.stock_level
        FROM daily_market_data dmd
        JOIN raw_materials rm ON dmd.material_id = rm.material_id
        WHERE dmd.region_id = ? AND dmd.avg_price > ?
    ''', (1, 30.0))
    results = cursor.fetchall()
    conn.close()
    
    return results

@app.route('/vendor_performance')
def vendor_performance():
    return render_template('vendor_ratings_page.html')

@app.route('/supplier_performance')
def supplier_performance():
    return render_template('supplier_ratings_page.html')

@app.route('/api/vendor', methods=['POST'])
def get_filtered_vendors():
    filters = request.get_json()
    query = "SELECT * FROM vendor_ratings WHERE 1=1"
    params = []

    # Apply filters
    if filters['business_type'] != 'all':
        query += " AND business_type LIKE ?"
        params.append('%' + filters['business_type'].replace('-', ' ') + '%')
    
    if filters['location'] != 'all':
        query += " AND LOWER(location) LIKE ?"
        params.append('%' + filters['location'].lower() + '%')

    if filters['payment_rating'] != 'all':
        rating_ranges = {
            "excellent": (4.5, 5),
            "good": (3.5, 4.4),
            "fair": (2.5, 3.4),
            "poor": (0, 2.4)
        }
        low, high = rating_ranges[filters['payment_rating']]
        query += " AND payment_score BETWEEN ? AND ?"
        params += [low, high]

    # You can add risk logic too if you have it in DB
    if filters['sort_by'] != 'overall':
        query += f" ORDER BY {filters['sort_by']}_score DESC"
    else:
        query += " ORDER BY overall_rating DESC"

    conn = sqlite3.connect('market_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    vendors = [dict(row) for row in rows]
    return jsonify({'vendors': vendors})


@app.route('/api/vendor-data')
def vendor_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Count of active vendors
    cursor.execute("SELECT COUNT(*) FROM vendor_ratings")
    active_vendors = cursor.fetchone()[0]

    # 2. Average payment score
    cursor.execute("SELECT AVG(payment_score) FROM vendor_ratings")
    avg_payment_score = round(cursor.fetchone()[0] or 0, 2)

    # 3. Monthly volume (assume monthly_volume column exists)
    cursor.execute("SELECT SUM(monthly_revenue) FROM vendor_ratings")
    monthly_volume = round(cursor.fetchone()[0] or 0, 2)

    # 4. High-risk vendors (assume <2.0 score is risky)
    cursor.execute("SELECT COUNT(*) FROM vendor_ratings WHERE payment_score < 2.0")
    highrisk_vendor = cursor.fetchone()[0]

    # 5. Payment Score Distribution Buckets
    buckets = {
        'excellent': "payment_score >= 4.5",
        'good': "payment_score >= 3.5 AND payment_score < 4.5",
        'fair': "payment_score >= 2.5 AND payment_score < 3.5",
        'poor': "payment_score < 2.5"
    }

    paymentscore_distribution = {}
    for label, condition in buckets.items():
        cursor.execute(f"SELECT COUNT(*) FROM vendor_ratings WHERE {condition}")
        paymentscore_distribution[label] = cursor.fetchone()[0]

    # 6. Business type performance: avg payment score + count
    cursor.execute("""
        SELECT business_type, COUNT(*), AVG(payment_score)
        FROM vendor_ratings
        GROUP BY business_type
    """)
    rows = cursor.fetchall()
    business_type_performance = {
        row[0]: {
            'vendor_count': row[1],
            'average_score': round(row[2] or 0, 2),
            'performance': round((row[2] or 0) * (row[1] or 1), 2)  # Sample formula: score * vendor count
        }
        for row in rows
    }

    conn.close()

    return jsonify({
        'active_vendor': active_vendors,
        'avg_payment_score': avg_payment_score,
        'monthly_volume': monthly_volume,
        'highrisk_vendor': highrisk_vendor,
        'paymentscore_distribution': paymentscore_distribution,
        'business_type_performance': business_type_performance
    })

@app.route('/api/suppliers', methods=['POST'])
def suppliers_api():
    filters = request.get_json()
    query = "SELECT * FROM suppliers WHERE 1=1"
    params = []

    # === HTML Filter Matching ===

    # CATEGORY filter
    if filters.get('category') and filters['category'] != 'all':
        query += " AND LOWER(category) LIKE ?"
        params.append('%' + filters['category'].lower() + '%')

    # LOCATION filter
    if filters.get('location') and filters['location'] != 'all':
        query += " AND LOWER(location) LIKE ?"
        params.append('%' + filters['location'].lower() + '%')

    # RATING filter
    if filters.get('rating') and filters['rating'] != 'all':
        rating_val = filters['rating']
        if rating_val == '5':
            query += " AND overall_rating >= 4.9"
        elif rating_val == '4+':
            query += " AND overall_rating >= 4.0"
        elif rating_val == '3+':
            query += " AND overall_rating >= 3.0"

    # === SAFE SORT MAPPING ===
    sort_column_map = {
        'rating': 'overall_rating',
        'reviews': 'num_reviews',
        'name': 'name',
        'price': 'min_order_cost'
    }

    sort_key = filters.get('sort_by', 'rating')  # Default to rating
    sort_column = sort_column_map.get(sort_key, 'overall_rating')

    query += f" ORDER BY {sort_column} DESC"

    # === EXECUTE THE QUERY ===
    try:
        conn = sqlite3.connect('market_data.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        vendors = [dict(row) for row in rows]
        return jsonify({'vendors': vendors})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    # Initialize database
    # init_database()
    # add_sample_data()   
    print("Database initialized with sample data")

    print("Database file:", DATABASE)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

import streamlit as st
import json
import os
import pandas as pd
import math
from io import BytesIO
import numpy as np
from copy import deepcopy

st.set_page_config(
    page_title="DayZ Trader Config Editor",
    page_icon="🧰",
    layout="wide",
)

# Title and description
st.title("DayZ Trader Config Editor")
st.markdown("""
This tool helps you modify DayZ mod configuration files, such as TraderPlus price configs.
Upload your JSON file, make changes, and download the modified version.
""")

# Function to parse product strings into components
def parse_product(product_str):
    parts = product_str.split(',')
    if len(parts) >= 6:
        return {
            "name": parts[0],
            "col2": parts[1],
            "col3": parts[2],
            "stock": parts[3],
            "buy_price": parts[4],
            "sell_price": parts[5]
        }
    return None

# Function to convert product components back to string
def product_to_string(product):
    return f"{product['name']},{product['col2']},{product['col3']},{product['stock']},{product['buy_price']},{product['sell_price']}"

# File upload
uploaded_file = st.file_uploader("Choose a JSON configuration file", type=["json"])

if uploaded_file is not None:
    # Load the JSON data
    try:
        data = json.load(uploaded_file)
        st.success("File loaded successfully!")
        
        # Display some basic info
        st.subheader("Configuration Overview")
        st.write(f"Version: {data.get('Version', 'N/A')}")
        st.write(f"Auto Calculation: {data.get('EnableAutoCalculation', 'N/A')}")
        st.write(f"Auto Destock at Restart: {data.get('EnableAutoDestockAtRestart', 'N/A')}")
        st.write(f"Default Trader Stock: {data.get('EnableDefaultTraderStock', 'N/A')}")
        
        # Get category names for dropdowns and tabs
        categories = data.get('TraderCategories', [])
        category_names = [cat.get('CategoryName', f"Category {i}") for i, cat in enumerate(categories)]
        
        # Sidebar for bulk operations
        st.sidebar.header("Bulk Operations")
        
        # Global price modification
        st.sidebar.subheader("Global Price Modification")
        price_change = st.sidebar.number_input("Price Change (%):", min_value=-99, max_value=500, value=0, step=5)
        
        # Category-specific price modification
        st.sidebar.subheader("Category Price Modification")
        selected_categories = st.sidebar.multiselect("Select Categories:", category_names)
        category_price_change = st.sidebar.number_input("Category Price Change (%):", min_value=-99, max_value=500, value=0, step=5)
        apply_to_buy = st.sidebar.checkbox("Apply to Buy Prices", value=True)
        apply_to_sell = st.sidebar.checkbox("Apply to Sell Prices", value=True)
        
        # Stock level modification
        st.sidebar.subheader("Stock Level")
        new_stock = st.sidebar.text_input("Set All Stock Levels To:", value="-1")
        
        # Apply bulk changes
        if st.sidebar.button("Apply Global Changes"):
            if price_change != 0 or new_stock != "":
                with st.spinner("Applying global changes..."):
                    # Process each category
                    for category in data.get('TraderCategories', []):
                        products = category.get('Products', [])
                        
                        for i, product_str in enumerate(products):
                            parts = product_str.split(',')
                            
                            if len(parts) >= 6:
                                # Apply stock change if specified
                                if new_stock != "":
                                    parts[3] = new_stock
                                
                                # Apply price changes if specified
                                if price_change != 0:
                                    # Buy price (5th column, index 4)
                                    if parts[4] != "-1":
                                        if '.' in parts[4]:
                                            new_price = round(float(parts[4]) * (1 + price_change/100), 2)
                                            parts[4] = str(new_price)
                                        else:
                                            new_price = math.floor(int(parts[4]) * (1 + price_change/100))
                                            parts[4] = str(new_price)
                                    
                                    # Sell price (6th column, index 5)
                                    if parts[5] != "-1":
                                        if '.' in parts[5]:
                                            new_price = round(float(parts[5]) * (1 + price_change/100), 2)
                                            parts[5] = str(new_price)
                                        else:
                                            new_price = math.floor(int(parts[5]) * (1 + price_change/100))
                                            parts[5] = str(new_price)
                                
                                # Update the product string
                                products[i] = ','.join(parts)
                    
                    st.success("Global changes applied successfully!")
        
        # Apply category-specific changes
        if st.sidebar.button("Apply Category Changes"):
            if category_price_change != 0 and selected_categories:
                with st.spinner(f"Applying {category_price_change}% price change to selected categories..."):
                    # Process each selected category
                    for category in data.get('TraderCategories', []):
                        category_name = category.get('CategoryName', '')
                        
                        # Check if this category is selected
                        if category_name in selected_categories:
                            products = category.get('Products', [])
                            
                            for i, product_str in enumerate(products):
                                parts = product_str.split(',')
                                
                                if len(parts) >= 6:
                                    # Apply buy price change if specified
                                    if apply_to_buy and parts[4] != "-1":
                                        if '.' in parts[4]:
                                            new_price = round(float(parts[4]) * (1 + category_price_change/100), 2)
                                            parts[4] = str(new_price)
                                        else:
                                            new_price = math.floor(int(parts[4]) * (1 + category_price_change/100))
                                            parts[4] = str(new_price)
                                    
                                    # Apply sell price change if specified
                                    if apply_to_sell and parts[5] != "-1":
                                        if '.' in parts[5]:
                                            new_price = round(float(parts[5]) * (1 + category_price_change/100), 2)
                                            parts[5] = str(new_price)
                                        else:
                                            new_price = math.floor(int(parts[5]) * (1 + category_price_change/100))
                                            parts[5] = str(new_price)
                                    
                                    # Update the product string
                                    products[i] = ','.join(parts)
                    
                    st.success(f"Price changes applied to {len(selected_categories)} categories!")
        
        # Category tabs
        st.subheader("Categories")
        
        tabs = st.tabs(category_names)
        
        for i, tab in enumerate(tabs):
            with tab:
                category = categories[i]
                products = category.get('Products', [])
                
                # Convert products to a more readable format for display
                parsed_products = []
                for product in products:
                    parsed = parse_product(product)
                    if parsed:
                        parsed_products.append(parsed)
                
                # Display as an editable table
                if parsed_products:
                    # Convert data for editable dataframe
                    df = pd.DataFrame(parsed_products)
                    
                    # Make a copy of the original data for comparison
                    original_df = df.copy()
                    
                    # Use data_editor for an editable spreadsheet-like interface
                    edited_df = st.data_editor(
                        df,
                        use_container_width=True,
                        num_rows="fixed",
                        column_config={
                            "name": st.column_config.TextColumn("Item Name"),
                            "col2": st.column_config.TextColumn("Column 2"),
                            "col3": st.column_config.TextColumn("Column 3"),
                            "stock": st.column_config.TextColumn("Stock Level"),
                            "buy_price": st.column_config.TextColumn("Buy Price"),
                            "sell_price": st.column_config.TextColumn("Sell Price"),
                        },
                        key=f"editor_{i}"
                    )
                    
                    # Check if there were any changes in the data
                    if not original_df.equals(edited_df):
                        # Convert the edited dataframe back to product strings
                        updated_products = []
                        for _, row in edited_df.iterrows():
                            product = {
                                'name': row['name'],
                                'col2': row['col2'],
                                'col3': row['col3'],
                                'stock': row['stock'],
                                'buy_price': row['buy_price'],
                                'sell_price': row['sell_price']
                            }
                            updated_products.append(product_to_string(product))
                        
                        # Update the category's products
                        category['Products'] = updated_products
                        
                        st.success(f"Changes to {category.get('CategoryName', '')} saved!")
                else:
                    st.write("No products in this category.")
        
        # Download button for the modified JSON
        st.subheader("Download Modified Configuration")
        
        if st.button("Generate Download Link"):
            # Convert the data back to JSON
            json_str = json.dumps(data, indent=2)
            
            # Create a download link
            b64 = BytesIO(json_str.encode()).getvalue()
            
            download_filename = "modified_config.json"
            st.download_button(
                label="Download Modified JSON",
                data=b64,
                file_name=download_filename,
                mime="application/json",
            )
            
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.write("Please make sure your file is a valid JSON configuration.")
else:
    st.info("Please upload a file to get started.")

# Footer
st.markdown("---")
st.markdown("DayZ Trader Config Editor - Created for easy mod configuration management.")

# Display helpful hints
with st.expander("How to use this app"):
    st.markdown("""
    ### Basic Usage:
    1. **Upload** your TraderPlus JSON configuration file
    2. **Browse** through categories using the tabs
    3. **Edit** prices directly in the table cells
    4. **Apply** bulk changes using the sidebar controls
    5. **Download** the modified configuration
    
    ### Types of Changes You Can Make:
    - **Global Changes**: Apply price changes or stock settings to all items
    - **Category Changes**: Select specific categories for price adjustments
    - **Item-Specific Changes**: Edit individual items directly in the table
    
    ### Tips:
    - Use **-1** for stock level to set unlimited stock
    - Use the tabs to navigate between different trader categories
    - Changes are saved automatically when you edit the table
    - Always download your changes before closing the app
    """)

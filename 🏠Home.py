import streamlit as st
import pandas as pd
from PIL import Image
import io
import base64

# Simulated database (replace with actual database in production)
users_db = pd.DataFrame(columns=['username', 'email', 'password', 'is_seller'])
products_db = pd.DataFrame(columns=['seller', 'name', 'description', 'price', 'category', 'image', 'video_proof'])

def main():
    st.title("Used Clothing and Creator Content Platform")

    menu = ["Home", "Login", "Register", "Seller Dashboard", "Buyer Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home()
    elif choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Seller Dashboard":
        seller_dashboard()
    elif choice == "Buyer Dashboard":
        buyer_dashboard()

def home():
    st.write("Welcome to our platform! Buy and sell used clothing with ease. As a seller, you must provide video proof to ensure item authenticity.")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        # Implement login logic
        user = users_db[users_db['username'] == username]
        if not user.empty and user['password'].values[0] == password:
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")

def register():
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type='password')
    is_seller = st.checkbox("Register as a seller")
    if st.button("Register"):
        # Save user details in simulated database
        users_db.loc[len(users_db)] = [new_username, new_email, new_password, is_seller]
        st.success(f"Account created for {new_username}!")

def seller_dashboard():
    st.subheader("Seller Dashboard")
    st.write("Manage your products and content here.")

    # Add product form
    st.subheader("Add New Product")
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    product_price = st.number_input("Price", min_value=0.0, step=0.01)
    product_category = st.selectbox("Category", ["Clothing", "Accessories", "Digital Content"])

    # Upload image
    product_image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

    # Upload video proof for the product
    product_video = st.file_uploader("Upload Video Proof", type=['mp4', 'mov'])

    if st.button("Add Product"):
        # Check that both image and video are provided
        if product_image and product_video:
            products_db.loc[len(products_db)] = [st.session_state['username'], product_name, product_description, product_price, product_category, product_image, product_video]
            st.success("Product added successfully!")
        else:
            st.error("Please upload both image and video proof.")

    # List existing products
    st.subheader("Your Products")
    seller_products = products_db[products_db['seller'] == st.session_state['username']]
    for index, product in seller_products.iterrows():
        st.write(f"**{product['name']}** - ${product['price']}")
        st.image(product['image'])
        st.video(product['video_proof'])

def buyer_dashboard():
    st.subheader("Buyer Dashboard")
    st.write("Browse and buy products.")

    # Display all products
    for index, product in products_db.iterrows():
        st.write(f"**{product['name']}** - ${product['price']}")
        st.image(product['image'])
        st.video(product['video_proof'])

        if st.button(f"Buy {product['name']}"):
            st.success(f"Purchase complete! You'll receive {product['name']} soon.")

if __name__ == "__main__":
    main()

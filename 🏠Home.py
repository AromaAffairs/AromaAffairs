import streamlit as st
import pandas as pd
from PIL import Image

# Simulated database (replace with actual database in production)
users_db = pd.DataFrame(columns=['username', 'email', 'password', 'tipo_usuario'])
products_db = pd.DataFrame(columns=['creator', 'nombre', 'descripcion', 'precio', 'categoria', 'imagen'])
purchases_db = pd.DataFrame(columns=['buyer', 'producto', 'creator'])

def main():
    st.title("Plataforma de Ropa Usada y Contenido de Creadores")
    
    menu = ["Inicio", "Iniciar Sesión", "Registrarse", "Panel de Creador", "Panel de Comprador"]
    choice = st.sidebar.selectbox("Menú", menu)
    
    if choice == "Inicio":
        inicio()
    elif choice == "Iniciar Sesión":
        iniciar_sesion()
    elif choice == "Registrarse":
        registrarse()
    elif choice == "Panel de Creador":
        panel_creador()
    elif choice == "Panel de Comprador":
        panel_comprador()

def inicio():
    st.write("Bienvenido a nuestra plataforma! Aquí puedes comprar y vender ropa usada, y los creadores pueden subir contenido digital. Para los vendedores, debes proporcionar prueba en video después de la compra para garantizar la autenticidad.")

def iniciar_sesion():
    st.subheader("Iniciar Sesión")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type='password')
    if st.button("Iniciar Sesión"):
        user = users_db[users_db['username'] == username]
        if not user.empty and user['password'].values[0] == password:
            st.session_state['username'] = username
            st.session_state['tipo_usuario'] = user['tipo_usuario'].values[0]
            st.success(f"Has iniciado sesión como {username}")
        else:
            st.error("Nombre de usuario o contraseña incorrectos")

def registrarse():
    st.subheader("Crear Nueva Cuenta")
    new_username = st.text_input("Nombre de usuario")
    new_email = st.text_input("Correo electrónico")
    new_password = st.text_input("Contraseña", type='password')
    tipo_usuario = st.selectbox("Tipo de cuenta", ["Comprador", "Creador"])
    if st.button("Registrarse"):
        users_db.loc[len(users_db)] = [new_username, new_email, new_password, tipo_usuario]
        st.success(f"¡Cuenta creada para {new_username} como {tipo_usuario}!")

def panel_creador():
    if st.session_state.get('tipo_usuario') == 'Creador':
        st.subheader("Panel de Creador")
        st.write("Administra tus productos y contenido aquí.")

        # Crear o actualizar perfil de creador
        st.subheader("Perfil de Creador")
        st.text_input("Nombre")
        st.text_area("Descripción del perfil")
        st.file_uploader("Sube una imagen de perfil", type=['png', 'jpg', 'jpeg'])

        # Añadir nuevo producto
        st.subheader("Añadir Producto")
        nombre_producto = st.text_input("Nombre del producto")
        descripcion_producto = st.text_area("Descripción del producto")
        precio_producto = st.number_input("Precio", min_value=0.0, step=0.01)
        categoria_producto = st.selectbox("Categoría", ["Ropa", "Accesorios", "Contenido Digital"])
        imagen_producto = st.file_uploader("Subir Imagen", type=['png', 'jpg', 'jpeg'])

        if st.button("Añadir Producto"):
            if imagen_producto:
                products_db.loc[len(products_db)] = [st.session_state['username'], nombre_producto, descripcion_producto, precio_producto, categoria_producto, imagen_producto]
                st.success("Producto añadido exitosamente!")
            else:
                st.error("Por favor sube una imagen del producto.")

        # Ver productos creados
        st.subheader("Tus Productos")
        creator_products = products_db[products_db['creator'] == st.session_state['username']]
        for index, product in creator_products.iterrows():
            st.write(f"**{product['nombre']}** - ${product['precio']}")
            st.image(product['imagen'])

        # Subir prueba de video después de la compra
        st.subheader("Subir Prueba de Video para Compras")
        compras = purchases_db[purchases_db['creator'] == st.session_state['username']]
        if not compras.empty:
            for index, compra in compras.iterrows():
                st.write(f"Compra de {compra['buyer']} para el producto: {compra['producto']}")
                video_prueba = st.file_uploader(f"Subir prueba de video para {compra['producto']}", type=['mp4', 'mov'])
                if st.button(f"Subir Prueba para {compra['producto']}"):
                    st.success(f"Prueba de video para {compra['producto']} subida exitosamente.")

    else:
        st.error("Debes iniciar sesión como Creador para acceder a este panel.")

def panel_comprador():
    if st.session_state.get('tipo_usuario') == 'Comprador':
        st.subheader("Panel de Comprador")
        st.write("Explora y compra productos de creadores.")

        # Mostrar productos disponibles
        for index, product in products_db.iterrows():
            st.write(f"**{product['nombre']}** - ${product['precio']}")
            st.image(product['imagen'])

            if st.button(f"Comprar {product['nombre']}"):
                purchases_db.loc[len(purchases_db)] = [st.session_state['username'], product['nombre'], product['creator']]
                st.success(f"Compra de {product['nombre']} realizada exitosamente. El creador subirá la prueba de video pronto.")

    else:
        st.error("Debes iniciar sesión como Comprador para acceder a este panel.")

if __name__ == "__main__":
    main()

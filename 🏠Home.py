import streamlit as st
import pandas as pd
from PIL import Image
import io

# Initialize session state for databases
if 'users_db' not in st.session_state:
    st.session_state.users_db = pd.DataFrame(columns=['username', 'email', 'password', 'tipo_usuario'])
if 'products_db' not in st.session_state:
    st.session_state.products_db = pd.DataFrame(columns=['creator', 'nombre', 'descripcion', 'precio', 'categoria', 'imagen'])
if 'purchases_db' not in st.session_state:
    st.session_state.purchases_db = pd.DataFrame(columns=['buyer', 'producto', 'creator'])
if 'creator_profiles' not in st.session_state:
    st.session_state.creator_profiles = pd.DataFrame(columns=['username', 'nombre', 'descripcion', 'imagen'])

def main():
    st.title("Plataforma de Ropa Usada y Contenido de Creadores")
    
    if 'username' not in st.session_state:
        menu = ["Inicio", "Iniciar Sesión", "Registrarse"]
    elif st.session_state.get('tipo_usuario') == 'Creador':
        menu = ["Inicio", "Mi Perfil", "Mi Tienda", "Añadir Producto", "Cerrar Sesión"]
    else:
        menu = ["Inicio", "Explorar Creadores", "Mis Compras", "Cerrar Sesión"]
    
    choice = st.sidebar.selectbox("Menú", menu)
    
    if choice == "Inicio":
        inicio()
    elif choice == "Iniciar Sesión":
        iniciar_sesion()
    elif choice == "Registrarse":
        registrarse()
    elif choice == "Mi Perfil":
        mi_perfil()
    elif choice == "Mi Tienda":
        mi_tienda()
    elif choice == "Añadir Producto":
        anadir_producto()
    elif choice == "Explorar Creadores":
        explorar_creadores()
    elif choice == "Mis Compras":
        mis_compras()
    elif choice == "Cerrar Sesión":
        cerrar_sesion()

def inicio():
    st.write("Bienvenido a nuestra plataforma! Aquí puedes comprar y vender ropa usada, y los creadores pueden subir contenido digital.")

def iniciar_sesion():
    st.subheader("Iniciar Sesión")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type='password')
    if st.button("Iniciar Sesión"):
        user = st.session_state.users_db[st.session_state.users_db['username'] == username]
        if not user.empty and user['password'].values[0] == password:
            st.session_state['username'] = username
            st.session_state['tipo_usuario'] = user['tipo_usuario'].values[0]
            st.success(f"Has iniciado sesión como {username}")
            st.rerun()
        else:
            st.error("Nombre de usuario o contraseña incorrectos")

def registrarse():
    st.subheader("Crear Nueva Cuenta")
    new_username = st.text_input("Nombre de usuario")
    new_email = st.text_input("Correo electrónico")
    new_password = st.text_input("Contraseña", type='password')
    tipo_usuario = st.selectbox("Tipo de cuenta", ["Comprador", "Creador"])
    if st.button("Registrarse"):
        if new_username and new_email and new_password:
            if new_username in st.session_state.users_db['username'].values:
                st.error("El nombre de usuario ya existe. Por favor, elige otro.")
            else:
                new_user = pd.DataFrame({
                    'username': [new_username],
                    'email': [new_email],
                    'password': [new_password],
                    'tipo_usuario': [tipo_usuario]
                })
                st.session_state.users_db = pd.concat([st.session_state.users_db, new_user], ignore_index=True)
                st.success(f"¡Cuenta creada para {new_username} como {tipo_usuario}!")
        else:
            st.error("Por favor, completa todos los campos.")

def mi_perfil():
    if st.session_state.get('tipo_usuario') == 'Creador':
        st.subheader("Mi Perfil de Creador")
        
        # Get existing profile or create a new one
        profile = st.session_state.creator_profiles[st.session_state.creator_profiles['username'] == st.session_state['username']]
        if profile.empty:
            profile = pd.DataFrame({'username': [st.session_state['username']], 'nombre': [''], 'descripcion': [''], 'imagen': [None]})
            st.session_state.creator_profiles = pd.concat([st.session_state.creator_profiles, profile], ignore_index=True)
        
        nombre = st.text_input("Nombre del perfil", value=profile['nombre'].values[0])
        descripcion = st.text_area("Descripción del perfil", value=profile['descripcion'].values[0])
        imagen = st.file_uploader("Imagen de perfil", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Guardar Perfil"):
            st.session_state.creator_profiles.loc[st.session_state.creator_profiles['username'] == st.session_state['username'], 'nombre'] = nombre
            st.session_state.creator_profiles.loc[st.session_state.creator_profiles['username'] == st.session_state['username'], 'descripcion'] = descripcion
            if imagen:
                st.session_state.creator_profiles.loc[st.session_state.creator_profiles['username'] == st.session_state['username'], 'imagen'] = imagen.getvalue()
            st.success("Perfil actualizado exitosamente!")
            st.rerun()
        
        # Display current profile
        st.subheader("Tu Perfil Actual")
        st.write(f"Nombre: {profile['nombre'].values[0]}")
        st.write(f"Descripción: {profile['descripcion'].values[0]}")
        if profile['imagen'].values[0]:
            st.image(profile['imagen'].values[0], width=200)
    else:
        st.error("Debes iniciar sesión como Creador para acceder a este panel.")

def mi_tienda():
    if st.session_state.get('tipo_usuario') == 'Creador':
        st.subheader("Mi Tienda")
        creator_products = st.session_state.products_db[st.session_state.products_db['creator'] == st.session_state['username']]
        if creator_products.empty:
            st.write("Aún no tienes productos en tu tienda. ¡Añade algunos!")
        else:
            for index, product in creator_products.iterrows():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if product['imagen']:
                        st.image(product['imagen'], width=100)
                with col2:
                    st.write(f"**{product['nombre']}**")
                    st.write(f"Precio: ${product['precio']}")
                    st.write(f"Categoría: {product['categoria']}")
                    if st.button(f"Eliminar {product['nombre']}"):
                        st.session_state.products_db = st.session_state.products_db.drop(index)
                        st.success(f"{product['nombre']} eliminado exitosamente!")
                        st.rerun()
                st.write("---")
    else:
        st.error("Debes iniciar sesión como Creador para acceder a este panel.")

def anadir_producto():
    if st.session_state.get('tipo_usuario') == 'Creador':
        st.subheader("Añadir Nuevo Producto")
        nombre_producto = st.text_input("Nombre del producto")
        descripcion_producto = st.text_area("Descripción del producto")
        precio_producto = st.number_input("Precio", min_value=0.0, step=0.01)
        categoria_producto = st.selectbox("Categoría", ["Ropa", "Accesorios", "Contenido Digital"])
        imagen_producto = st.file_uploader("Subir Imagen", type=['png', 'jpg', 'jpeg'])

        if st.button("Añadir Producto"):
            if nombre_producto and descripcion_producto and precio_producto and categoria_producto and imagen_producto:
                new_product = pd.DataFrame({
                    'creator': [st.session_state['username']],
                    'nombre': [nombre_producto],
                    'descripcion': [descripcion_producto],
                    'precio': [precio_producto],
                    'categoria': [categoria_producto],
                    'imagen': [imagen_producto.getvalue()]
                })
                st.session_state.products_db = pd.concat([st.session_state.products_db, new_product], ignore_index=True)
                st.success("Producto añadido exitosamente!")
                st.rerun()
            else:
                st.error("Por favor, completa todos los campos y sube una imagen del producto.")
    else:
        st.error("Debes iniciar sesión como Creador para acceder a este panel.")

def explorar_creadores():
    st.subheader("Explorar Creadores")
    for index, creator in st.session_state.creator_profiles.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            if creator['imagen']:
                st.image(creator['imagen'], width=100)
        with col2:
            st.write(f"**{creator['nombre']}**")
            st.write(creator['descripcion'])
            if st.button(f"Ver tienda de {creator['nombre']}"):
                ver_tienda_creador(creator['username'])
        st.write("---")

def ver_tienda_creador(creator_username):
    st.subheader(f"Tienda de {creator_username}")
    creator_products = st.session_state.products_db[st.session_state.products_db['creator'] == creator_username]
    for index, product in creator_products.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if product['imagen']:
                st.image(product['imagen'], width=100)
        with col2:
            st.write(f"**{product['nombre']}**")
            st.write(product['descripcion'])
            st.write(f"Categoría: {product['categoria']}")
        with col3:
            st.write(f"Precio: ${product['precio']}")
            if st.button(f"Comprar {product['nombre']}"):
                realizar_compra(product)
        st.write("---")

def realizar_compra(product):
    if 'username' in st.session_state:
        new_purchase = pd.DataFrame({
            'buyer': [st.session_state['username']],
            'producto': [product['nombre']],
            'creator': [product['creator']]
        })
        st.session_state.purchases_db = pd.concat([st.session_state.purchases_db, new_purchase], ignore_index=True)
        st.success(f"Compra de {product['nombre']} realizada exitosamente!")
    else:
        st.error("Debes iniciar sesión para realizar una compra.")

def mis_compras():
    if 'username' in st.session_state:
        st.subheader("Mis Compras")
        user_purchases = st.session_state.purchases_db[st.session_state.purchases_db['buyer'] == st.session_state['username']]
        if user_purchases.empty:
            st.write("Aún no has realizado ninguna compra.")
        else:
            for index, purchase in user_purchases.iterrows():
                st.write(f"Producto: {purchase['producto']}")
                st.write(f"Vendedor: {purchase['creator']}")
                st.write("---")
    else:
        st.error("Debes iniciar sesión para ver tus compras.")

def cerrar_sesion():
    for key in ['username', 'tipo_usuario']:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Has cerrado sesión exitosamente.")
    st.rerun()

if __name__ == "__main__":
    main()

import streamlit as st

st.set_page_config(
    page_title="Radhakrishna Communication",
    page_icon="📱",
    layout="wide"
)

# Sample product catalogue
products = [
    {
        "id": 1,
        "name": "Smartphone",
        "category": "Mobile",
        "price": 12999,
        "description": "A stylish smartphone with a high-quality display and powerful performance.",
        "image": "https://placehold.co/600x400?text=Smartphone",
        "gallery": [
            "https://placehold.co/600x400?text=Smartphone+Front",
            "https://placehold.co/600x400?text=Smartphone+Back",
            "https://placehold.co/600x400?text=Smartphone+Side"
        ]
    },
    {
        "id": 2,
        "name": "Wireless Headphones",
        "category": "Headphones",
        "price": 1499,
        "description": "Enjoy wireless audio with comfortable ear cushions and clear sound.",
        "image": "https://placehold.co/600x400?text=Headphones",
        "gallery": [
            "https://placehold.co/600x400?text=Headphones+Front",
            "https://placehold.co/600x400?text=Headphones+Side",
            "https://placehold.co/600x400?text=Headphones+Case"
        ]
    },
    {
        "id": 3,
        "name": "Mobile Charger",
        "category": "Accessories",
        "price": 499,
        "description": "A compact mobile charger for everyday use.",
        "image": "https://placehold.co/600x400?text=Mobile+Charger",
        "gallery": [
            "https://placehold.co/600x400?text=Charger+Front",
            "https://placehold.co/600x400?text=Charger+Side"
        ]
    },
    {
        "id": 4,
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 1999,
        "description": "A portable Bluetooth speaker for music at home or outdoors.",
        "image": "https://placehold.co/600x400?text=Bluetooth+Speaker",
        "gallery": [
            "https://placehold.co/600x400?text=Speaker+Front",
            "https://placehold.co/600x400?text=Speaker+Back"
        ]
    }
]

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7ff, #eefaff);
}
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #153e75;
    padding: 15px;
}
.product-card {
    background: white;
    padding: 12px;
    border-radius: 15px;
    border: 1px solid #dce5f5;
    margin-bottom: 10px;
}
.price {
    color: #078447;
    font-size: 23px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">'
    '📱 Radhakrishna Communication & Electronics'
    '</div>',
    unsafe_allow_html=True
)

st.caption("Explore our products, prices and product details.")

# Search and category filter
search = st.text_input(
    "🔍 Search Products",
    placeholder="Enter product name..."
)

categories = ["All Categories"] + sorted(
    {p["category"] for p in products}
)

category = st.selectbox(
    "Select Category",
    categories
)

# Filter products
filtered_products = [
    p for p in products
    if search.lower() in p["name"].lower()
    and (
        category == "All Categories"
        or p["category"] == category
    )
]

st.divider()

# Product details page
selected_id = st.session_state.get("selected_product")

if selected_id is not None:
    selected = next(
        (p for p in products if p["id"] == selected_id),
        None
    )

    if selected:
        if st.button("← Back to Catalogue"):
            del st.session_state["selected_product"]
            st.rerun()

        st.header(selected["name"])

        left, right = st.columns([1, 1])

        with left:
            st.image(
                selected["image"],
                use_container_width=True
            )

        with right:
            st.subheader(selected["name"])
            st.write("Category:", selected["category"])

            st.markdown(
                f'<p class="price">₹{selected["price"]:,.2f}</p>',
                unsafe_allow_html=True
            )

            st.write(selected["description"])

        st.subheader("Product Gallery")

        gallery = selected["gallery"]

        gallery_columns = st.columns(
            min(len(gallery), 3)
        )

        for i, image in enumerate(gallery):
            with gallery_columns[i % len(gallery_columns)]:
                st.image(
                    image,
                    use_container_width=True
                )

        # Related products
        related = [
            p for p in products
            if p["category"] == selected["category"]
            and p["id"] != selected["id"]
        ]

        if related:
            st.subheader("Related Products")

            cols = st.columns(
                min(len(related), 3)
            )

            for i, product in enumerate(related):
                with cols[i % len(cols)]:
                    st.image(
                        product["image"],
                        use_container_width=True
                    )
                    st.write(product["name"])
                    st.write(f"₹{product['price']:,.2f}")

                    if st.button(
                        "View Product",
                        key=f"related_{product['id']}"
                    ):
                        st.session_state["selected_product"] = (
                            product["id"]
                        )
                        st.rerun()

    st.stop()

# Main catalogue
st.subheader("Our Product Catalogue")

if not filtered_products:
    st.info("No products found.")
else:
    columns = st.columns(4)

    for index, product in enumerate(filtered_products):
        with columns[index % 4]:
            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )

            st.image(
                product["image"],
                use_container_width=True
            )

            st.markdown(
                f"**{product['name']}**"
            )

            st.markdown(
                f'<p class="price">₹{product["price"]:,.2f}</p>',
                unsafe_allow_html=True
            )

            if st.button(
                "View Details",
                key=f"product_{product['id']}",
                use_container_width=True
            ):
                st.session_state["selected_product"] = (
                    product["id"]
                )
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.caption(
    "© Radhakrishna Communication & Electronics"
)
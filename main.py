import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io
import time


SUPABASE_URL = "https://jhsjdvrlcvqkcqbzaqqc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impoc2pkdnJsY3Zxa2NxYnphcXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzMjA0MDEsImV4cCI6MjA4MDg5NjQwMX0.e5Q9kwOIH2sUIkifRIcs26c9aCYEOtoyoRSOVdrD_Gk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================
# SUPABASE CONFIGURATION
# ============================================


# Initialize Supabase client
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("⚠️ Please check your Supabase credentials!")
    st.stop()

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="T-Shirt Inventory",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - BLACK BACKGROUND WITH RED ACCENTS + LOADING ANIMATION
st.markdown("""
<style>
    /* BLACK background everywhere */
    .main {
        background-color: #000000 !important;
    }
    .stApp {
        background-color: #000000 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #000000 !important;
    }
    [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    
    /* WHITE text for body content */
    body, p, li, td, th, a {
        color: #ffffff !important;
    }
    
    /* Headings - RED */
    h1, h2, h3, h4, h5, h6 {
        color: #dc143c !important;
        font-weight: 600 !important;
    }
    
    /* Input fields - BLACK background with RED border and WHITE text */
    input[type="text"], input[type="password"], input[type="number"], 
    textarea {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
        border-radius: 5px !important;
    }
    
    /* Input placeholders - gray text */
    input::placeholder, textarea::placeholder {
        color: #999999 !important;
        opacity: 0.7 !important;
    }
    
    /* Input labels - RED */
    .stTextInput label, .stNumberInput label, .stSelectbox label, 
    .stTextArea label, .stCheckbox label {
        color: #dc143c !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Metrics - RED labels, WHITE values */
    [data-testid="stMetricLabel"] {
        color: #dc143c !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    /* ===== BUTTONS - RED WITH WHITE TEXT ===== */
    .stButton > button {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        height: 45px !important;
    }
    .stButton > button:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
        border: 2px solid #b30000 !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }
    
    /* Form submit buttons - RED with WHITE text */
    button[kind="primaryFormSubmit"], button[kind="primary"] {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    button[kind="primaryFormSubmit"]:hover, button[kind="primary"]:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
    }
    button[kind="primaryFormSubmit"] *, button[kind="primary"] * {
        color: #ffffff !important;
    }
    
    /* Download buttons - RED with WHITE text */
    .stDownloadButton > button {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    .stDownloadButton > button:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
    }
    .stDownloadButton > button * {
        color: #ffffff !important;
    }
    
    /* ===== DROPDOWN/SELECT - RED WITH WHITE TEXT ===== */
    [data-baseweb="select"] {
        background-color: #dc143c !important;
    }
    [data-baseweb="select"] > div {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    [data-baseweb="select"] input {
        color: #ffffff !important;
        background-color: #dc143c !important;
    }
    [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    [data-baseweb="select"] div {
        color: #ffffff !important;
    }
    [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    
    /* Dropdown when opened */
    [data-baseweb="popover"] {
        background-color: #dc143c !important;
    }
    
    /* Dropdown menu items */
    [role="listbox"] {
        background-color: #dc143c !important;
    }
    [role="option"] {
        background-color: #dc143c !important;
        color: #ffffff !important;
    }
    [role="option"]:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
    }
    [role="option"] * {
        color: #ffffff !important;
    }
    
    /* Selected dropdown value */
    .stSelectbox div[data-baseweb="select"] div {
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Dropdown text specifically */
    [data-baseweb="select"] [data-baseweb="input"] {
        color: #ffffff !important;
    }
    [data-baseweb="select"] [data-baseweb="input-container"] {
        background-color: #dc143c !important;
    }
    [data-baseweb="select"] [data-baseweb="input-container"] * {
        color: #ffffff !important;
    }
    
    /* Form container - BLACK with RED border */
    .stForm {
        background-color: #000000 !important;
        border: 2px solid #dc143c !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    /* Expander - BLACK background with RED */
    .streamlit-expanderHeader {
        background-color: #000000 !important;
        color: #dc143c !important;
        font-weight: 600 !important;
        border: 1px solid #dc143c !important;
    }
    details[open] > .streamlit-expanderContent {
        background-color: #000000 !important;
        border: 1px solid #dc143c !important;
        border-top: none !important;
    }
    
    /* Tabs - RED text */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        background-color: #000000 !important;
        border-bottom: 3px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #dc143c !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #dc143c !important;
    }
    
    /* Dataframe/Tables - BLACK with RED borders */
    .dataframe, .stDataFrame {
        background-color: #000000 !important;
    }
    .dataframe thead tr th {
        background-color: #000000 !important;
        color: #dc143c !important;
        font-weight: 700 !important;
        border: 1px solid #dc143c !important;
    }
    .dataframe tbody tr td {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #dc143c !important;
    }
    
    /* Success messages - BLACK background with GREEN border */
    .stSuccess {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #28a745 !important;
        border-radius: 5px !important;
    }
    .stSuccess * {
        color: #ffffff !important;
    }
    
    /* Error messages - BLACK with RED border */
    .stError {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
        border-radius: 5px !important;
    }
    .stError * {
        color: #ffffff !important;
    }
    
    /* Warning messages - BLACK with YELLOW border */
    .stWarning {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffc107 !important;
        border-radius: 5px !important;
    }
    .stWarning * {
        color: #ffffff !important;
    }
    
    /* Info messages - BLACK with BLUE border */
    .stInfo {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #17a2b8 !important;
        border-radius: 5px !important;
    }
    .stInfo * {
        color: #ffffff !important;
    }
    
    /* Dividers - RED */
    hr {
        border-color: #dc143c !important;
        border-width: 2px !important;
    }
    
    /* Sidebar elements */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #dc143c !important;
    }
    [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Number input increment/decrement buttons - RED with WHITE text */
    button[kind="stepUp"], button[kind="stepDown"] {
        color: #ffffff !important;
        background-color: #dc143c !important;
        border: 1px solid #dc143c !important;
    }
    button[kind="stepUp"] svg, button[kind="stepDown"] svg {
        fill: #ffffff !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #dc143c !important;
    }
    .stCheckbox label span {
        color: #ffffff !important;
    }
    
    /* All markdown text - WHITE */
    .stMarkdown {
        color: #ffffff !important;
    }
    .stMarkdown p {
        color: #ffffff !important;
    }
    .stMarkdown span {
        color: #ffffff !important;
    }
    
    /* Column backgrounds - BLACK */
    [data-testid="column"] {
        background-color: #000000 !important;
    }
    
    /* Make sure all nested elements in buttons/dropdowns are white */
    button *, [data-baseweb="select"] * {
        color: #ffffff !important;
    }
    
    /* Override any conflicting styles */
    .stButton button div, .stButton button span, .stButton button p {
        color: #ffffff !important;
    }
    
    /* Strong/Bold text - WHITE */
    strong, b {
        color: #ffffff !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #dc143c !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONSTANTS
# ============================================
KIDS_SIZES = ["26", "28", "30", "32"]
ADULT_SIZES = ["34 (XS)", "36 (S)", "38 (M)", "40 (L)", "42 (XL)", "44 (XXL)", "46 (XXXL)"]
ORGANIZATIONS = ["Warehouse", "Organization 2", "Event Place"]

# Predefined reasons for IN/OUT
REASONS_IN = [
    "New Stock Arrival",
    "Transfer from Warehouse",
    "Transfer from Other Org",
    "Return/Exchange",
    "Other"
]

REASONS_OUT = [
    "Regular Distribution",
    "VIP Gift",
    "Event Distribution",
    "Transfer to Warehouse",
    "Transfer to Other Org",
    "Damaged/Lost",
    "Other"
]

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_org' not in st.session_state:
    st.session_state.user_org = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

# ============================================
# LOADING ANIMATION
# ============================================
def show_loading():
    """Show loading animation for 4 seconds"""
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>👕 T-Shirt Inventory</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: #dc143c;'>Loading System...</h3>", unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate loading stages
            stages = [
                "Initializing database connection...",
                "Loading user session...",
                "Fetching inventory data...",
                "Preparing dashboard..."
            ]
            
            for i in range(100):
                progress_bar.progress(i + 1)
                stage_index = min(i // 25, len(stages) - 1)
                status_text.markdown(f"<p style='text-align: center; color: #ffffff;'>{stages[stage_index]}</p>", unsafe_allow_html=True)
                time.sleep(0.04)  # 4 seconds total (100 * 0.04)
            
            status_text.markdown("<p style='text-align: center; color: #28a745;'>✅ Ready!</p>", unsafe_allow_html=True)
            time.sleep(0.5)
    
    loading_placeholder.empty()

# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

def authenticate_user(user_id, password):
    """Authenticate user credentials"""
    try:
        response = supabase.table('users').select('*').eq('user_id', user_id).eq('password', password).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Login error: {e}")
        return None

def get_stock_data(organization):
    """Get current stock for an organization"""
    try:
        response = supabase.table('stock').select('*').eq('organization', organization).execute()
        return response.data if response.data else []
    except:
        return []

def get_current_stock(organization, category, size):
    """Get current stock quantity for specific size"""
    try:
        response = supabase.table('stock').select('*').eq('organization', organization).eq('category', category).eq('size', size).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]['quantity']
        return 0
    except:
        return 0

def get_total_shirts(organization):
    """Get total shirts count for organization"""
    try:
        stock_data = get_stock_data(organization)
        if stock_data:
            df = pd.DataFrame(stock_data)
            total = df['quantity'].sum()
            return int(total)
        return 0
    except:
        return 0

def update_stock(organization, category, size, quantity_change, user_name, action_type, reason):
    """Update stock and record transaction with validation"""
    try:
        # Get current stock
        response = supabase.table('stock').select('*').eq('organization', organization).eq('category', category).eq('size', size).execute()
        
        if response.data and len(response.data) > 0:
            # Update existing stock
            current_qty = response.data[0]['quantity']
            new_qty = current_qty + quantity_change
            
            # VALIDATION: Prevent negative stock
            if new_qty < 0:
                return False, f"❌ Cannot remove {abs(quantity_change)} shirts! Only {current_qty} available in Size {size}"
            
            supabase.table('stock').update({'quantity': new_qty}).eq('id', response.data[0]['id']).execute()
        else:
            # Insert new stock entry
            # VALIDATION: Cannot remove from non-existent stock
            if quantity_change < 0:
                return False, f"❌ Cannot remove shirts! Size {size} has 0 stock"
            
            new_qty = max(0, quantity_change)
            supabase.table('stock').insert({
                'organization': organization,
                'category': category,
                'size': size,
                'quantity': new_qty
            }).execute()
        
        # Record transaction with reason
        supabase.table('transactions').insert({
            'organization': organization,
            'volunteer_name': user_name,
            'category': category,
            'size': size,
            'quantity': abs(quantity_change),
            'action_type': action_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }).execute()
        
        return True, "✅ Success"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def record_distribution(organization, volunteer_name, category, size, quantity, customer_name, customer_phone, customer_email):
    """Record distribution with customer details (Event Place only)"""
    try:
        # Check current stock first
        current_stock = get_current_stock(organization, category, size)
        
        if current_stock < quantity:
            return False, f"❌ Cannot distribute {quantity} shirts! Only {current_stock} available in Size {size}"
        
        # Update stock
        success, message = update_stock(organization, category, size, -quantity, volunteer_name, "OUT", "Event Distribution")
        
        if not success:
            return False, message
        
        # Record customer details
        supabase.table('customers').insert({
            'organization': organization,
            'volunteer_name': volunteer_name,
            'category': category,
            'size': size,
            'quantity': quantity,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'timestamp': datetime.now().isoformat()
        }).execute()
        
        return True, "✅ Success"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# ============================================
# LOGIN PAGE
# ============================================

def login_page():
    st.title("👕 T-Shirt Inventory System")
    st.subheader("Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        user_id = st.text_input("User ID", key="login_user_id", placeholder="Enter your user ID")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        st.write("")
        
        if st.button("Login", use_container_width=True):
            if user_id and password:
                with st.spinner("Authenticating..."):
                    user = authenticate_user(user_id, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['user_id']
                        st.session_state.user_org = user['organization']
                        st.session_state.user_name = user['name']
                        st.session_state.is_admin = user.get('is_admin', False)
                        st.session_state.first_load = True
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            else:
                st.warning("⚠️ Please enter both User ID and Password")

# ============================================
# STOCK UPDATE UI COMPONENT (WITH REASONS)
# ============================================

def stock_update_ui(organization):
    """Reusable stock update interface with reasons"""
    st.title(f"📦 {organization}")
    st.subheader("Stock Management")
    
    # Display volunteer name and total shirts
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Volunteer:** {st.session_state.user_name}")
    with col2:
        total_shirts = get_total_shirts(organization)
        st.metric("Total T-Shirts", total_shirts)
    
    st.markdown("---")
    
    # Kids Section
    st.subheader("👶 Kids T-Shirts")
    st.write("")
    
    for size in KIDS_SIZES:
        with st.expander(f"Size {size}", expanded=False):
            # Get current stock
            current_stock = get_current_stock(organization, "Kids", size)
            st.metric(f"Current Stock - Size {size}", current_stock)
            
            col1, col2 = st.columns(2)
            
            # IN Section
            with col1:
                st.write("**Stock IN**")
                qty_in = st.number_input(f"Quantity", min_value=0, value=0, step=1, key=f"kids_in_qty_{size}_{organization}")
                reason_in = st.selectbox(f"Reason", REASONS_IN, key=f"kids_in_reason_{size}_{organization}")
                
                if st.button("Add Stock (IN)", key=f"kids_in_btn_{size}_{organization}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            success, message = update_stock(organization, "Kids", size, qty_in, st.session_state.user_name, "IN", reason_in)
                            if success:
                                st.success(f"✅ Added {qty_in} shirts - {reason_in}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            
            # OUT Section
            with col2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(f"Quantity", min_value=0, value=0, step=1, key=f"kids_out_qty_{size}_{organization}")
                reason_out = st.selectbox(f"Reason", REASONS_OUT, key=f"kids_out_reason_{size}_{organization}")
                
                if st.button("Remove Stock (OUT)", key=f"kids_out_btn_{size}_{organization}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            success, message = update_stock(organization, "Kids", size, -qty_out, st.session_state.user_name, "OUT", reason_out)
                            if success:
                                st.success(f"✅ Removed {qty_out} shirts - {reason_out}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
    
    st.markdown("---")
    
    # Adults Section
    st.subheader("👔 Adult T-Shirts")
    st.write("")
    
    for size in ADULT_SIZES:
        with st.expander(f"{size}", expanded=False):
            # Get current stock
            current_stock = get_current_stock(organization, "Adults", size)
            st.metric(f"Current Stock - {size}", current_stock)
            
            col1, col2 = st.columns(2)
            
            # IN Section
            with col1:
                st.write("**Stock IN**")
                qty_in = st.number_input(f"Quantity", min_value=0, value=0, step=1, key=f"adult_in_qty_{size}_{organization}")
                reason_in = st.selectbox(f"Reason", REASONS_IN, key=f"adult_in_reason_{size}_{organization}")
                
                if st.button("Add Stock (IN)", key=f"adult_in_btn_{size}_{organization}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            success, message = update_stock(organization, "Adults", size, qty_in, st.session_state.user_name, "IN", reason_in)
                            if success:
                                st.success(f"✅ Added {qty_in} shirts - {reason_in}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            
            # OUT Section
            with col2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(f"Quantity", min_value=0, value=0, step=1, key=f"adult_out_qty_{size}_{organization}")
                reason_out = st.selectbox(f"Reason", REASONS_OUT, key=f"adult_out_reason_{size}_{organization}")
                
                if st.button("Remove Stock (OUT)", key=f"adult_out_btn_{size}_{organization}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            success, message = update_stock(organization, "Adults", size, -qty_out, st.session_state.user_name, "OUT", reason_out)
                            if success:
                                st.success(f"✅ Removed {qty_out} shirts - {reason_out}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")

# ============================================
# EVENT PLACE PAGE (with customer details)
# ============================================

def event_place_page():
    """Event Place with customer details capture"""
    st.title("🎪 Event Place")
    st.subheader("T-Shirt Distribution")
    
    # Display volunteer name and total shirts
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Volunteer:** {st.session_state.user_name}")
    with col2:
        total_shirts = get_total_shirts("Event Place")
        st.metric("Total T-Shirts", total_shirts)
    
    st.markdown("---")
    
    with st.form("distribution_form"):
        st.subheader("Customer Details")
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", placeholder="Enter name")
            customer_phone = st.text_input("Phone Number *", placeholder="Enter phone")
        
        with col2:
            customer_email = st.text_input("Email Address *", placeholder="Enter email")
            category = st.selectbox("Category *", ["Kids", "Adults"])
        
        if category == "Kids":
            size = st.selectbox("Size *", KIDS_SIZES)
        else:
            size = st.selectbox("Size *", ADULT_SIZES)
        
        # Show current stock for selected size
        current_stock = get_current_stock("Event Place", category, size)
        st.info(f"📊 Current Stock for {category} Size {size}: **{current_stock}** shirts")
        
        quantity = st.number_input("Quantity *", min_value=1, value=1, step=1)
        
        st.write("")
        submit = st.form_submit_button("Distribute T-Shirt", use_container_width=True)
        
        if submit:
            if customer_name and customer_phone and customer_email:
                with st.spinner("Recording distribution..."):
                    success, message = record_distribution("Event Place", st.session_state.user_name, category, size, quantity, customer_name, customer_phone, customer_email)
                    if success:
                        st.success(f"✅ Distributed {quantity} x {category} Size {size} to {customer_name}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("❌ Please fill all required fields!")
    
    # Show current stock
    st.markdown("---")
    st.subheader("📊 Current Stock at Event Place")
    with st.spinner("Loading stock data..."):
        stock_data = get_stock_data("Event Place")
        if stock_data:
            df = pd.DataFrame(stock_data)
            st.dataframe(df[['category', 'size', 'quantity']], use_container_width=True, hide_index=True)
        else:
            st.info("No stock data available")

# ============================================
# ADMIN PANEL
# ============================================

def admin_panel():
    """Admin panel for managing users and viewing data"""
    st.title("⚙️ Admin Panel")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Stock Overview", "User Management", "Transaction History", "Download Reports"])
    
    # Tab 1: Overview
    with tab1:
        st.subheader("Stock Overview - All Organizations")
        st.write("")
        
        with st.spinner("Loading stock data..."):
            for org in ORGANIZATIONS:
                with st.expander(f"📦 {org}", expanded=True):
                    stock_data = get_stock_data(org)
                    if stock_data:
                        df = pd.DataFrame(stock_data)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            kids_total = df[df['category'] == 'Kids']['quantity'].sum()
                            st.metric("Total Kids T-Shirts", int(kids_total))
                        with col2:
                            adults_total = df[df['category'] == 'Adults']['quantity'].sum()
                            st.metric("Total Adult T-Shirts", int(adults_total))
                        with col3:
                            grand_total = df['quantity'].sum()
                            st.metric("Grand Total", int(grand_total))
                        
                        st.write("")
                        st.dataframe(df[['category', 'size', 'quantity']], use_container_width=True, hide_index=True)
                    else:
                        st.info("No stock data available")
    
    # Tab 2: User Management
    with tab2:
        st.subheader("Create New User")
        st.write("")
        
        with st.form("create_user"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_user_id = st.text_input("User ID *", placeholder="Enter unique user ID")
                new_password = st.text_input("Password *", type="password", placeholder="Enter password")
                new_name = st.text_input("Full Name *", placeholder="Enter volunteer name")
            
            with col2:
                new_org = st.selectbox("Organization *", ORGANIZATIONS)
                is_admin = st.checkbox("Grant Admin Access")
            
            st.write("")
            
            if st.form_submit_button("Create User", use_container_width=True):
                if new_user_id and new_password and new_name:
                    try:
                        with st.spinner("Creating user..."):
                            supabase.table('users').insert({
                                'user_id': new_user_id,
                                'password': new_password,
                                'name': new_name,
                                'organization': new_org,
                                'is_admin': is_admin
                            }).execute()
                            st.success(f"✅ User '{new_user_id}' created successfully!")
                            time.sleep(1)
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error creating user: {e}")
                else:
                    st.error("❌ Please fill all required fields!")
        
        st.markdown("---")
        st.subheader("All Users")
        st.write("")
        
        with st.spinner("Loading users..."):
            try:
                users = supabase.table('users').select('*').execute()
                if users.data:
                    df_users = pd.DataFrame(users.data)
                    st.dataframe(df_users[['user_id', 'name', 'organization', 'is_admin']], use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Error loading users: {e}")
    
    # Tab 3: Transaction History with Reasons
    with tab3:
        st.subheader("Transaction History with Reasons")
        st.write("")
        
        with st.spinner("Loading transaction history..."):
            for org in ORGANIZATIONS:
                with st.expander(f"📜 {org} Transactions", expanded=False):
                    try:
                        transactions = supabase.table('transactions').select('*').eq('organization', org).order('timestamp', desc=True).execute()
                        if transactions.data:
                            df_trans = pd.DataFrame(transactions.data)
                            # Show relevant columns including reason
                            display_cols = ['volunteer_name', 'category', 'size', 'quantity', 'action_type', 'reason', 'timestamp']
                            available_cols = [col for col in display_cols if col in df_trans.columns]
                            st.dataframe(df_trans[available_cols], use_container_width=True, hide_index=True)
                        else:
                            st.info("No transaction data")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    # Tab 4: Download Data
    with tab4:
        st.subheader("Download Reports")
        st.write("")
        
        for org in ORGANIZATIONS:
            st.write(f"**{org}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Stock data
                stock_data = get_stock_data(org)
                if stock_data:
                    df_stock = pd.DataFrame(stock_data)
                    
                    try:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df_stock.to_excel(writer, index=False, sheet_name='Stock')
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            label=f"Download {org} Stock",
                            data=excel_buffer,
                            file_name=f"{org.replace(' ', '_')}_stock_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error creating Excel file: {e}")
                else:
                    st.info("No stock data")
            
            with col2:
                # Transaction history with reasons
                try:
                    transactions = supabase.table('transactions').select('*').eq('organization', org).execute()
                    if transactions.data:
                        df_trans = pd.DataFrame(transactions.data)
                        
                        try:
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                df_trans.to_excel(writer, index=False, sheet_name='Transactions')
                            excel_buffer.seek(0)
                            
                            st.download_button(
                                label=f"Download {org} Transactions",
                                data=excel_buffer,
                                file_name=f"{org.replace(' ', '_')}_transactions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error creating Excel file: {e}")
                    else:
                        st.info("No transaction data")
                except:
                    st.info("No transaction data")
            
            st.markdown("---")
        
        # Customer data for Event Place
        st.write("**Event Place - Customer Data**")
        try:
            customers = supabase.table('customers').select('*').execute()
            if customers.data:
                df_customers = pd.DataFrame(customers.data)
                
                try:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_customers.to_excel(writer, index=False, sheet_name='Customers')
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="Download Customer Data",
                        data=excel_buffer,
                        file_name=f"customers_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error creating Excel file: {e}")
            else:
                st.info("No customer data")
        except:
            st.info("No customer data")

# ============================================
# MAIN APP ROUTING
# ============================================

def main():
    # Show loading animation on first load
    if st.session_state.first_load and st.session_state.logged_in:
        show_loading()
        st.session_state.first_load = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.title("👕 T-Shirt Inventory")
            st.write(f"**User:** {st.session_state.user_name}")
            st.write(f"**Organization:** {st.session_state.user_org}")
            
            # Show total shirts in sidebar
            if not st.session_state.is_admin:
                total = get_total_shirts(st.session_state.user_org)
                st.metric("My Total T-Shirts", total)
            
            st.markdown("---")
            
            if st.button("Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Route to appropriate page
        if st.session_state.is_admin:
            admin_panel()
        elif st.session_state.user_org == "Event Place":
            event_place_page()
        else:
            stock_update_ui(st.session_state.user_org)

if __name__ == "__main__":
    main()



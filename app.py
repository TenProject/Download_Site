import streamlit as st
import os
from datetime import datetime
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="TenProject - Downloads",
    page_icon="📥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #333333; }
    h1, h2, h3 { color: #333333; }
    .main-header { border-bottom: 2px solid #5a9bd4; padding-bottom: 20px; margin-bottom: 20px; display: flex; align-items: center; gap: 20px;}
    .logo-img { max-height: 80px; }
    .sponsor-section { display: none; } /* Hide sponsors */
    
    /* Fix Download Button Style */
    div.stDownloadButton > button {
        background-color: #ffffff;
        color: #2c5d8f;
        border: 2px solid #2c5d8f;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stDownloadButton > button:hover {
        background-color: #2c5d8f;
        color: #ffffff;
        border-color: #2c5d8f;
    }
    div.stDownloadButton > button:active {
        background-color: #1a3c5e;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Logo and Header
# Only try to load logo if it exists
logo_path = "images/image.png" 
if os.path.exists(logo_path):
    col_logo, col_text = st.columns([1, 5])
    with col_logo:
        st.image(logo_path, width=100)
    with col_text:
        st.markdown("<h1>Looking for a specific release?</h1>", unsafe_allow_html=True)
        st.markdown("<p>TenProject releases (Hosted Locally):</p>", unsafe_allow_html=True)
else:
    st.markdown("<div class='main-header'><h1>Looking for a specific release?</h1><p>TenProject releases (Hosted Locally):</p></div>", unsafe_allow_html=True)


# Table Header
c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
c1.markdown("**Release version**")
c2.markdown("**Release date**")
c3.markdown("**Download**")
c4.markdown("**Details**")
st.markdown("---")

# Logic to read local downloads
DOWNLOADS_DIR = "downloads"
if not os.path.exists(DOWNLOADS_DIR):
    st.error(f"Directory '{DOWNLOADS_DIR}' not found.")
else:
    # Auto-unzip/unrar logic
    import zipfile
    import rarfile
    
    # Configure UnRAR path for Windows (User might need to adjust this or have it in PATH)
    # Common locations for WinRAR
    if os.name == 'nt':
        possible_paths = [
            r"C:\Program Files\WinRAR\UnRAR.exe",
            r"C:\Program Files (x86)\WinRAR\UnRAR.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                rarfile.UNRAR_TOOL = path
                break

    # Check for compressed files and extract if needed
    for filename in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        
        # logic for ZIP
        if filename.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_content = zip_ref.namelist()
                    exe_in_zip = [f for f in zip_content if f.endswith(".exe")]
                    if exe_in_zip:
                        exe_name = exe_in_zip[0]
                        exe_path = os.path.join(DOWNLOADS_DIR, exe_name)
                        if not os.path.exists(exe_path):
                            with st.spinner(f"Extracting {filename}..."):
                                zip_ref.extractall(DOWNLOADS_DIR)
            except zipfile.BadZipFile:
                st.warning(f"File {filename} is invalid zip.")

        # logic for RAR
        elif filename.endswith(".rar"):
            try:
                with rarfile.RarFile(file_path) as rar_ref:
                    rar_content = rar_ref.namelist()
                    exe_in_rar = [f for f in rar_content if f.endswith(".exe")]
                    if exe_in_rar:
                        exe_name = exe_in_rar[0]
                        exe_path = os.path.join(DOWNLOADS_DIR, exe_name)
                        if not os.path.exists(exe_path):
                            with st.spinner(f"Extracting {filename}..."):
                                try:
                                    rar_ref.extractall(DOWNLOADS_DIR)
                                except rarfile.RarExecError:
                                    st.error("Error extracting RAR. Make sure UnRAR is installed and in PATH (or WinRAR is installed).")
            except rarfile.Error:
                 st.warning(f"File {filename} is invalid rar or UnRAR not found.")

    # Now look for .exe files (either pre-existing or just extracted)
    files = [f for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".exe")]
    
    if not files:
        st.info("No executable files found (and extraction of .rar/.zip failed or found nothing). Check if you have UnRAR installed.")
    
    for filename in files:
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        
        # Get file stats
        stats = os.stat(filepath)
        mod_time = datetime.fromtimestamp(stats.st_mtime)
        date_str = mod_time.strftime("%b. %d, %Y")
        
        # Assume version based on filename or just "Latest"
        version_display = "v0.1" # Fixed version as requested
        
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            st.markdown(f"**{filename}**")
            
        with col2:
            st.markdown(date_str)
            
        with col3:
            # Streamlit download button
            with open(filepath, "rb") as f:
                st.download_button(
                    label="📥 Download",
                    data=f,
                    file_name=filename,
                    mime="application/vnd.microsoft.portable-executable"
                )
            
        with col4:
            st.markdown(f"**Version: {version_display}**")
        
        st.markdown("<hr style='margin: 5px 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

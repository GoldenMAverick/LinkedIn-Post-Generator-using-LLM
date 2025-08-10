from few_shot import FewShotPosts
from post_generator import generate_post
import streamlit as st
import pyperclip

# Constants
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

def local_css():
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0A66C2;
        color: white;
        border-radius: 20px;
        padding: 10px;
    }
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTitle {
        color: #0A66C2;
        text-align: center;
    }
    .output-container {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def display_post(post):
    st.markdown("""
    <div style='
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        border: 1px solid #ddd;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    '>
        {}
    </div>
    """.format(post.replace('\n', '<br>')), unsafe_allow_html=True)

def handle_copy(post):
    try:
        pyperclip.copy(post)
        st.success("✅ Post copied to clipboard!")
    except Exception:
        st.error("❌ Failed to copy. Please select the text and copy manually.")

def main():
    local_css()
    
    with st.container():
        st.title("✍️ LinkedIn Post Generator")
        st.markdown("### Transform your ideas into engaging LinkedIn content")
        
        with st.expander("ℹ️ How to use", expanded=False):
            st.markdown("""
            1. **Select a Topic**: Choose from our curated list of professional topics
            2. **Choose Length**: Pick short, medium, or long format
            3. **Select Language**: Choose between English or Hinglish
            4. **Generate**: Click the generate button and wait for your post
            """)
        
        st.divider()
        
        try:
            fs = FewShotPosts()
            tags = fs.get_tags()
        except Exception as e:
            st.error("Failed to load topics. Please try again later.")
            return

        with st.form("post_generator_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_tag = st.selectbox("🏷️ Topic", options=tags)
            with col2:
                selected_length = st.selectbox("📏 Length", options=length_options)
            with col3:
                selected_language = st.selectbox("🌐 Language", options=language_options)
            
            generate_button = st.form_submit_button("✨ Generate Post")
        
        if generate_button:
            try:
                with st.spinner("🎯 Crafting your perfect post..."):
                    post = generate_post(selected_length, selected_language, selected_tag)
                
                st.success("✨ Your post is ready!")
                
                with st.container():
                    st.markdown("### 📝 Generated Post")
                    display_post(post)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy to Clipboard"):
                            handle_copy(post)
                    with col2:
                        st.download_button(
                            label="📥 Download Post",
                            data=post,
                            file_name="linkedin_post.txt",
                            mime="text/plain"
                        )
            except Exception as e:
                st.error(f"Failed to generate post. Please try again. Error: {str(e)}")
        
        st.divider()
        

if __name__ == "__main__":
    main()
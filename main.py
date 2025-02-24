import os
import streamlit as st
from PIL import Image
# import pytesseract
from openai import OpenAI

# Optional: Configure Streamlit page
st.set_page_config(
    page_title="Drained Brains",
    layout="centered"
)

# Load your OpenAI key securely (Render, local env, etc.)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# --- Logo ---
logo_url = '''<svg width="43" height="41" viewBox="0 0 43 41" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M23.8287 8.94266C22.4425 8.94266 21.0699 9.21493 19.7892 9.74393C18.5086 10.2729 17.3449 11.0483 16.3648 12.0257C15.3846 13.0032 14.6071 14.1636 14.0766 15.4407C13.7048 16.3358 13.4595 17.276 13.346 18.2342C13.2568 18.9873 12.8442 19.6828 12.1656 20.0212L10.1584 21.022C9.47979 21.3604 9.03456 22.0559 9.12376 22.809C9.23726 23.7673 9.48259 24.7074 9.85438 25.6025C10.3849 26.8796 11.1624 28.04 12.1425 29.0175C13.1227 29.9949 14.2864 30.7703 15.567 31.2993C16.8477 31.8283 18.2203 32.1006 19.6064 32.1006C20.9926 32.1006 22.3652 31.8283 23.6459 31.2993C24.9265 30.7703 26.0902 29.9949 27.0704 29.0175C28.0505 28.04 28.828 26.8796 29.3585 25.6025C29.7303 24.7074 29.9756 23.7673 30.0891 22.809C30.1783 22.0559 30.5909 21.3604 31.2696 21.022L33.2767 20.0212C33.9553 19.6828 34.4006 18.9873 34.3114 18.2342C34.1979 17.276 33.9525 16.3358 33.5807 15.4407C33.0503 14.1636 32.2727 13.0032 31.2926 12.0257C30.3124 11.0483 29.1488 10.2729 27.8681 9.74393C26.5874 9.21493 25.2148 8.94266 23.8287 8.94266ZM28.7047 17.4549C28.8111 17.711 28.8968 17.9745 28.9612 18.2428C29.1384 18.9802 28.6775 19.6828 27.9989 20.0212L25.9918 21.022C25.3131 21.3604 24.9161 22.063 24.739 22.8004C24.6745 23.0688 24.5889 23.3322 24.4825 23.5884C24.2172 24.2269 23.8285 24.8071 23.3384 25.2959C22.8483 25.7846 22.2665 26.1723 21.6262 26.4368C20.9858 26.7013 20.2995 26.8374 19.6064 26.8374C18.9134 26.8374 18.2271 26.7013 17.5867 26.4368C16.9464 26.1723 16.3646 25.7846 15.8745 25.2959C15.3844 24.8071 14.9956 24.2269 14.7304 23.5884C14.624 23.3322 14.5384 23.0688 14.4739 22.8004C14.2968 22.063 14.7576 21.3604 15.4362 21.022L17.4433 20.0212C18.122 19.6828 18.519 18.9802 18.6961 18.2428C18.7606 17.9745 18.8463 17.711 18.9526 17.4549C19.2179 16.8163 19.6066 16.2361 20.0967 15.7474C20.5868 15.2586 21.1686 14.871 21.8089 14.6065C22.4493 14.342 23.1356 14.2058 23.8287 14.2058C24.5218 14.2058 25.2081 14.342 25.8484 14.6065C26.4887 14.871 27.0705 15.2586 27.5606 15.7474C28.0507 16.2361 28.4395 16.8163 28.7047 17.4549Z" fill="#E22935"></path>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M23.8287 0.521606C21.3336 0.521606 18.8629 1.01169 16.5577 1.96389C14.2525 2.91608 12.158 4.31174 10.3936 6.07116C8.62933 7.83059 7.2298 9.91933 6.27496 12.2181C5.47865 14.1352 5.00464 16.1672 4.86918 18.2322C4.81955 18.989 4.39977 19.6828 3.72111 20.0212L1.714 21.022C1.03534 21.3604 0.597326 22.0543 0.646962 22.811C0.782417 24.8761 1.25643 26.908 2.05273 28.8251C3.00757 31.1239 4.4071 33.2126 6.17142 34.9721C7.93573 36.7315 10.0303 38.1271 12.3355 39.0793C14.6406 40.0315 17.1113 40.5216 19.6064 40.5216C22.1016 40.5216 24.5722 40.0315 26.8774 39.0793C29.1826 38.1271 31.2772 36.7315 33.0415 34.9721C34.8058 33.2126 36.2053 31.1239 37.1602 28.8251C37.9565 26.908 38.4305 24.8761 38.5659 22.811C38.6156 22.0543 39.0353 21.3604 39.714 21.022L41.7211 20.0212C42.3998 19.6828 42.8378 18.989 42.7882 18.2322C42.6527 16.1672 42.1787 14.1352 41.3824 12.2181C40.4275 9.91933 39.028 7.83059 37.2637 6.07116C35.4994 4.31174 33.4048 2.91608 31.0997 1.96389C28.7945 1.01169 26.3238 0.521606 23.8287 0.521606ZM33.2726 22.8102C33.3413 22.0549 33.7576 21.3604 34.4362 21.022L36.4433 20.0212C37.122 19.6828 37.5635 18.9883 37.4948 18.2331C37.3699 16.8597 37.0373 15.5106 36.5064 14.2323C35.8167 12.572 34.806 11.0635 33.5317 9.79278C32.2575 8.52208 30.7448 7.51411 29.0799 6.82641C27.4151 6.13872 25.6307 5.78476 23.8287 5.78476C22.0266 5.78476 20.2423 6.13872 18.5774 6.82641C16.9125 7.51411 15.3998 8.52208 14.1256 9.79278C12.8514 11.0635 11.8406 12.572 11.151 14.2323C10.62 15.5106 10.2874 16.8597 10.1625 18.2331C10.0938 18.9883 9.67755 19.6828 8.99889 20.0212L6.99178 21.022C6.31312 21.3604 5.87162 22.0549 5.9403 22.8102C6.0652 24.1835 6.39777 25.5326 6.92876 26.811C7.61837 28.4712 8.62914 29.9797 9.90337 31.2504C11.1776 32.5211 12.6903 33.5291 14.3552 34.2168C16.02 34.9045 17.8044 35.2584 19.6064 35.2584C21.4085 35.2584 23.1929 34.9045 24.8577 34.2168C26.5226 33.5291 28.0353 32.5211 29.3095 31.2504C30.5838 29.9797 31.5945 28.4712 32.2841 26.811C32.8151 25.5326 33.1477 24.1835 33.2726 22.8102Z" fill="#E22935"></path>
            <path d="M42.8234 19.0401H37.5437C37.5414 19.3092 37.3834 19.5526 37.1408 19.6735L33.739 21.3697C33.4965 21.4906 33.3417 21.734 33.3227 22.0031H38.6023C38.619 21.7339 38.7743 21.4906 39.0168 21.3697L42.4186 19.6735C42.6611 19.5526 42.8187 19.3093 42.8234 19.0401Z" fill="#FF6670"></path>
            <path d="M0.612061 22.0031H5.89171C5.89403 21.734 6.05205 21.4906 6.29459 21.3697L9.6964 19.6735C9.93894 19.5526 10.0937 19.3092 10.1128 19.0401H4.83311C4.81639 19.3093 4.66115 19.5526 4.41862 19.6735L1.01681 21.3697C0.774281 21.4906 0.616707 21.7339 0.612061 22.0031Z" fill="#FF6670"></path>
            <path d="M13.2815 19.0401C13.2599 19.3092 13.1056 19.5526 12.8631 19.6735L9.46126 21.3697C9.2187 21.4906 9.06019 21.7341 9.0604 22.0031H14.347C14.3357 21.7346 14.4964 21.4907 14.739 21.3697L18.1408 19.6735C18.3835 19.5525 18.5358 19.3086 18.568 19.0401H13.2815Z" fill="#FF6670"></path>
            <path d="M29.0885 19.0401C29.0997 19.3086 28.9391 19.5525 28.6964 19.6735L25.2946 21.3697C25.0519 21.4907 24.8997 21.7346 24.8674 22.0031H30.154C30.1755 21.7341 30.3298 21.4906 30.5724 21.3697L33.9742 19.6735C34.2167 19.5526 34.3752 19.3092 34.375 19.0401H29.0885Z" fill="#FF6670"></path>
            </svg>'''
st.logo(logo_url, icon_image=logo_url)

# --- TOP SECTION: TITLE, INTRO, QUICK LINKS ---
st.markdown("<h1 style='text-align: center;'>🌏 Drained Brains 🛫</h1><br><br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("⚓ Together for better care of our elders back home 👵🏼👴🏼")
    # st.caption("_italics_ :green[Care]")
    st.caption("_Join to understand and manage mental healthcare for elders living away back home_")
    st.session_state.show_newsletter_form = False

    if st.button("Subscribe to our Newsletter", type="primary"):
        st.session_state.show_newsletter_form = True
   
with col2:    
    col2a, col2b = st.columns(2)
    with col2b:
        st.caption(" \n\n Check out the :green[Toolkit] :sunglasses:")
        # st.link_button("Community", "https://www.reddit.com/r/drainedbrains/", icon="👩🏼‍❤️‍👨🏻", type="secondary", disabled=False, use_container_width=True)
        st.link_button("Meds Check", "#prescription-explainer", icon="🔍", type="secondary", disabled=False, use_container_width=True)
        st.link_button("SOS bot", "#sos-chat", icon="🆘", type="secondary", disabled=False, use_container_width=True)
        st.link_button("Resources", "#resources", icon="📚", type="secondary", disabled=False, use_container_width=True)
        st.link_button("Practitioners", "#doctors-directory", icon="👩🏻‍⚕️", type="secondary", disabled=False, use_container_width=True)


# -------------------------------------------------------
# FUNCTION: Renders the Newsletter Form
# -------------------------------------------------------

@st.dialog(" ")
def render_newsletter_form():

    st.markdown("Hello 👋, Subscribe to us for Reliable information")
    substack_html = """<iframe src="https://drainedbrains.substack.com/embed" width=100% height="320" style="border:1px solid #EEE; background:white;" frameborder="0" scrolling="no"></iframe>"""
    st.markdown(substack_html, unsafe_allow_html=True)

st.write("---")

if st.session_state.show_newsletter_form:
    render_newsletter_form()

# --- PRESCRIPTION CHECKER SECTION ---
st.subheader("Prescription Explainer")
st.caption("This is a simple tool to understand a :green[Mental health medical prescription]. Summarize your symptoms and enter exact prescription (with dosage) in details:")

st.caption("_example: Escitalopram 10mg 1-0-0, Panto 1 40 mg 1-0-0, Ibuprofen 400mg SOS._\n"
            " _symptoms of restlessness, mood swings and dietary issues_")

prescription_text = st.text_area("Prescription Text (please mask personal details):")
uploaded_image = st.file_uploader(
    "Optional: Upload prescription image (crop out names)",
    type=["jpg", "jpeg", "png", "HEIC", "heic"]
)

if st.button("Submit"):
    # (1) Extract text from image if provided
    
    if uploaded_image:
        try:
            image = Image.open(uploaded_image)
            prescription_scan = pytesseract.image_to_string(image)
            st.write(f"**Extracted Prescription From image:{prescription_scan}")
        except Exception as e:
            prescription_scan = ""
            st.write(f"Error calling the Image API: {e}") 
    
    else:
        prescription_scan = ""

    # (2) Build your prompt
    prompt = (
        f"Prescription:\n{prescription_text}\n\n"
        f"Prescription reference read from image (unreliable):\n{prescription_scan}"
    )

    # (3) Call your LLM
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert mental health practitioner that checks if a prescription for Geriatric mental health makes sense with. make sure to respond succinctly and only about the prescriptions as follows: (1. Report if there is a fault in prescription, any critical issues like medicines on wrong time, too much quantity or incompatible with symptoms if provided. (2. Report if there is an addiction causing medicine or major side effects causing drug. (3. Report if image or text is unreadable and ask for text input if not clear"},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",
        )

        result = chat_completion.choices[0].message.content.strip()

        st.write("Results:")
        st.write(result)

    except Exception as e:
        st.error(f"Error calling the AI API: {e}")

st.caption("Disclaimer: _This tool is designed strictly as an :red[emergency guide] for individuals navigating a :red[mental health medical emergency], whether for themselves or a family member. It offers preliminary guidance based on self-reported symptoms, medical history, and prescription details (including dosage). It is not intended to replace professional medical advice, diagnosis, or treatment. Use this tool responsibly and do not rely solely on its output for critical decisions. Please ensure that you do not share any personal identifiable information. Always seek immediate help from qualified healthcare professionals in case of a medical emergency. Your safety and confidentiality remain paramount. Be cautious._")

st.write("---")


# --- SOS Section ---

st.subheader("SOS Chat")
st.caption("This is a strictly emergency tool to guide the user navigate under a :green[Mental health medical emergency] with self or family. Summarize your symptoms and enter applicable history with prescriptions (with dosage) in details: :red[(Do not share personal identifiable information)]")

st.caption("_example: Elder having severe psychosis. what to do?_\n"
            " _Latest prescription: Escitalopram 10mg 1-0-0, Panto 1 40 mg 1-0-0_")


messages = st.container(height=300)
chat_input_box = st.container()

with chat_input_box:
    if prompt := st.chat_input("How can i help ?"):
        messages.chat_message("user").write(prompt)

        # (3) Call your LLM
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert mental health practitioner that guides the user to medical helpline using following info: helpline number : 100. "},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4o",
            )

            result = chat_completion.choices[0].message.content.strip()
            messages.chat_message("assistant").write(f"{result}")

        except Exception as e:
            st.error(f"Error calling the AI API: {e}")

st.caption("Disclaimer: _This tool is designed strictly as an :red[emergency guide] for individuals navigating a :red[mental health medical emergency], whether for themselves or a family member. It offers preliminary guidance based on self-reported symptoms, medical history, and prescription details (including dosage). It is not intended to replace professional medical advice, diagnosis, or treatment. Use this tool responsibly and do not rely solely on its output for critical decisions. Please ensure that you do not share any personal identifiable information. Always seek immediate help from qualified healthcare professionals in case of a medical emergency. Your safety and confidentiality remain paramount. Be cautious._")

st.write("---")

# --- DIRECTORIES & RESOURCES ---


col1_directory, col2_directory = st.columns(2)
with col1_directory:
    st.header("👩🏻‍⚕️")
    st.subheader("Doctors Directory")

with col2_directory:
    st.link_button("iCALL crowdsourced list of Mental Health Professionals We Can Trust (23rd April 2021)", "https://docs.google.com/spreadsheets/u/2/d/1pzckT6ns2H1IlmwYwJa8EnBh_1u3gRA9cEOoA4zfilc/htmlview#", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("iCALL Helpline", "https://icallhelpline.org/", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("Therapists listing", "https://themindclan.com/professionals/", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("IACP directory", "https://iacp.in/wp-content/uploads/2022/01/directory.pdf", icon=None, type="secondary", disabled=False, use_container_width=True)
st.write("---")

col1_resources, col2_resources = st.columns(2)
with col1_resources:
    st.header("📚")
    st.subheader("Resources")

with col2_resources:
    st.link_button("Essential elder care checklist", "https://www.talkspace.com/blog/aging-parents-checklist/", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("Mental Health First Aid Guidelines", "https://mhfainternational.org/guidelines/", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("strategies to support parents mental-health for NRIs", "https://www.nilacares.com/blogs/6-effective-strategies-for-nri-children-to-support-their-parents-mental-health-in-india", icon=None, type="secondary", disabled=False, use_container_width=True)
    st.link_button("Know your medical prescription", "https://www.1mg.com/articles/know-your-medical-prescription/?srsltid=AfmBOopqxCbk5Kph2oWEQfnQvSvAwuZSTpOzHJ-MPBspQr9JhQ6J59b8", icon=None, type="secondary", disabled=False, use_container_width=True)
st.write("---")

# --- ABOUT SECTION ---
st.subheader("About Us")
st.write(
    "I’ve always had a personal connection to mental health. Growing up, I experienced firsthand the impact of mental illness when my mother, a respected teacher, suffered a sudden attack amid old-school politics. I was in class 10 during my boards, and that long night rushing to the hospital changed everything. In the years that followed, I learned how mental illness can change a person, even when it starts with something as simple as an unexpected health scare.\n"
    "\n"
    "I went on to study engineering and then Data, spending over a decade in the field of products, strategy, and business. But my journey through user behaviour and data science led me to understanding psychology and mental health. Through the ups and downs of life, I have witnessed the challenges many older adults face. I’ve seen parents struggling with mental health disorders, dealing with confusing prescriptions, mixed medications, and new issues brought on by modern life: screen addiction, loneliness, depression, post-retirement challenges, and even the risks of scams.\n"
    "\n"
    "This initiative is my simple effort to help adults take care of their parents’ mental health. I understand how important it is to have accessible and reliable support, especially when finding the right doctor or getting a second opinion feels overwhelming. That’s why I have put together a toolkit that includes easy-to-use tools like a prescription explainer and an SOS chat for moments of crisis, along with practical checklists for daily care routines.\n"
    "\n"
    "Whether you’re balancing a career while caring for aging parents or supporting them from afar as living abroad- Join me in creating a community to learn from experiences, and find trusted help. Subscribe to our monthly newsletter for updates and helpful tips. Together, we can look after the mental health of our loved ones—because caring for our parents is something we all share ❤️."
)
st.write("---")

# --- SOCIAL ICONS / LINKS ---
st.subheader("Connect with us:")

substack_html = """<iframe src="https://drainedbrains.substack.com/embed" width=100% height="320" style="border:1px solid #EEE; background:white;" frameborder="0" scrolling="no"></iframe>"""
st.markdown(substack_html, unsafe_allow_html=True)
st.write("\n ")
st.write("\n ")
st.write(" \n\n Scan to stay connected with :blue[with our community] :sunglasses:")

col_substack_2, col_insta = st.columns(2)
with col_substack_2:
    st.link_button("Blog and Newsletter", "https://drainedbrains.substack.com/", icon="📣", type="secondary", disabled=False, use_container_width=True)
    st.image("directory/sub_qrcode.svg", width=None, use_container_width=True)

with col_insta:
    st.link_button("Instagram", "https://www.instagram.com/unsubscription.society/?hl=en", icon="🎭", type="secondary", disabled=False, use_container_width=True)
    st.image("directory/download.png", width=None, use_container_width=True)

# --- FOOTER LINKS ---
st.write("---")
st.link_button("Contact me", "mailto:vashist.anupam@gmail.com", icon="📩", type="secondary", disabled=False, use_container_width=False)
st.link_button("Disclaimer and TC", "https://drainedbrains.substack.com/p/terms-of-usage", icon="⁉️", type="secondary", disabled=False, use_container_width=False)

import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pandass Cover Generator", page_icon="🎸", layout="wide")

# --- CUSTOM CSS BIAR UI LEBIH BADASS ---
st.markdown("""
<style>
    /* Ubah font judul utama */
    h1 {
        font-family: 'Arial Black', sans-serif;
        color: #ff2a2a !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    /* Tombol Gaskeun biar nyala dan garang */
    .stButton>button {
        background: linear-gradient(90deg, #b30000 0%, #ff1a1a 100%);
        color: white !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        border: 2px solid #ff4d4d;
        border-radius: 8px;
        box-shadow: 0px 4px 15px rgba(255, 26, 26, 0.5);
        transition: 0.3s;
        padding: 15px !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(255, 26, 26, 0.8);
        border-color: #ffb3b3;
    }
    /* Border untuk area input biar tegas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 1px solid #ff4d4d !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI HEADER ---
st.title("🔥 PANDASS LYRIC ENGINE")
st.markdown("**Ubah lirik lagu apapun jadi aransemen Pop-Punk / Moshpit bertenaga! 🤘**")
st.markdown("---")

# --- LAYOUT DIBAGI 2 KOLOM (KIRI INPUT, KANAN SETTING) ---
col_main, col_settings = st.columns([1.5, 1])

with col_main:
    # INPUT DIGABUNG SESUAI REQUEST
    song_info = st.text_input("🎸 Judul Lagu & Nama Artis Asli", placeholder="Contoh: Dirimu yang Dulu - Anggis Devaki")
    original_lyrics = st.text_area("📜 Lirik Original", height=350, placeholder="Paste lirik lengkap di sini...\n\n[Verse 1]\n...")

with col_settings:
    st.markdown("### ⚙️ Cover Settings")
    with st.container(border=True):
        cover_style = st.selectbox("🎛️ Cover Style", ["Heavy Modern Pop Punk", "Powerful Epic Orchestral", "Cinematic Rock", "Original Genre", "Custom"])
        
        # LOGIKA CUSTOM STYLE YANG UDAH DIBENERIN
        if cover_style == "Custom":
            final_style = st.text_input("🔥 Tulis Genre Lu di sini:", placeholder="Contoh: Nu Metal ala Linkin Park")
        else:
            final_style = cover_style
            
        st.markdown("**Vocal & Vibe:**")
        female_vocal = st.checkbox("👩‍🎤 Female Lead Vocal Only", value=True)
        high_bpm = st.checkbox("🥁 High BPM 160–190", value=True)
        emotional_energy = st.checkbox("🔥 Emotional & Moshpit Energy", value=True)
        
        st.markdown("**AI Pronunciation:**")
        indo_chunking = st.checkbox("🗣️ Indo Pronunciation Chunking (-)", value=True, help="Biar nyanyi bahasa Indonesia natural (misal: seba-gai)")

# --- LOGIKA MESIN PROMPT AI ---
def generate_cover(api_key, song_data, lyrics, style):
    genai.configure(api_key=api_key)
    
    system_prompt = """
    You are Pandass Cover Generator. Your job is to transform user-provided song lyrics into a singable cover adaptation.
    
    CORE PRIORITIES:
    1. Preserve the original meaning and structure.
    2. Match original rhythmic phrasing.
    
    INDONESIAN PRONUNCIATION CHUNKING:
    When hyphen mode is enabled, "-" is a pronunciation guide. (e.g., CORRECT: seba-gai, mera-sakan, melin-dungi). Keep the "e" sound connected to the correct pronunciation chunk.
    
    OUTPUT EXACTLY 8 SECTIONS. Separate each section strictly with this exact delimiter: ===SECTION_DIVIDER===
    Do not add extra text before the first delimiter or after the last one.
    
    Format required:
    ===SECTION_DIVIDER===
    [Section 1: YouTube Title & Full SEO Caption following the Pandass template. Include "Bebas pakai untuk backsound..." etc.]
    ===SECTION_DIVIDER===
    [Section 2: TikTok Caption following the Pandass template: "Mana suaranya yang..."]
    ===SECTION_DIVIDER===
    [Section 3: English Lyric Adaptation (Homophone style)]
    ===SECTION_DIVIDER===
    [Section 4: Indonesian Lyric Adaptation (Chunking style with "-")]
    ===SECTION_DIVIDER===
    [Section 5: Audio AI Style Prompt (Keep Heavy Pop Punk presets)]
    ===SECTION_DIVIDER===
    [Section 6: Excluded Style]
    ===SECTION_DIVIDER===
    [Section 7: YouTube Thumbnail AI Prompt (Y2K / vintage pop-rock nostalgic style duo band. DO NOT use the word Pandass in the image text)]
    ===SECTION_DIVIDER===
    [Section 8: Omniflash Video Prompts (3 Beats for NPC encounter & 3 Beats for Garage Performance using the PANDASS character reference sheet rules)]
    """

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=system_prompt
        )
        user_prompt = f"Lagu dan Penyanyi Asli: {song_data}\nStyle Cover: {style}\nLirik Original:\n{lyrics}"
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return str(e)

# --- TOMBOL EKSEKUSI ---
st.markdown("<br>", unsafe_allow_html=True) # Spasi dikit
if st.button("🔥 GASKEUN", use_container_width=True):
    if not song_info or not original_lyrics:
        st.warning("⚠️ Woi bro, isi Judul/Artis sama Liriknya dulu!")
    else:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            st.error("⚠️ API Key Gemini belum dipasang di Streamlit Secrets!")
        else:
            with st.spinner("Pandass lagi nyetem gitar dan masak aransemen maut... 🎸🔥"):
                result = generate_cover(api_key, song_info, original_lyrics, final_style)
                
                sections = [s.strip() for s in result.split("===SECTION_DIVIDER===") if s.strip()]
                
                if len(sections) >= 8:
                    st.success("✅ ARANSEMEN JADI, SIAP MOSHPIT!")
                    
                    # BIAR TAB-NYA KELIATAN RAPI
                    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                        "🎬 YT SEO", "📱 TikTok", "🇬🇧 Eng Lirik", "🇮🇩 Indo Lirik", 
                        "🎸 Style", "🚫 Excluded", "🖼️ Thumbnail", "🎥 Video AI"
                    ])
                    
                    tabs = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]
                    for i in range(8):
                        with tabs[i]:
                            st.code(sections[i], language="markdown")
                else:
                    st.error("Waduh, format AI agak meleset nih. Coba klik GASKEUN lagi bro.")
                    st.write("Raw Output:", result)

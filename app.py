import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pandass Cover Generator", page_icon="🎸", layout="wide")

# --- CUSTOM CSS BIAR UI LEBIH BADASS ---
st.markdown("""
<style>
    h1 {
        font-family: 'Arial Black', sans-serif;
        color: #ff2a2a !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
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
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 1px solid #ff4d4d !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI HEADER ---
st.title("🔥 PANDASS LYRIC ENGINE")
st.markdown("**Ubah lirik lagu apapun jadi aransemen Pop-Punk / Moshpit bertenaga! 🤘**")
st.markdown("---")

# --- LAYOUT DIBAGI 2 KOLOM ---
col_main, col_settings = st.columns([1.5, 1])

with col_main:
    song_info = st.text_input("🎸 Judul Lagu & Nama Artis Asli", placeholder="Contoh: Dirimu yang Dulu - Anggis Devaki")
    original_lyrics = st.text_area("📜 Lirik Original", height=350, placeholder="Paste lirik lengkap di sini...\n\n[Verse 1]\n...")

with col_settings:
    st.markdown("### ⚙️ Cover Settings")
    with st.container(border=True):
        cover_style = st.selectbox("🎛️ Cover Style", ["Heavy Modern Pop Punk", "Powerful Epic Orchestral", "Cinematic Rock", "Original Genre", "Custom"])
        
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

# --- LOGIKA MESIN PROMPT AI (ANTI-GAGAL) ---
def generate_cover(api_key, song_data, lyrics, style):
    genai.configure(api_key=api_key)
    
    system_prompt = """
    You are Pandass Cover Generator. Your job is to transform user-provided song lyrics into a singable cover adaptation.
    
    CRITICAL INSTRUCTION: You MUST output EXACTLY 8 sections. 
    Separate each section using EXACTLY this string: ===SECTION_DIVIDER===
    Do NOT write any intro or outro text. Start immediately with the first section.
    
    Format Required:
    [Section 1: YouTube Title & Full SEO Caption following Pandass template]
    ===SECTION_DIVIDER===
    [Section 2: TikTok Caption]
    ===SECTION_DIVIDER===
    [Section 3: English Lyric Adaptation (Homophone style)]
    ===SECTION_DIVIDER===
    [Section 4: Indonesian Lyric Adaptation (Chunking style with "-" e.g., seba-gai)]
    ===SECTION_DIVIDER===
    [Section 5: Audio AI Style Prompt]
    ===SECTION_DIVIDER===
    [Section 6: Excluded Style]
    ===SECTION_DIVIDER===
    [Section 7: YouTube Thumbnail AI Prompt]
    ===SECTION_DIVIDER===
    [Section 8: Omniflash Video Prompts]
    """

    try:
        # PAKE MESIN FLASH BIAR NGEBUT DAN GRATIS
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )
        user_prompt = f"Lagu dan Penyanyi Asli: {song_data}\nStyle Cover: {style}\nLirik Original:\n{lyrics}"
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- TOMBOL EKSEKUSI ---
st.markdown("<br>", unsafe_allow_html=True)
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
                
                if result.startswith("ERROR:"):
                    st.error(f"Gagal konek ke Google AI: {result}")
                else:
                    # Bersihkan hasil split biar aman
                    raw_sections = result.split("===SECTION_DIVIDER===")
                    sections = [s.strip() for s in raw_sections if s.strip()]
                    
                    if len(sections) >= 8:
                        st.success("✅ ARANSEMEN JADI, SIAP MOSHPIT!")
                        
                        tab_titles = ["🎬 YT SEO", "📱 TikTok", "🇬🇧 Eng Lirik", "🇮🇩 Indo Lirik", "🎸 Style", "🚫 Excluded", "🖼️ Thumbnail", "🎥 Video AI"]
                        tabs = st.tabs(tab_titles)
                        
                        for i in range(8):
                            with tabs[i]:
                                st.code(sections[i], language="markdown")
                    else:
                        st.warning("⚠️ Hasilnya berhasil dibikin, tapi pembagian tab-nya agak meleset dikit dari AI-nya. Ini Full Output-nya:")
                        st.code(result, language="markdown")

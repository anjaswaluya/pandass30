import streamlit as st
import anthropic

st.set_page_config(page_title="Pandass Cover Generator", page_icon="🐼", layout="wide")

st.title("🔥 PANDASS COVER GENERATOR")
st.markdown("Ubah lirik lagu jadi aransemen pop-punk moshpit bertenaga (Full 8 Output)!")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        song_title = st.text_input("Judul Lagu (Contoh: Dirimu yang Dulu)")
    with col2:
        original_artist = st.text_input("Penyanyi Asli (Contoh: Anggis Devaki)")
    
    original_lyrics = st.text_area("Lirik Original", height=200, placeholder="Paste lirik lengkap di sini...")

st.subheader("⚙️ Cover Settings")
col3, col4 = st.columns(2)
with col3:
    cover_style = st.selectbox("Cover Style", ["Heavy Modern Pop Punk", "Powerful Epic Orchestral", "Cinematic Rock", "Original Genre", "Custom"])
    female_vocal = st.checkbox("Female Lead Vocal Only", value=True)
    high_bpm = st.checkbox("High BPM 160–190", value=True)
with col4:
    indo_chunking = st.checkbox("Gunakan Indonesian Pronunciation Chunking (-)", value=True)
    emotional_energy = st.checkbox("Emotional Vocals & Moshpit Energy", value=True)

def generate_cover(api_key, title, artist, lyrics, style):
    client = anthropic.Anthropic(api_key=api_key)
    
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

    user_prompt = f"Lagu: {title}\nPenyanyi: {artist}\nStyle: {style}\nLirik:\n{lyrics}"

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return str(e)

if st.button("🔥 GASKEUN", use_container_width=True, type="primary"):
    if not song_title or not original_artist or not original_lyrics:
        st.warning("⚠️ Isi Judul, Penyanyi, dan Lirik dulu bro!")
    else:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            st.error("⚠️ API Key Anthropic belum di-setting di Streamlit Secrets!")
        else:
            with st.spinner("Pandass lagi masak aransemen maut... Tunggu bentar bro! 🎸"):
                result = generate_cover(api_key, song_title, original_artist, original_lyrics, cover_style)
                
                sections = [s.strip() for s in result.split("===SECTION_DIVIDER===") if s.strip()]
                
                if len(sections) >= 8:
                    st.success("✅ Selesai di-generate!")
                    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                        "🎬 YT SEO", "📱 TikTok", "🇬🇧 English Lirik", "🇮🇩 Indo Lirik", 
                        "🎸 Style", "🚫 Excluded", "🖼️ Thumbnail", "🎥 Video Beats"
                    ])
                    
                    tabs = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]
                    for i in range(8):
                        with tabs[i]:
                            st.code(sections[i], language="markdown")
                else:
                    st.error(f"Waduh, format balasan AI kurang pas. Coba klik GASKEUN lagi.")
                    st.write("Raw Output:")
                    st.write(result)

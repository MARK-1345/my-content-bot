import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ===========================================
# ⚙️ CONFIG
# ===========================================
st.set_page_config(
    page_title="🎬 ปั้นคอนเทนต์พรรคพวก",
    page_icon="🎬",
    layout="wide"
)

PASSWORD_SECRET = "sawatdeepeechai555"
MODEL_NAME = "gemini-2.5-flash-lite"  # ฟรี 1,000 requests/วัน

# ===========================================
# 🔐 1. ระบบรหัสผ่าน + ชื่อเล่น
# ===========================================
st.sidebar.title("🔐 ด่านตรวจพรรคพวก")

user_password = st.sidebar.text_input("กรอกรหัสลับ:", type="password")
nickname = st.sidebar.text_input("ชื่อเล่นของคุณ:", placeholder="เช่น เอ, บี, ปุ๋ย")

if user_password != PASSWORD_SECRET:
    if user_password:
        st.sidebar.error("รหัสไม่ถูกนะเสี่ย ไปถามพรรคพวกมาใหม่!")
    st.title("🚧 พื้นที่ส่วนบุคคล")
    st.info("กรุณากรอกรหัสลับและชื่อเล่นที่แถบด้านข้าง เพื่อเปิดใช้งานระบบครับ")
    st.stop()

if not nickname:
    st.warning("⚠️ กรุณากรอกชื่อเล่นที่แถบด้านข้างก่อน เพื่อแยกบทของคุณกับคนอื่น")
    st.stop()

# ===========================================
# 🤖 2. ตั้งค่า Gemini API
# ===========================================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]  # ใช้ตอน deploy บน Streamlit Cloud
except:
    api_key = "AIzaSyCBia1yk71nHVsh7KgI3GfA2zaIolsZ7PI"  # ใช้ตอนรันในเครื่อง

if not api_key or api_key == "PUT_YOUR_GEMINI_API_KEY_HERE":
    st.error("❌ ยังไม่ได้ตั้งค่า GEMINI API KEY")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(MODEL_NAME)

# ===========================================
# 💾 3. State สำหรับ History (แยกตามชื่อเล่น)
# ===========================================
if "history" not in st.session_state:
    st.session_state.history = {}

if nickname not in st.session_state.history:
    st.session_state.history[nickname] = []

def add_to_history(feature, input_text, output_text):
    st.session_state.history[nickname].insert(0, {
        "time": datetime.now().strftime("%H:%M"),
        "feature": feature,
        "input": input_text,
        "output": output_text
    })
    st.session_state.history[nickname] = st.session_state.history[nickname][:20]

# ===========================================
# 🤖 ฟังก์ชันเรียก Gemini
# ===========================================
def call_gemini(prompt, system_prompt=None):
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    response = model.generate_content(full_prompt)
    return response.text

# ===========================================
# 🎬 4. UI หลัก
# ===========================================
st.title("🎬 เครื่องมือปั้นคอนเทนต์ (ฉบับพรรคพวก)")
st.caption(f"ยินดีต้อนรับ **{nickname}** 👋")

st.sidebar.divider()
st.sidebar.subheader("🎯 เลือกฟีเจอร์")

feature = st.sidebar.radio(
    "อยากใช้ฟีเจอร์ไหน:",
    [
        "🎬 ปั้น Reel/TikTok (3 เวอร์ชัน)",
        "✏️ เกลาบทเก่า",
        "🚩 Red Flag Checker",
        "📜 History",
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()
brand = st.sidebar.selectbox(
    "เลือกแบรนด์:",
    ["แซ่บซี๊ด", "เป๋าตุง", "เจ็นโฟ", "อื่น ๆ (ระบุเอง)"]
)
if brand == "อื่น ๆ (ระบุเอง)":
    brand = st.sidebar.text_input("ระบุชื่อแบรนด์:", value="แบรนด์ของคุณ")

# ===========================================
# 🎬 ฟีเจอร์ 1: ปั้น Reel/TikTok 3 เวอร์ชัน
# ===========================================
if feature == "🎬 ปั้น Reel/TikTok (3 เวอร์ชัน)":
    st.subheader(f"🎬 ปั้นบท Reel/TikTok ให้แบรนด์: {brand}")

    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox("⏱️ ความยาว:", ["15 วินาที", "30 วินาที", "60 วินาที"])
        hook_style = st.selectbox(
            "🪝 Hook style:",
            ["สะดุดหู กวน ๆ ตลก", "Pain point ตรง ๆ", "เล่าเรื่อง (Storytelling)", "ตัวเลข/สถิติ ช็อก ๆ"]
        )
    with col2:
        tone = st.selectbox(
            "🎙️ โทน:",
            ["กวน ๆ เพื่อนซี้", "จริงจัง น่าเชื่อถือ", "อบอุ่น เข้าใจ", "ดราม่า กระแทกใจ"]
        )
        target = st.text_input("👥 กลุ่มเป้าหมาย:", placeholder="เช่น แม่บ้านวัย 30+")

    user_context = st.text_area(
        "📝 โจทย์/สถานการณ์/สินค้า:",
        placeholder="เช่น ขายครีมหน้าใส ใช้แล้วเด็กลง 5 ปี เน้นรีวิวจากคนใช้จริง",
        height=120
    )

    if st.button("🚀 ปั้นบท 3 เวอร์ชัน!", type="primary"):
        if not user_context:
            st.warning("⚠️ ใส่โจทย์ก่อนนะเสี่ย")
        else:
            system_prompt = """
คุณคือ Creative Copywriter ระดับท็อปของไทย เชี่ยวชาญบท Reel/TikTok โดยเฉพาะ
ตอบเป็นภาษาไทยกันเอง พูดเหมือนพรรคพวกคนสู้ชีวิต
"""
            prompt = f"""
ช่วยปั้นบทวิดีโอสั้น **3 เวอร์ชัน** สำหรับแบรนด์ "{brand}"

**ข้อมูล:**
- โจทย์: {user_context}
- ความยาว: {duration}
- Hook style: {hook_style}
- โทน: {tone}
- กลุ่มเป้าหมาย: {target if target else "คนทั่วไป"}

**กติกา:**
- 3 เวอร์ชัน ต้องมีมุมต่างกันชัดเจน (อย่าซ้ำกัน)
- แต่ละเวอร์ชันมี: ชื่อเรียก (เช่น "เวอร์ชันสายตรง"), Hook 1-2 ประโยคแรก, บทพูดทั้งหมด, CTA ปิด
- บทพูดต้องอ่านแล้วถ่ายได้ทันที ไม่ต้องเดา
- ถ้ามี visual cue สั้น ๆ ให้ใส่ในวงเล็บ เช่น (โชว์สินค้า), (หันกล้องเข้าหน้า)

ใช้ Markdown แบ่งหัวข้อให้ชัด
"""
            with st.spinner("กำลังปั่นบท 3 เวอร์ชัน..."):
                try:
                    result = call_gemini(prompt, system_prompt)
                    st.markdown("### ✨ บทที่ได้:")
                    st.markdown(result)
                    st.success("ปั้นเสร็จแล้วเสี่ย! กดบล็อกข้อความเพื่อก๊อปได้เลย 🚀")
                    add_to_history("Reel 3 เวอร์ชัน", user_context, result)
                except Exception as e:
                    st.error(f"❌ พลาด: {e}")
                    if "429" in str(e):
                        st.info("💡 โควตาวันนี้หมดแล้ว (1,000 requests/วัน) รอวันใหม่นะครับ")

# ===========================================
# ✏️ ฟีเจอร์ 2: เกลาบทเก่า
# ===========================================
elif feature == "✏️ เกลาบทเก่า":
    st.subheader("✏️ เกลาบทเก่าให้คมขึ้น")
    st.caption("วางบทเดิมที่มีอยู่แล้ว → บอกว่าอยากให้ปรับยังไง → AI เกลาให้")

    old_script = st.text_area(
        "📝 บทเดิมของคุณ:",
        placeholder="วางบทเก่ามาตรงนี้เลย...",
        height=200
    )
    feedback = st.text_area(
        "🎯 อยากให้ปรับยังไง:",
        placeholder="เช่น Hook ยังจืด อยากให้แรงขึ้น, ตอนจบอยากให้กระแทกใจกว่านี้, ตัดให้สั้นลง 30%...",
        height=100
    )

    if st.button("✨ เกลาให้หน่อย!", type="primary"):
        if not old_script or not feedback:
            st.warning("⚠️ ใส่ทั้งบทเก่าและคำสั่งปรับนะเสี่ย")
        else:
            system_prompt = "คุณคือ Creative Copywriter ที่เก่งเรื่องการเกลาบทให้ดีขึ้นโดยรักษาแก่นเดิมไว้"
            prompt = f"""
ช่วยเกลาบทนี้ให้ดีขึ้นตามคำสั่ง:

**บทเดิม:**
{old_script}

**ปรับยังไง:**
{feedback}

**ส่งกลับมา:**
1. **บทใหม่** (ปรับแล้ว — เป็นบทพูดล้วนพร้อมถ่าย)
2. **เปลี่ยนอะไรไปบ้าง** (สรุปสั้น ๆ 3-5 ข้อ)
"""
            with st.spinner("กำลังเกลา..."):
                try:
                    result = call_gemini(prompt, system_prompt)
                    st.markdown("### ✨ บทที่เกลาแล้ว:")
                    st.markdown(result)
                    st.success("เกลาเสร็จแล้วครับ!")
                    add_to_history("เกลาบท", old_script[:100] + "...", result)
                except Exception as e:
                    st.error(f"❌ พลาด: {e}")
                    if "429" in str(e):
                        st.info("💡 โควตาวันนี้หมดแล้ว รอวันใหม่นะครับ")

# ===========================================
# 🚩 ฟีเจอร์ 3: Red Flag Checker
# ===========================================
elif feature == "🚩 Red Flag Checker":
    st.subheader("🚩 ตรวจคำเสี่ยง / Red Flags")
    st.caption("วางบท/แคปชัน → เช็กคำที่เสี่ยงผิดกฎหมาย/แพลตฟอร์มแบน → แนะนำคำแทน")

    text_to_check = st.text_area(
        "📝 ข้อความที่จะตรวจ:",
        placeholder="วางบทหรือแคปชันที่จะตรวจตรงนี้...",
        height=200
    )
    industry = st.selectbox(
        "🏷️ ประเภทสินค้า/บริการ:",
        ["ทั่วไป", "อาหารเสริม/สุขภาพ", "เครื่องสำอาง/สกินแคร์", "การเงิน/ลงทุน", "ลดน้ำหนัก", "อื่น ๆ"]
    )

    if st.button("🔍 ตรวจให้หน่อย!", type="primary"):
        if not text_to_check:
            st.warning("⚠️ วางข้อความก่อนนะเสี่ย")
        else:
            system_prompt = """
คุณคือผู้เชี่ยวชาญด้านกฎหมายโฆษณาไทย และนโยบายแพลตฟอร์ม Facebook/TikTok/IG
เก่งเรื่องการหาคำที่เสี่ยงและแนะนำคำแทนที่ปลอดภัยแต่ยังขายได้
"""
            prompt = f"""
ช่วยตรวจข้อความนี้หา **Red Flags** (คำเสี่ยงผิดกฎ อย./กฎหมายโฆษณา/นโยบายแพลตฟอร์ม):

**ประเภทสินค้า:** {industry}

**ข้อความ:**
{text_to_check}

**ส่งกลับมาในรูปแบบ:**

### 🚩 คำเสี่ยงที่เจอ
(ถ้าไม่มี ให้บอกว่า "ไม่พบคำเสี่ยง ปลอดภัยใช้ได้")

| คำ/วลีเสี่ยง | เหตุผล | ระดับเสี่ยง | คำแทนที่แนะนำ |
|---|---|---|---|
| ... | ... | 🔴/🟡/🟢 | ... |

### ✅ เวอร์ชันที่ปลอดภัย
(เขียนข้อความใหม่ทั้งดุ้น โดยแทนคำเสี่ยงด้วยคำที่ปลอดภัยแล้ว)

### 💡 คำแนะนำเพิ่มเติม
(ถ้ามี เช่น ควรใส่ disclaimer อะไร)
"""
            with st.spinner("กำลังตรวจ..."):
                try:
                    result = call_gemini(prompt, system_prompt)
                    st.markdown(result)
                    add_to_history("Red Flag Check", text_to_check[:100] + "...", result)
                except Exception as e:
                    st.error(f"❌ พลาด: {e}")
                    if "429" in str(e):
                        st.info("💡 โควตาวันนี้หมดแล้ว รอวันใหม่นะครับ")

# ===========================================
# 📜 ฟีเจอร์ 4: History
# ===========================================
elif feature == "📜 History":
    st.subheader(f"📜 ประวัติของ {nickname}")

    user_history = st.session_state.history.get(nickname, [])

    if not user_history:
        st.info("ยังไม่มีประวัติ — ลองใช้ฟีเจอร์อื่นก่อนนะ")
    else:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ ล้างประวัติ"):
                st.session_state.history[nickname] = []
                st.rerun()

        st.caption(f"ทั้งหมด {len(user_history)} รายการ (เก็บล่าสุด 20)")

        for i, item in enumerate(user_history):
            with st.expander(f"⏰ {item['time']} — {item['feature']}"):
                st.markdown(f"**Input:** {item['input']}")
                st.markdown("**Output:**")
                st.markdown(item['output'])

# ===========================================
# Footer
# ===========================================
st.sidebar.divider()
st.sidebar.caption(f"👤 ผู้ใช้: **{nickname}**")
st.sidebar.caption(f"🤖 โมเดล: {MODEL_NAME} (ฟรี 1,000/วัน)")

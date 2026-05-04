import streamlit as st
import google.generativeai as genai

# --- 1. ตั้งค่าความปลอดภัย (รหัสลับ) ---
PASSWORD_SECRET = "sawatdeepeechai555" 

# --- 2. ส่วนเช็กรหัสผ่านที่ Sidebar ---
st.sidebar.title("🔐 ด่านตรวจพรรคพวก")
user_password = st.sidebar.text_input("กรอกรหัสลับเพื่อใช้งาน:", type="password")

if user_password != PASSWORD_SECRET:
    if user_password: 
        st.sidebar.error("รหัสไม่ถูกนะเสี่ย ไปถามพรรคพวกมาใหม่!")
    st.title("🚧 พื้นที่ส่วนบุคคล")
    st.info("กรุณากรอกรหัสลับที่แถบด้านข้าง เพื่อเปิดใช้งานระบบปั้นคอนเทนต์ครับ")
    st.stop() 

# --- 3. ถ้าผ่านรหัสมาได้ จะเริ่มทำงานข้างล่างนี้ ---
st.title("🎬 เครื่องมือปั้นคอนเทนต์ 15 วิ (ฉบับพรรคพวก)")
st.success("ยินดีต้อนรับครับเสี่ย! รหัสถูกต้อง ลุยงานต่อได้เลย")

# --- ดึง API KEY และตั้งค่าโมเดล ---
# แนะนำเสี่ย: ถ้าไม่อยากโดนแบนกุญแจ ให้เอา Key ไปใส่ใน Streamlit Secrets ตามที่เคยบอกนะครับ
try:
    API_KEY = st.secrets["AIzaSyAs27sUI4XDy5CybfoizlcvLDnSnlunaWM"]
except:
    API_KEY = "ใส่เลขคีย์จริงของเสี่ยตรงนี้ถ้ายังไม่ได้ตั้ง Secrets" 

genai.configure(api_key=API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# ใช้รุ่น 1.5-flash (ตัวแรงและเสถียรที่สุดตอนนี้ครับเสี่ย)
model = genai.GenerativeModel(
  model_name="gemini-2.5-flash", 
  generation_config=generation_config,
  safety_settings=safety_settings
)

# 2. ส่วน Sidebar สำหรับเลือกแบรนด์
st.sidebar.divider()
brand = st.sidebar.selectbox(
    "เลือกแบรนด์ที่จะโปรโมท:",
    ["แซ่บซี๊ด", "เป๋าตุง", "เจ็นโฟ"]
)

# 3. ส่วนรับโจทย์จากเสี่ย
st.subheader(f"🎬 กำลังปั้นคอนเทนต์ให้แบรนด์: {brand}")
user_context = st.text_area(
    "สไตล์ตัวละคร/สถานการณ์:",
    placeholder="เช่น วิน วิลเลี่ยม พูดหน้ากล้อง, พิมรี่พายรีวิวแบบดุๆ...",
    height=150
)

# 4. ปุ่มกด "สั่งงาน"
if st.button("🚀 ปั้นสคริปต์ให้หน่อยพรรคพวก!"):
    if user_context.strip():
        with st.spinner("พรรคพวกกำลังปั้นบทให้ใจเย็นๆ..."):
            # ใส่กุญแจมือ AI: บังคับเอาแต่บทพูด ไม่เอาน้ำ
            prompt = (
                f"ในฐานะก๊อปปี้ไรเตอร์มือโปร เขียนบทพูดวิดีโอ 15 วินาที ให้แบรนด์ {brand} "
                f"โจทย์คือ: {user_context} "
                "\n\n--- กฎเหล็ก (ห้ามละเมิด) ---"
                "\n1. ตอบกลับมาเฉพาะ 'บทพูด' เท่าที่จะใช้พากย์จริงเท่านั้น"
                "\n2. ห้ามมีวงเล็บอธิบายท่าทาง ห้ามมีชื่อฉาก ห้ามมีมุมกล้อง"
                "\n3. ห้ามมีบทนำ (จัดไปเลยเพื่อน) หรือบทสรุปตอนท้าย"
                "\n4. สำนวนต้อง 'เปิดคมๆ หักมุมตอนจบ' สไตล์พรรคพวก คนสู้ชีวิต"
                "\n5. ความยาวต้องอ่านจบใน 15 วินาที"
                "\n\nเริ่มเขียนบทพูดได้เลย:"
            )
            
            try:
                response = model.generate_content(prompt)
                st.markdown("### ✨ บทที่ได้:")
                st.write(response.text)
                st.success("ปั้นเสร็จแล้วเสี่ย! เอาไปใช้ได้เลย")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("เสี่ยต้องใส่โจทย์ก่อนนะ ไม่งั้น AI ไปไม่ถูก!")

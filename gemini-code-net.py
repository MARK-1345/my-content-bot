import streamlit as st
import google.generativeai as genai

# --- 1. ตั้งค่าความปลอดภัย (รหัสลับ) ---
PASSWORD_SECRET = "sawatdeepeechai555"  # <--- เสี่ยเปลี่ยนเลข 1234 เป็นรหัสที่เสี่ยต้องการได้เลยครับ

# --- 2. ส่วนเช็กรหัสผ่านที่ Sidebar ---
st.sidebar.title("🔐 ด่านตรวจพรรคพวก")
user_password = st.sidebar.text_input("กรอกรหัสลับเพื่อใช้งาน:", type="password")

if user_password != PASSWORD_SECRET:
    if user_password: # ถ้ามีการพิมพ์แต่รหัสผิด
        st.sidebar.error("รหัสไม่ถูกนะเสี่ย ไปถามพรรคพวกมาใหม่!")
    st.title("🚧 พื้นที่ส่วนบุคคล")
    st.info("กรุณากรอกรหัสลับที่แถบด้านข้าง เพื่อเปิดใช้งานระบบปั้นคอนเทนต์ครับ")
    st.stop() # หยุดการทำงานของโค้ดที่เหลือทั้งหมดถ้าไม่ได้รหัสที่ถูกต้อง

# --- 3. ถ้าผ่านรหัสมาได้ จะเริ่มทำงานข้างล่างนี้ ---
# (ส่วนนี้คือโค้ดเดิมของเสี่ยที่เชื่อมกับ Gemini)
st.title("🎬 เครื่องมือปั้นคอนเทนต์ 15 วิ (ฉบับพรรคพวก)")

# ดึง API KEY จาก Streamlit Secrets (แนะนำให้ใช้ตอนเอาขึ้น GitHub)
# หรือถ้าจะเทสในเครื่องเสี่ยก่อน ก็ใส่ genai.configure(api_key="API_KEY_ของเสี่ย")
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["AIzaSyAp8Y6H-9uUsxePJglzUhJTAgOkplWAa1E"])

# --- ส่วนที่ 3: โค้ดส่วนที่เหลือ (ระบบเลือกแบรนด์และปุ่มกด) ---

# 1. ตั้งค่าโมเดล Gemini
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash') # ใช้ตัวแรงตามโปรเจกต์เสี่ย

# 2. ส่วน Sidebar สำหรับเลือกแบรนด์
st.sidebar.divider()
brand = st.sidebar.selectbox(
    "เลือกแบรนด์ที่จะโปรโมท:",
    ["แซ่บซี๊ด", "เป๋าตุง", "เจ็นโฟ"]
)

# 3. ส่วนรับโจทย์จากเสี่ย (Text Area)
st.subheader(f"🎬 กำลังปั้นคอนเทนต์ให้แบรนด์: {brand}")
user_context = st.text_area(
    "สไตล์ตัวละคร/สถานการณ์:",
    placeholder="เช่น วิน วิลเลี่ยม พูดหน้ากล้อง, พิมรี่พายรีวิวแบบดุๆ...",
    height=150
)

# 4. ปุ่มกด "สั่งงาน"
if st.button("🚀 ปั้นสคริปต์ให้หน่อยพรรคพวก!"):
    if user_context:
        with st.spinner("พรรคพวกกำลังปั่นบทให้ใจเย็นๆ..."):
            # สร้างคำสั่งส่งให้ AI
            prompt = f"ช่วยเขียนสคริปต์วิดีโอสั้น 15 วินาที สำหรับแบรนด์ {brand} โดยมีโจทย์คือ: {user_context} ขอเน้นคำพูดสไตล์พรรคพวก คนสู้ชีวิต และมีหักมุมตอนจบ"
            
            response = model.generate_content(prompt)
            
            # แสดงผลลัพธ์
            st.markdown("### ✨ บทที่ได้:")
            st.write(response.text)
            st.success("ปั้นเสร็จแล้วเสี่ย! เอาไปใช้ได้เลย")
    else:
        st.warning("เสี่ยต้องใส่โจทย์ก่อนนะ ไม่งั้น AI ไปไม่ถูก!")
st.success("ยินดีต้อนรับครับเสี่ย! รหัสถูกต้อง ลุยงานต่อได้เลย")

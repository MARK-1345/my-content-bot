import streamlit as st
import google.generativeai as genai

# -------------------------------
# 🔐 1. ระบบรหัสผ่าน
# -------------------------------
PASSWORD_SECRET = "sawatdeepeechai555"

st.sidebar.title("🔐 ด่านตรวจพรรคพวก")
user_password = st.sidebar.text_input("กรอกรหัสลับเพื่อใช้งาน:", type="password")

if user_password != PASSWORD_SECRET:
    if user_password:
        st.sidebar.error("รหัสไม่ถูกนะเสี่ย ไปถามพรรคพวกมาใหม่!")
    st.title("🚧 พื้นที่ส่วนบุคคล")
    st.info("กรุณากรอกรหัสลับที่แถบด้านข้าง เพื่อเปิดใช้งานระบบปั้นคอนเทนต์ครับ")
    st.stop()

# -------------------------------
# 🤖 2. ตั้งค่า Gemini API (แก้ถูก 100%)
# -------------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]  # ใช้ตอน deploy
except:
    api_key = "AIzaSyBbVIhEKf8rfhj4HzGUJZUifGq20zQFMhM"  # ใช้ตอนรันในเครื่อง

if not api_key or api_key == "PUT_YOUR_API_KEY_HERE":
    st.error("❌ ยังไม่ได้ตั้งค่า API KEY")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# 🎬 3. UI หลัก
# -------------------------------
st.title("🎬 เครื่องมือปั้นคอนเทนต์ 15 วิ (ฉบับพรรคพวก)")

st.sidebar.divider()
brand = st.sidebar.selectbox(
    "เลือกแบรนด์ที่จะโปรโมท:",
    ["แซ่บซี๊ด", "เป๋าตุง", "เจ็นโฟ"]
)

st.subheader(f"🎬 กำลังปั้นคอนเทนต์ให้แบรนด์: {brand}")

user_context = st.text_area(
    "สไตล์ตัวละคร/สถานการณ์:",
    placeholder="เช่น วินสายลุย พูดหน้ากล้อง, สายขายตรงพลังสูง...",
    height=150
)

# -------------------------------
# 🚀 4. ปุ่มสร้างคอนเทนต์
# -------------------------------
if st.button("🚀 ปั้นสคริปต์ให้หน่อยพรรคพวก!"):
    if user_context:
        with st.spinner("พรรคพวกกำลังปั่นบทให้ใจเย็นๆ..."):
            prompt = f"""
ช่วยเขียนสคริปต์วิดีโอสั้น 15 วินาที สำหรับแบรนด์ {brand}

เงื่อนไข:
- โจทย์: {user_context}
- สไตล์: พูดแบบพรรคพวก คนสู้ชีวิต
- ภาษา: กันเอง ตรง ๆ
- ต้องมี: hook เปิดแรง + หักมุมตอนจบ

ขอเป็นบทพูดล้วน อ่านแล้วถ่ายได้เลย
"""

            try:
                response = model.generate_content(prompt)

                st.markdown("### ✨ บทที่ได้:")
                st.write(response.text)
                st.success("ปั้นเสร็จแล้วเสี่ย! เอาไปยิงได้เลย 🚀")

            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("⚠️ เสี่ยต้องใส่โจทย์ก่อนนะ ไม่งั้น AI ไปไม่ถูก!")

st.success("✅ ยินดีต้อนรับครับเสี่ย! ระบบพร้อมลุย")

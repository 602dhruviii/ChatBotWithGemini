import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image
import os
import io

# Set your API key directly
API_KEY = "your-api-key"
genai.configure(api_key=API_KEY)

st.image("./Google-Gemini-AI-Logo.png", width=200)
st.write("")

gemini_pro, gemini_vision = st.columns(2)

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def main():
    with gemini_pro:
        st.header("Interact with Gemini Pro")
        st.write("")

        prompt = st.text_input("prompt please...", placeholder="Prompt")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND"):
            response = model.generate_content(prompt)

            st.write("")
            st.header(":blue[Response]")
            st.write("")

            st.markdown(response.text)

    with gemini_vision:
        st.header("Interact with Gemini Pro Vision")
        st.write("")

        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt")
        uploaded_file = st.file_uploader("Choose and Image", accept_multiple_files=False,
                                         type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)

        if st.button("GET RESPONSE"):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts=[
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[Response]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")

if __name__ == "__main__":
    main()

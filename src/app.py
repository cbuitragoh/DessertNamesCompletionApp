import streamlit as st
from .completion_helpers import create_generator
from PIL import Image

st.title(':blue[Dessert names completion app] :ice_cream:')

image = Image.open("./media/dessert.jpg")
st.image(image=image, caption="mango dessert")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    

model_selected = st.selectbox("select model for generate",
                                ("openai-gpt", "text-davinci-002"),
                                index=None,
                                placeholder="Select model..."
                            )

if prompt := st.chat_input(
    placeholder="Welcome a us app! Please type dessert base name to complete",
    max_chars=15
):
    if prompt == None:
        pass
    else:
        try:
            if model_selected == None:
                st.info("Please select a model to continue.")
                st.stop()
            else:
                if model_selected == "openai-gpt":
                    st.info(f"{model_selected} model is provided by HuggingFace :hugging_face:")
                else:
                    st.info(body=f"{model_selected} model is provided by OpenAI :openai:")

            if not openai_api_key and model_selected == "text-davinci-002":
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            with st.spinner("Generating completion..."):   
                final_text = create_generator(prompt=prompt,
                                              seed=42,
                                              model=model_selected,
                                              openai_api_key=openai_api_key
                            )
                st.chat_message("assistant").write(final_text.capitalize())
        except Exception as e:
            st.error(e)


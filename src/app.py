import streamlit as st
import asyncio
from helpers import (create_generator,
                    openAI_models,
                    huggingface_models,
                    generate_dessert_image,
                    show_image,
                    save_tempImage,
                    del_tempImage,
                    load_base_image,
                    normalize_text)

 
# session variable for handling images path
if 'image_path' not in st.session_state:
    st.session_state.image_path = ""

def set_image_path(path):
    st.session_state.image_path = path

def reset_image_path():
    st.session_state.image_path = ""


# session variable for handling generation images in memory
if 'image' not in st.session_state:
    st.session_state.image = "False"
 
def set_image():
    st.session_state.image = "True"

def reset_image():
    st.session_state.image = "False"


# session variable for handling text raw and cleaned as prompt input
if 'final_text' not in st.session_state:
    st.session_state.final_text = ""
 
def set_final_text(text):
    st.session_state.final_text = text


# session variable for handling app stages
if 'stage' not in st.session_state:
    st.session_state.stage = 0
 
def set_stage(stage):
    st.session_state.stage = stage

  
# web page title
st.title(':blue[Dessert Suggestions app] :ice_cream:')


# landing image
image = load_base_image()
principal_image = st.image(image=image, caption="Mango Bavaroise")


# sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/cbuitragoh/DessertNamesCompletionApp/blob/main/src/app.py)"
    

# tabs
tab1, tab2 = st.tabs(["suggestions", "generate images"]) 

with tab1:
    st.subheader("Dessert Suggestions")
    
    model_selected = st.selectbox("Select model for generate delicious dessert suggestions",
                                    (f"{huggingface_models[0]}",
                                     f"{openAI_models[0]}",
                                     f"{openAI_models[1]}"),
                                    index=None,
                                    placeholder="Select model..."
                                )
# user input to generate suggestions
if prompt := st.chat_input(
    placeholder="Welcome a us app! Please type food product for generate dessert suggestions",
    max_chars=20
):
    if prompt == None:
        st.info("Please type a product name to continue.")
        st.stop()
    else:
        try:
            # select model is a must
            if model_selected == None:
                st.info("Please select a model to continue.")
                st.stop()
            else:
                # info about model selected
                if model_selected == "openai-gpt":
                    st.info(f"{model_selected} model is provided by HuggingFace :hugging_face:")
                else:
                    st.info(body=f"{model_selected} model is provided by OpenAI")
            if not openai_api_key and (model_selected in openAI_models): # OpenAI API key is a must
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
            with st.spinner("Generating suggestions..."):   
                final_text = create_generator(prompt=prompt,
                                              seed=42,
                                              model=model_selected,
                                              openai_api_key=openai_api_key
                            )
                st.chat_message("assistant").write(final_text.capitalize())
                set_final_text(final_text) # update state variable 'final_text' value

        
        except Exception as e:
            st.error(e)

# validate wheather user selected suggestion or not
if st.session_state.final_text != "":
    with tab2:
        st.subheader("Image for suggestions")
        results = st.session_state.final_text.split(",")
        prompt_image = st.selectbox(
            "Do you want to create an image of any of these?",
            options=[option for option in results],
            index=None,
            key="prompt_image",
            on_change=set_stage,
            args=(1,),
            placeholder="Select suggestion for generate."
            )
        # validate if user selected suggestion or not
        # validate if a previous image and its path exist or have already been deleted.
        if prompt_image == None or st.session_state.image != "False":
            set_stage(0)
            reset_image()
            if st.session_state.image_path != "":
                del_tempImage(image_path=st.session_state.image_path)
                reset_image_path()
        if st.session_state.stage > 0:
            # text cleaning
            prompt_image = normalize_text(prompt_image)
            st.info(f"Selected suggestion: {prompt_image}")
            generate_button = st.button('Generate',
                                        on_click=set_stage, 
                                        args=(2,)
                            )
            if st.session_state.stage > 1:
                with st.container():
                        try:
                            if not openai_api_key: # OpenAI_APY_KEY es a must
                                    st.info("Please add your OpenAI API key to continue.")
                                    st.stop() 
                            with st.spinner("Generating image..."):
                                # Dalle-3 API calling to generate image
                                generated_image = asyncio.run(generate_dessert_image(prompt_image,
                                                                         openai_api_key
                                                                         )
                                                            )
                                if generated_image:
                                    # Show image in container
                                    final_image = show_image(generated_image)
                                    st.image(image=final_image, caption=f"{prompt_image}")
                                    # Save image in temp folder
                                    image_path = save_tempImage(final_image, prompt_image)
                                    # update state variable 'image_path' value
                                    set_image_path(image_path)
                                    # download image
                                    with open(f"src/tempImages/{prompt_image}.jpg", "rb") as f:
                                        btn = st.download_button('Download image',
                                                           data=f,
                                                           file_name=f"{prompt_image}.jpg",
                                                           mime='image/jpeg',
                                                           on_click=set_stage,
                                                           args=(3,)
                                            )
                                    # update state variable 'image' value
                                    set_image()

                        except Exception as e:
                            st.error(e)

    
            
                     
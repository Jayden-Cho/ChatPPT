from PIL import Image
from diffusers import StableDiffusionPipeline
import tempfile
from pathlib import Path
from util import *

import torch
import gradio as gr

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

def generate_image_stable_diffusion(prompt, pipe):
    image = pipe(prompt).images[0]
    img_stream = io.BytesIO()
    image.save(img_stream, format="PNG")
    img_stream.seek(0)  # reset the stream pointer to the start    
    return img_stream

def gr_generate_slides(NUM_PAGES, TOPIC, FILENAME, method, font_choice, layout_choice, font_size, font_format):
  gpt_prompt = [{
      "role": "system",
      "content": (
          "You are a software developer creating an automated PowerPoint generation program."
          " You decide the content that goes into each slide of the PowerPoint."
          " Each slide typically consists of a topic, introduction, main points, conclusion, and references."
          " Follow the rules below:\n"
          f"1. Summarize and extract the key contents from the user's input with {NUM_PAGES} slides.\n"
          "2. Each slide contains 'title', 'content' and 'prompt'.\n"
          "3. 'content' is a bullet point that breaks down the core content into brief, step-by-step chunks.\n"
          "4. All of the slides contain images.\n"
          "5. If the slide contains a image, create a prompt to generate an image using the DALL-E API based on the summarized and extracted content. And save it into 'prompt'.\n"
          "6. Focus on nouns and adjectives and separate them with commas so that 'prompt' is a good visual representation of 'content'.\n"
          "7. Set the above contents as keys named 'title', 'content', and 'prompt'.\n"
          "9. Save the results of each slide as a JSON list.\n"
          "10. Output the final output in JSON format.\n"
          "11. Make sure output JSON can be parsed with Python `json.loads()`.\n"
          "12. Must return JSON format only\n\n"
          "Output example:\n\n"
  """```[
    {
      "title": "South Korea's declining birthrate",
      "content": [
          "1. Declining fertility rates",
          "2. Aging Society Issues",
          "3. Economic impact of population decline",
          "4. Lack of social contribution",
          "5. Lack of social support from family"
      ],
      "prompt": "sad family, old people, small family"
    },
    {
      "title": "Select a campaign topic",
      "content": [
          "1. Encouraging births",
          "2. Strengthen family support policies",
          "3. Strengthening youth sex education",
          "4. Provide economic benefits",
          "5. Social enterprise engagement"
      ],
      "prompt": "children, playing in garden, money, family"
    },
    {
      "title": "Encouraging births",
      "content": [
          "1. Improving parental leave",
          "2. Expand childcare",
          "3. Provide maternity information",
          "4. Develop a program to help women return to work after childbirth",
          "5. Enhance your life insurance benefits"
      ],
      "prompt": "parents with baby, kindergarten, pregnant, mother"
    },
    {
      "title": "Strengthen family support policies",
      "content": [
          "1. Improve housing supply policies",
          "2. Expanding public childcare",
          "3. Create a training support program",
          "4. Expanding the Family Tax Benefit",
          "5. Enhance family support services"
      ],
      "prompt": "house, kindergarten, school, tax, baby care service"
    }
  ]```"""
      )
  }, {
      "role": "user",
      "content": TOPIC
  }]

  print("[1] Generating contents...")

  # gpt_response = openai.ChatCompletion.create(
  #     model="gpt-3.5-turbo",
  #     messages=gpt_prompt)
  # # Extract necessary data from response
  # contents = gpt_response["choices"][0]["message"]["content"]

  contents = [{'title': 'Introduction to AI', 'content': ['1. Definition of AI', '2. Applications of AI', '3. Importance of AI in various industries', '4. AI technologies and techniques', '5. Impact of AI on society'], 'prompt': 'robot, machine learning, automation'},
 {'title': 'Skills required for AI', 'content': ['1. Programming languages (Python, R, Java)', '2. Statistics and probability', '3. Machine learning algorithms', '4. Deep learning architectures', '5. Data preprocessing and analysis'], 'prompt': 'code, math, neural network'},
 {'title': 'Steps to excel in AI', 'content': ['1. Learn the basics of AI', '2. Gain strong programming skills', '3. Get hands-on experience with real-world datasets', '4. Master machine learning techniques', '5. Stay updated with the latest advancements in AI'], 'prompt': 'books, coding, data science'}]

  # contents = json.loads(contents.replace("`", ""), strict=False)

  print("[2] Generating PowerPoint slides...")

  prs = Presentation()

  # Add the title slide
  add_title_slide(prs, TOPIC, font_choice, font_size, font_format)

  # Add the table of contents slide
  add_table_of_contents(prs, contents, font_choice, font_size, font_format)

  # Step 1: Create a temporary directory
  temp_dir = tempfile.mkdtemp()

  image_paths = []  # List to collect paths to saved images

  for i, content in enumerate(contents):
      if "prompt" in content and content["prompt"]:
          print(f"[3-{i+1}] Generating an image for slide #{i+1}...")
          if method == "Dall-E":
              img_stream = generate_image_dalle(content["prompt"])
          else:
              img_stream = generate_image_stable_diffusion(content["prompt"], pipe)

          # Convert BytesIO stream to PIL Image and append to the list
          image = Image.open(img_stream)

          # Step 2: Save the image to the temporary directory
          image_path = Path(temp_dir) / f"slide_{i + 1}.png"
          image.save(image_path)
          image_paths.append(image_path)

          create_slide(prs, content, img_stream, font_choice, layout_choice, font_size, font_format)

  print(f"[4] Saving result into disk... {TOPIC}.pptx")
  # Step 2 (cont.): Save the PowerPoint to the temporary directory
  ppt_path = Path(temp_dir) / f"./{TOPIC}.pptx"
  prs.save(ppt_path)
  prs.save(f"./{TOPIC}.pptx")

  print("[5] Done!")
  return image_paths, f"./{TOPIC}.pptx"

with gr.Blocks() as demo:
    gr.Markdown(
        """
        <h1 style="text-align: center;">ChatPPT</h1>
        <h3 style="text-align: center;">AI-Generated Presentations with ChatGPT, Dall-E, and Stable Diffusion<h3>
        """
    )
    with gr.Row(equal_height=True):
        with gr.Column():
            md_input = gr.Markdown(
                """
                <h3 style="text-align: center;">Input</h3>
                """
            )
            with gr.Tab("Basics"):
                pages = gr.Slider(0, 20, step=1, label='Number of Pages', value=5)
                topic = gr.Textbox(label="Topic", placeholder="Which topic would you like to create?")
                filename = gr.Textbox(label="Filename", placeholder="What will be the filename of the presentation?")
            with gr.Tab("Customizations"):
                method = gr.Radio(['Dall-E', 'Stable-Diffusion'], label='Image Generation Method', value='Dall-E')
                layout_radio = gr.Radio(choices=["Right", "Left"], label="Image  Layout", value='Right')            
                font_dropdown = gr.Dropdown(choices=["Arial", "Times New Roman", "Calibri", "Verdana"], label="Font Choice", value='Arial')
                font_size_slider = gr.Slider(10, 40, step=1, label='Font Size', value=18)
                font_format = gr.CheckboxGroup(choices=['Bold', 'Italic'], label="Font Format")
            btn = gr.Button("Generate!")
        with gr.Column():
            md_output = gr.Markdown(
                """
                <h3 style="text-align: center;">Preview Images</h3>
                """
            )
            gallery = gr.Gallery(label="Generated images", columns=5, preview=True)
            f = gr.File(label=".pptx file", interactive=False)

    btn.click(gr_generate_slides, inputs=[pages, topic, filename, method, font_dropdown, layout_radio, font_size_slider, font_format], outputs=[gallery, f])

if __name__ == "__main__":
    demo.queue().launch(debug=True, share=True)
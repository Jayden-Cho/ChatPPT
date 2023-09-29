# ChatPPT
An AI-powered tool that auto-generates PowerPoint presentations based on a given topic using ChatGPT, Dall-E, and Stable Diffusion.



# Introduction
When I develop, I always keep two ironclad rules in mind:

1. Does it improve the convenience of life?
2. Do I personally feel like using it?

With these principles, I decided to develop a program that satisfies both and enhances the convenience of my life. That is ChatPPT.

ChatPPT is an innovative AI-driven tool designed to assist users in brainstorming and generating introductory ideas for their PowerPoint presentations. By harnessing the capabilities of ChatGPT for content generation, Dall-E and Stable Diffusion for imaginative image generation, ChatPPT delivers a harmonious blend of textual and visual elements, providing a foundational start for any presentation.

**The main goal is to enable users to come up with or brainstorm some basic introductory ideas on creating presentations for their needs, alleviating the initial burden and sparking creativity.**

# Requirements
- [openai](https://github.com/openai/openai-python) (For accessing the core functionalities of GPT models.)
- [python-pptx](https://python-pptx.readthedocs.io/en/latest/) (For generating and manipulating PowerPoint files.) 
- [gradio](https://www.gradio.app/) (For creating an interactive interface for our application.)
- [diffusers](https://huggingface.co/runwayml/stable-diffusion-v1-5) (For harnessing Stable Diffusion techniques.)
- [transformers](https://huggingface.co/docs/transformers/index) (Library by HuggingFace providing access to many transformer-based models.)

All the required libraries are listed in the **`requirements.txt`** file. You can easily install them using the following command:

```
pip install -r requirements.txt
```

# Table Of Contents
-  [In a Nutshell](#in-a-nutshell)
-  [Future Work](#future-work)
-  [Contributing](#contributing)
-  [Acknowledgments](#acknowledgments)

# In a Nutshell   

To utilize the capabilities of **ChatPPT**, users will follow a streamlined process from launching the application to generating the final PowerPoint slides. Here's a step-by-step guide:

1. **Launch the Application**: Begin by running the app.py script. This initializes the gradio interface, beautifully rendering the main dashboard of ChatPPT with an emphasis on user-friendliness. Before launching the app, make sure to provide your OpenAI API key on `util.py`.
    ```
    python app.py
    ```

2. **Input Presentation Details**:
    * **Basics Tab**:
      * Define the number of pages for your presentation using the slider.
      * Specify the main topic or subject of the presentation.
      * Provide a desired filename for the final PowerPoint file.
    * **Customizations Tab**:
      * Choose between two powerful image generation methods: 'Dall-E' or 'Stable-Diffusion'.
      * Select the desired image layout for your slides, either 'Right' or 'Left'.
      * Personalize your presentation with font customizations, such as font type, size, and style (e.g., bold, italic).

3. **Generate Presentation Content**: After inputting the desired parameters, click on the "Generate!" button. The underlying code, particularly the **`gr_generate_slides()`** function in `util.py`, begins its magic. It crafts the presentation by:
    * Initiating the AI models to brainstorm content.
    * Making calls to functions such as **`generate_image_dalle()`** or **`generate_image_stable_diffusion()`** to generate relevant images.
    * Constructing individual slides with the help of **`create_slide()`**.
    * Adding a title slide and a table of contents through **`add_title_slide()`** and **`add_table_of_contents()`**, respectively.

4. **Preview and Download**: Once the process completes:
    * A gallery of generated images related to your topic will be displayed in the "Preview Images" section. This gives a quick look at the visuals that will be incorporated into your presentation.
    * A downloadable **.pptx** file will be available, containing all the generated slides tailored to your specified details.

5. **Refine and Iterate**: You have the flexibility to tweak input parameters and regenerate slides as needed. The interactive nature of **ChatPPT** allows for a dynamic creation process that caters to varying user preferences.



# Demo in Google Colab
Experience the functionality of ChatPPT without any local setup! Try out our interactive Colab notebook:

<a target="_blank" href="https://colab.research.google.com/github/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/model_monitoring/model_monitoring.ipynb](https://colab.research.google.com/drive/1uo-LE6fnlQWng1xNg5e0rVEMSUjln_6P?authuser=1#scrollTo=_7Xae7iBupPj">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Click the badge above and follow the steps in the notebook.

# Future Work
  * Integrate more diverse AI models for content generation.
  * Implement support for various presentation themes and templates.
  * Offer user customization for slide transitions and animations.

# Contributing
Contributions, bug fixes, and enhancements are always welcome. Please feel free to open an issue or send a pull request.


# Acknowledgments
  * **OpenAI** for ChatGPT and Dall-E models.
  * **RunwayML** for the Stable Diffusion model.
  * **Gradio** for providing the rapid UI generation toolkit.

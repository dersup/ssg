📄 ssg


A lightweight static site generator written in Python.


Generate fast, simple, and portable websites from source files like Markdown, templates, or structured content.



🚀 Features




⚡ Fast static site generation


📝 Content-driven workflow (e.g., Markdown or text-based input)


🧩 Template-based page rendering


📁 Simple project structure


🔌 Easy to extend and customize





📦 Installation


Clone the repository:

```
git clone https://github.com/dersup/ssg.git
cd ssg
```


(Optional) Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```


Install dependencies (if applicable):

```
pip install -r requirements.txt
```



🛠️ Usage


Run the generator:

```
python main.py
```


📁 Project Structure

```
ssg/
├── src/            # Source content (markdown, data, etc.)
├── templates/      # HTML / template files
├── dist/           # Generated static site output
├── main.py         # Entry point
└── README.md
```



⚙️ How It Works

Place your content inside the src/ directory


Define layouts/templates in templates/


Run the generator


Output is written to dist/


Static site generators work by converting content into pre-built HTML files, making sites fast, secure, and easy to deploy .



✏️ Example Workflow


# Add content
```
echo "# Hello World" > src/index.md
```
# Build site
```
python main.py
```
# Open output
```
open dist/index.html
```



🌐 Deployment


You can deploy the generated dist/ folder to:


GitHub Pages


Netlify


Vercel


Any static file host


Contributions are welcome!




Fork the repo


Create a new branch


Make your changes


Submit a pull request





📜 License


This project is licensed under the MIT License.

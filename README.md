
# Youtube-Chatbot 🎥💬

A conversational chatbot app that lets you interact with YouTube content using AI.
Built with **Streamlit** and powered by **Together API**.

---

## 🚀 Demo

Experience a seamless interface to extract, process, and chat with YouTube video transcripts!

<p align="center">
  <img src="Step 1.png" alt="Step 1" />
  <img src="Step 2.png" alt="Step 2" width="400"/>
  <br>
  <img src="Step 3.png" alt="Step 3" width="400"/>
  <img src="Step 4.png" alt="Step 4" width="400"/>
  <br>
  <img src="Step 5.png" alt="Step 5" width="400"/>
</p>

---

## 🗂️ Project Structure

| Symbol | File/Folder            | Description                         |
| ------ | ---------------------- | ----------------------------------- |
| ¢      | .env                   | Your API key (keep this **secret**) |
| =      | .env(example)          | Template for your `.env` file       |
| \*     | app.py                 | Main Streamlit chatbot app          |
| &      | extract\_transcript.py | Extracts YouTube transcripts        |
| \*     | extract.py             | Helper extraction script            |
| ₴      | hybrid\_chunking.py    | Efficient hybrid chunking logic     |
| •      | README.md              | This file                           |
| =      | requirements.txt       | Python dependencies                 |
| \$     | run.sh                 | Script to launch the app            |
| \$     | setup.sh               | Script to set up the environment    |

---

## 🛠️ Quickstart

### 1. **Clone the repository**

```bash
git clone https://github.com/Rohitg9234/Youtube-Chatbot.git
cd Youtube-Chatbot
```

---

### 2. **Set up your environment**

```bash
chmod +x setup.sh run.sh
./setup.sh
```

---

### 3. **Configure your API key**

* Copy `.env(example)` to `.env`:

  ```bash
  cp .env(example) .env
  ```
* Edit `.env` and add your Together API key:

  ```
  export TOGETHER_API_KEY=your_actual_key_here
  ```

---

### 4. **Run the app**

```bash
./run.sh
```

Open the Streamlit link from your terminal in your browser.

---

## 💡 Features

* Extract YouTube video transcripts
* Advanced hybrid chunking for better AI context
* Clean, step-by-step interface (see screenshots above!)
* Easy setup and run with scripts

---

## 📁 Example `.env` file

```bash
export TOGETHER_API_KEY=your_actual_key_here
```

---

## 📦 Requirements

* Conda
* Python 3.10+
* Streamlit

---

## 🤝 Contributing

Pull requests and suggestions are welcome!
Feel free to [open an issue](https://github.com/Rohitg9234/Youtube-Chatbot/issues).

---

## 📝 License

MIT

---

### ✨ Happy Chatting with YouTube! ✨


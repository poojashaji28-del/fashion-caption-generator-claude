# Fashion Instagram Caption Generator (Python Edition)

Generate up to 10 unique, engaging Instagram captions for fashion content using Claude AI. Choose between CLI or web app interface.

## Features

✨ **Two Interfaces:**
- **CLI Tool** - Command-line interface for quick caption generation
- **Web App** - Beautiful web interface with all preference controls

🎯 **Smart Generation:**
- Generate 1-10 unique captions per request
- Customize tone (sophisticated, playful, inspiring, casual, edgy)
- Choose style (trendy, minimalist, luxe, vintage, bold)
- Target specific audiences (general, luxury, Gen-Z, professionals, creators)
- Toggle hashtags and emojis on/off

📋 **Convenient Features:**
- Interactive prompt mode
- Batch file export
- One-click copy (web version)
- Error handling and validation

## Installation

### Step 1: Clone or copy the files

You should have these files:
```
caption_generator.py    (Core module + CLI)
app.py                  (Flask web app)
requirements.txt        (Dependencies)
README.md              (This file)
```

### Step 2: Create a virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get your Anthropic API key

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key

### Step 5: Set up environment variables

Create a `.env` file in your project root:

```bash
# .env
ANTHROPIC_API_KEY=YOUR_API_KEY_HERE
```

⚠️ **IMPORTANT:** Replace `YOUR_API_KEY_HERE` with your actual Anthropic API key.

### Step 6: Add to .gitignore

Make sure your `.env` file is in `.gitignore`:

```bash
# .gitignore
.env
.env.local
*.pyc
__pycache__/
venv/
```

Check it's there:
```bash
cat .gitignore
```

---

## Usage

### Option 1: CLI Tool

The command-line interface offers multiple ways to generate captions.

#### Quick generation with options:

```bash
python caption_generator.py generate --topic "Summer outfit" --tone sophisticated --style trendy --count 5
```

**Full options:**

```bash
python caption_generator.py generate \
  --topic "New collection launch" \
  --tone sophisticated \
  --style luxe \
  --audience luxury \
  --count 8 \
  --hashtags \
  --emojis
```

**Interactive mode:**

```bash
python caption_generator.py interactive
```

This will guide you through all preferences step-by-step with a menu.

#### Command-line arguments:

| Option | Type | Default | Values |
|--------|------|---------|--------|
| `--topic` | text | required | Any topic/theme |
| `--tone` | choice | sophisticated | sophisticated, playful, inspiring, casual, edgy |
| `--style` | choice | trendy | trendy, minimalist, luxe, vintage, bold |
| `--audience` | choice | general | general, luxury, Gen-Z, professionals, creators |
| `--count` | int | 5 | 1-10 |
| `--hashtags` | flag | True | --hashtags / --no-hashtags |
| `--emojis` | flag | True | --emojis / --no-emojis |

#### Save captions to file:

The CLI will ask if you want to save after generation. Or use Python:

```python
from caption_generator import CaptionGenerator

generator = CaptionGenerator()
captions = generator.generate(
    topic="Summer outfit",
    tone="playful",
    num_captions=5
)

# Save to file
with open('captions.txt', 'w', encoding='utf-8') as f:
    for i, caption in enumerate(captions, 1):
        f.write(f"{i}. {caption}\n")
```

---

### Option 2: Web App

Beautiful web interface with GUI controls.

#### Start the server:

```bash
python app.py
```

The app will run at: **http://localhost:5000**

#### Using the web app:

1. Open http://localhost:5000 in your browser
2. Enter your caption topic
3. Click tone/style/audience buttons to select preferences
4. Adjust the caption count slider (1-10)
5. Toggle hashtags and emojis as needed
6. Click "Generate Captions"
7. Click any caption to copy it to clipboard
8. Click "Generate New Captions" to reset and create more

#### Customizing the web app:

**Change port:**
```python
# In app.py, change the last line:
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change 5000 to desired port
```

**Deploy the web app:**

The Flask app can be deployed to:
- Heroku
- PythonAnywhere
- Render
- AWS/Google Cloud
- Your own server

Example for Heroku:
```bash
echo "web: gunicorn app:app" > Procfile
pip install gunicorn
git push heroku main
```

---

## Programmatic Usage

Use the module in your own Python code:

```python
from caption_generator import CaptionGenerator

# Initialize
generator = CaptionGenerator()

# Generate captions
captions = generator.generate(
    topic="Winter fashion collection",
    tone="sophisticated",
    style="luxe",
    audience="luxury",
    num_captions=8,
    include_hashtags=True,
    include_emojis=True
)

# Use the captions
for i, caption in enumerate(captions, 1):
    print(f"{i}. {caption}")
```

### Parameters

- `topic` (str, required) - The main topic/theme
- `tone` (str) - One of: 'sophisticated', 'playful', 'inspiring', 'casual', 'edgy'
- `style` (str) - One of: 'trendy', 'minimalist', 'luxe', 'vintage', 'bold'
- `audience` (str) - One of: 'general', 'luxury', 'Gen-Z', 'professionals', 'creators'
- `num_captions` (int) - Number of captions (1-10)
- `include_hashtags` (bool) - Include hashtags in captions
- `include_emojis` (bool) - Include emojis in captions

### Returns

List of caption strings

---

## Troubleshooting

### "API key not found" error

**Solution:** Make sure your `.env` file has:
```
ANTHROPIC_API_KEY=YOUR_API_KEY_HERE
```

And you're running the script from the same directory as `.env`.

### "Module not found" error

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "Invalid API key" error

**Solution:**
1. Check your API key is correct (no extra spaces)
2. Get a new key from [console.anthropic.com](https://console.anthropic.com)
3. Update your `.env` file
4. Restart your script/server

### Slow generation

**Causes:**
- API rate limiting (try again in a few moments)
- Poor internet connection
- Server load

**Solution:** Try again after a few seconds.

### "Cannot find caption_generator.py" when running app.py

**Solution:** Make sure both files are in the same directory.

---

## Security Best Practices

✅ **DO:**
- Store your API key in `.env` file (not in code)
- Add `.env` to `.gitignore`
- Regenerate your API key if accidentally committed
- Use environment variables for all secrets

❌ **DON'T:**
- Commit `.env` file to GitHub
- Share your API key publicly
- Hardcode the key in your code
- Upload `.env` to version control

---

## API Information

**Model:** `claude-opus-4-6` (latest, most capable model)
**Max Tokens:** 1000 per request
**Endpoint:** Anthropic API v1/messages

See [Anthropic Documentation](https://docs.anthropic.com) for more details.

## Performance & Costs

- Generation time: 2-5 seconds per request
- API cost: Based on token usage (~500-1000 tokens per request)
- Check [pricing](https://www.anthropic.com/pricing) for current rates

## File Structure

```
caption-generator/
├── .env                    (Your API key - in .gitignore)
├── .gitignore
├── caption_generator.py    (Core module + CLI)
├── app.py                  (Flask web app)
├── requirements.txt
└── README.md
```

## Customization

### Modify available tones

In `caption_generator.py`, line 165:
```python
tones = ['sophisticated', 'playful', 'inspiring', 'casual', 'edgy']
```

### Modify available styles

In `caption_generator.py`, line 172:
```python
styles = ['trendy', 'minimalist', 'luxe', 'vintage', 'bold']
```

### Modify available audiences

In `caption_generator.py`, line 179:
```python
audiences = ['general', 'luxury', 'Gen-Z', 'professionals', 'creators']
```

### Change max caption count

In `caption_generator.py`, line 52 and CLI options:
```python
if not 1 <= num_captions <= 10:  # Change max value here
```

---

## Support

For issues with:
- **Python setup**: See [Python docs](https://www.python.org/doc/)
- **Flask**: See [Flask docs](https://flask.palletsprojects.com)
- **Anthropic API**: See [Anthropic docs](https://docs.anthropic.com)
- **Click CLI**: See [Click docs](https://click.palletsprojects.com)

---

## Version History

- **v1.0** - Initial release with CLI and web app interfaces

## License

Use freely for personal and commercial projects.

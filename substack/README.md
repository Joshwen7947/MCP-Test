# Substack Notes Automation Tool

Automatically post notes to your Substack at scheduled times using Python and Selenium.

## 🚀 Features

- **Automated Posting**: Schedule notes to be posted automatically
- **Random Content**: Posts random notes from your curated collection
- **Flexible Scheduling**: Set multiple posting times throughout the day
- **Browser Automation**: Uses Selenium to interact with Substack's web interface
- **Error Handling**: Robust error handling and logging
- **Easy Configuration**: Simple setup with environment variables

## 📋 Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Substack account with Notes enabled

## 🛠️ Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your credentials**:
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your actual credentials
   nano .env
   ```

4. **Configure your .env file**:
   ```
   SUBSTACK_EMAIL=your_email@example.com
   SUBSTACK_PASSWORD=your_password_here
   SUBSTACK_URL=https://your-substack.substack.com
   ```

## 🎯 Usage

### Quick Start

Run the automation tool:
```bash
python substack.py
```

Choose from three options:
1. **Post a single note now** - Test the system immediately
2. **Set up scheduled posting** - Configure automatic posting times
3. **Run scheduler** - Start continuous automated posting

### Configuration Options

#### Posting Times
You can set multiple posting times:
- Single time: `09:00`
- Multiple times: `09:00,15:00,21:00`

#### Notes Content
Edit `notes.json` to customize your notes:
```json
[
  {
    "content": "Your note content here...",
    "tags": ["tag1", "tag2"],
    "category": "category_name"
  }
]
```

## 📁 File Structure

```
substack/
├── substack.py          # Main automation script
├── requirements.txt     # Python dependencies
├── notes.json          # Your notes content (auto-created)
├── env_example.txt     # Environment variables template
└── README.md           # This file
```

## 🔧 How It Works

1. **Browser Setup**: Launches Chrome with automation settings
2. **Login**: Automatically logs into your Substack account
3. **Navigation**: Goes to the Notes section
4. **Posting**: Selects a random note and posts it
5. **Scheduling**: Uses the `schedule` library for timing
6. **Cleanup**: Closes browser and handles errors

## 🎨 Customizing Notes

The tool automatically creates a `notes.json` file with sample content. You can:

- **Add your own notes**: Edit the content, tags, and categories
- **Organize by category**: Group notes by topic (programming, productivity, etc.)
- **Use rich content**: Include emojis, code snippets, and formatting

### Example Note Structure
```json
{
  "content": "Just learned something amazing about Python! 🐍\n\nDid you know that Python's list comprehensions are not only more readable but often faster than traditional loops?",
  "tags": ["python", "programming", "tips"],
  "category": "programming"
}
```

## ⚙️ Advanced Configuration

### Running in Headless Mode
For server deployment, uncomment this line in `substack.py`:
```python
chrome_options.add_argument("--headless")
```

### Custom Posting Schedule
Modify the default schedule in the script:
```python
poster.setup_schedule(["08:00", "12:00", "18:00"])
```

### Error Handling
The tool includes comprehensive error handling:
- Network connection issues
- Login failures
- Element not found errors
- Browser crashes

## 🚨 Important Notes

### Security
- Never commit your `.env` file to version control
- Use strong passwords for your Substack account
- Consider using 2FA for additional security

### Rate Limiting
- The tool includes delays to be respectful to Substack
- Don't set too many posting times (max 3-4 per day recommended)
- Monitor your account for any issues

### Browser Requirements
- Chrome browser must be installed
- ChromeDriver is automatically downloaded and managed
- Ensure Chrome is up to date

## 🐛 Troubleshooting

### Common Issues

1. **"ChromeDriver not found"**
   - The tool automatically downloads ChromeDriver
   - Ensure you have internet connection during first run

2. **"Login failed"**
   - Check your email and password in `.env`
   - Ensure 2FA is disabled or handle it manually

3. **"Could not find note input element"**
   - Substack's interface may have changed
   - Check if Notes feature is enabled on your account

4. **"Browser crashes"**
   - Try running without headless mode for debugging
   - Check Chrome browser version compatibility

### Debug Mode
Run with visible browser to see what's happening:
```python
# Comment out this line in substack.py:
# chrome_options.add_argument("--headless")
```

## 🔄 Automation Ideas

### Content Sources
- **RSS Feeds**: Automatically post summaries of interesting articles
- **API Data**: Post daily statistics or updates
- **File Monitoring**: Post when new content is added to a folder
- **Social Media**: Cross-post from Twitter or LinkedIn

### Scheduling Variations
- **Time-based**: Different content at different times
- **Day-based**: Weekday vs weekend content
- **Event-based**: Post around specific events or holidays

## 📊 Monitoring

### Logs
The tool provides detailed console output:
- Login status
- Posting success/failure
- Error messages
- Timing information

### Success Tracking
Monitor your Substack analytics to see:
- Post engagement
- Optimal posting times
- Content performance

## 🤝 Contributing

Feel free to enhance this tool:
- Add more content sources
- Improve error handling
- Add analytics tracking
- Support for other platforms

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with Substack's terms of service.

---

**Happy Automating! 🤖**


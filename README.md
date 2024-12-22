# 🤖 ChatGPT Python Client

## 📝 Description
A modern, object-oriented Python client for interacting with chat models. This project demonstrates advanced Python concepts including OOP design patterns, type hinting, error handling, and clean code principles.

## ⚠️ Important Disclaimer
This code is provided **strictly for educational purposes** to demonstrate Python programming concepts and software architecture patterns. It should NOT be used to:
- Circumvent any terms of service
- Access services without proper authorization
- Engage in any form of API abuse or misuse
- Cause harm to any services or organizations

Please respect all terms of service and use official APIs for production applications.

## ✨ Features
- 🎯 Type-safe implementation with modern Python type hints
- 🛡️ Robust error handling with custom exception hierarchy
- 🔄 Clean, maintainable OOP design
- 📊 Support for multiple chat models
- ⚡ Efficient session management
- 🔍 Comprehensive input validation
- 📝 Detailed logging and error reporting

## 🛠️ Technical Architecture
The project follows a clean, modular architecture:
- `ChatModelEnum`: Enumeration of supported models
- `Message`: Dataclass for chat message representation
- `ChatClientBase`: Abstract base class defining the client interface
- `ChatGPT`: Concrete implementation with full functionality
- Custom exception hierarchy for granular error handling

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.7
cloudscraper
```

### Installation
```bash
# Clone the repository
git clone https://github.com/sujalrajpoot/ChatGPT-Python-Client.git
cd ChatGPT-Python-Client

# Install dependencies
pip install cloudscraper
```

### Basic Usage
```python
from chat_client import ChatGPT, ChatModelEnum

# Initialize client
client = ChatGPT()

# Send a message
try:
    response = client.chat("Hello!", ChatModelEnum.GPT4O)
    print(response)
except ChatGPTError as e:
    print(f"Error occurred: {e}")
```

## 🔧 Configuration
The client can be configured with custom parameters:
```python
client = ChatGPT(
    timeout=30,  # Request timeout in seconds
    stream_chunk_size=1000  # Size of streaming chunks
)
```

## 🎯 Error Handling
The client implements a comprehensive error handling system:
- `ChatGPTError`: Base exception class
- `ConnectionError`: Network-related issues
- `AuthenticationError`: Authentication failures
- `ParseError`: Response parsing problems

## 📚 Best Practices
When using this code for learning:
- Study the OOP patterns implemented
- Understand the type hinting system
- Learn from the error handling architecture
- Examine the documentation practices
- Analyze the code organization

## 🔒 Security Notes
- Never store sensitive information in code
- Use environment variables for configuration
- Implement rate limiting in production code
- Follow security best practices
- Respect API terms of service

## 📖 Documentation
- Code includes comprehensive docstrings
- Type hints provide additional documentation
- Comments explain complex logic
- README covers all major features
- Examples demonstrate proper usage

## 👥 Community Guidelines
- Be respectful and constructive
- Focus on educational aspects
- Help others learn
- Share knowledge
- Maintain code quality

## ⭐ Show Your Support
If you find this educational project helpful:
- Star the repository
- Share with other learners
- Provide feedback
- Contribute improvements
- Help others learn

---

# Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

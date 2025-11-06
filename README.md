# OpenWebUI Pipes Collection

A collection of AI model integration pipes for Open WebUI, enabling seamless access to multiple leading AI providers through a unified interface.

> **Note:** This collection includes pipes from multiple authors across the Open WebUI community. Each pipe is credited to its respective author(s) below.

## What are Pipes?

Pipes are Open WebUI's integration layer that connects various AI model providers to your Open WebUI instance. Each pipe acts as a bridge, translating Open WebUI requests into provider-specific API calls.

---

## Available Pipes

### 🤖 Anthropic Claude Pipe
**File:** `anthropic_pipe.py`
**Author:** [justinh-rahb](https://github.com/justinh-rahb) and christian-taillon

Connect to Anthropic's Claude models, featuring some of the most advanced AI language models available.

**Features:**
- Full Claude model family support (3, 3.5, 3.7, 4, 4.5)
- Image processing with automatic size validation and compression
- Streaming and non-streaming responses
- Multimodal support (text + images)
- Advanced parameter handling for newer models

**Available Models:**
- Claude 3 Family: Haiku, Opus, Sonnet
- Claude 3.5 Family: Haiku, Sonnet (June & Oct releases)
- Claude 3.7: Hybrid reasoning model
- Claude 4 Family: Sonnet, Opus 4.1
- Claude 4.5 Family: Sonnet, Haiku (Latest)

**Configuration:** Requires `ANTHROPIC_API_KEY`

---

### ☁️ Cloudflare Workers AI Pipe
**File:** `cloudflare_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Access Cloudflare's Workers AI platform with a variety of open-source models running on Cloudflare's edge network.

**Features:**
- Multiple model size options (1B to 120B parameters)
- Fast edge inference
- No cold starts
- Cost-effective AI processing

**Available Models:**
- **Large Models:** GPT-OSS 120B, Llama 3.1/3.3 70B, Mistral Small 3.1 24B
- **Medium Models:** Llama 3.1 8B, Mistral 7B, Qwen 2.5 Coder 32B, Gemma 3 12B
- **Lightweight Models:** GPT-OSS 20B, Llama 3.2 1B/3B

**Configuration:** Requires `CLOUDFLARE_API_KEY` and `CLOUDFLARE_ACCOUNT_ID`

---

### 🧠 DeepSeek Pipe
**File:** `deepseek_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Integrate DeepSeek's powerful language models, including their innovative reasoning model.

**Features:**
- Chat and reasoning modes
- OpenAI-compatible API
- Streaming support
- Advanced parameter control

**Available Models:**
- **DeepSeek Chat (V3.2-Exp):** General-purpose conversational AI
- **DeepSeek Reasoner (V3.2-Exp):** Advanced reasoning and thinking mode

**Configuration:** Requires `DEEPSEEK_API_KEY`

---

### 🔍 Google Gemini Pipe
**File:** `google_pipe.py`
**Author:** [owndev](https://github.com/owndev/) and olivier-lacroix

The most feature-rich pipe in the collection, offering Google's Gemini models with extensive capabilities.

**Features:**
- Full Gemini model family support
- Advanced image generation with Gemini 2.5 Flash Image Preview
- Intelligent image optimization and compression
- Multi-image processing with history tracking
- Google Search grounding integration
- Native tool calling support
- Thinking/reasoning output formatting
- Vertex AI support for enterprise deployments
- Configurable safety settings
- Encrypted API key storage

**Advanced Image Capabilities:**
- Automatic image size optimization
- Intelligent compression with quality control
- Support for multiple images in prompts
- Image deduplication in conversation history
- Configurable image reference limits
- Generated image upload to Open WebUI

**Available Models:**
- All Gemini 1.5, 2.0, and 2.5 variants
- Special image generation models (marked with 🎨)
- Flash, Pro, and experimental variants

**Configuration:**
- Standard: `GOOGLE_API_KEY`
- Enterprise: `GOOGLE_CLOUD_PROJECT` for Vertex AI

---

### 🌟 Mistral AI Pipe
**File:** `mistral_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Access Mistral AI's powerful open and proprietary models, including specialized code generation models.

**Features:**
- Full model lineup from 7B to 123B parameters
- Multimodal support on newer models
- Specialized code generation with Codestral
- Open-source and proprietary options
- Advanced parameter support

**Available Models:**
- **Large Models:** Mistral Large 2.1 (123B params)
- **Small Models:** Mistral Small 3.2 (multimodal)
- **Medium Models:** Mistral Medium 3.1
- **Code Models:** Codestral (latest and 2501)
- **Open-Source Models:** Mistral 7B, Mixtral 8x7B, Mixtral 8x22B

**Configuration:** Requires `MISTRAL_API_KEY`

---

### 🔮 Perplexity AI Pipe
**File:** `perplexity_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Integrate Perplexity's search-enhanced AI models for responses grounded in real-time information.

**Features:**
- Search-enhanced responses
- Reasoning model variants
- Real-time information access
- Citation support

**Available Models:**
- **Sonar Pro:** Premium search-enhanced model
- **Sonar:** Standard search-enhanced model
- **Sonar Reasoning:** Reasoning with search
- **Sonar Reasoning Pro:** Premium reasoning with search

**Configuration:** Requires `PERPLEXITY_API_KEY`

---

### 🚀 x.AI Grok Pipe
**File:** `xai_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Connect to x.AI's Grok models, featuring some of the largest context windows available.

**Features:**
- Massive context windows (up to 2M tokens)
- Fast reasoning variants
- Vision capabilities
- Image generation
- Code-specialized models

**Available Models:**
- **Grok 4 Fast:** Reasoning and non-reasoning variants (2M context)
- **Grok 4:** 256K context window
- **Grok 3:** 131K context window
- **Grok 3 Mini:** Efficient variant
- **Grok 2 Vision:** Multimodal capabilities
- **Grok Code Fast:** Specialized for coding
- **Grok 2 Image:** Image generation

**Configuration:** Requires `XAI_API_KEY`

---

### 🌏 Z.AI Pipe
**File:** `zai_pipe.py`
**Author:** [dotcomdudee](https://github.com/dotcomdudee)

Integrate Z.AI (Zhipu AI) models, including the GLM series and multimodal capabilities.

**Features:**
- Text generation with GLM models
- Visual reasoning
- Image generation with CogView
- Video frame generation
- Chinese and English support

**Available Models:**
- **GLM-4.6:** Flagship language model
- **GLM-4.5V:** Visual reasoning capabilities
- **CogView-4:** Advanced image generation
- **CogVideoX-3:** Video frame generation

**Configuration:** Requires `ZAI_API_KEY`

---

## Installation

1. Copy the desired pipe files to your Open WebUI Functions/Pipes directory
2. Configure the required API keys through Open WebUI's admin panel or environment variables
3. Restart Open WebUI to load the pipes
4. Select your preferred model from the model dropdown

## Configuration

Each pipe requires specific API credentials. You can set these through:

- **Environment Variables:** Set before starting Open WebUI
- **Valve Settings:** Configure through the Open WebUI admin interface

### Example Environment Variables:
```bash
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
export DEEPSEEK_API_KEY="your-key-here"
export MISTRAL_API_KEY="your-key-here"
export PERPLEXITY_API_KEY="your-key-here"
export XAI_API_KEY="your-key-here"
export ZAI_API_KEY="your-key-here"
export CLOUDFLARE_API_KEY="your-key-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

## Common Features

All pipes support:
- Streaming responses
- Temperature control
- Max token limits
- Top-p sampling
- Custom system messages
- Chat history

## License

These pipes are provided under their respective licenses (MIT or Apache 2.0). See individual pipe files for specific authorship and licensing information.

### Attribution Summary:
- **Anthropic Pipe:** justinh-rahb and christian-taillon (MIT)
- **Cloudflare Pipe:** dotcomdudee (MIT)
- **DeepSeek Pipe:** dotcomdudee (MIT)
- **Google Gemini Pipe:** owndev and olivier-lacroix (Apache 2.0)
- **Mistral Pipe:** dotcomdudee (MIT)
- **Perplexity Pipe:** dotcomdudee (MIT)
- **x.AI Grok Pipe:** dotcomdudee (MIT)
- **Z.AI Pipe:** dotcomdudee (MIT)

## Contributing

Contributions are welcome! Please ensure any modifications maintain compatibility with Open WebUI's pipe interface.

---

**Note:** API keys and usage are subject to each provider's terms of service and pricing. Always review provider documentation before use.

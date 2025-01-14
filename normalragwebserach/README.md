# AI Assistant with CrewAI

A powerful multi-agent AI system powered by [crewAI](https://crewai.com) that combines knowledge base search, web research, and intelligent conversation capabilities.

## Quick Start

### Prerequisites
- Python >=3.10 <3.13
- Conda (Miniconda or Anaconda)
- Git
- API Keys:
  - [OpenAI API Key](https://platform.openai.com)
  - [Serper API Key](https://serper.dev)

### Installation

1. Clone and navigate:
```bash
git clone https://github.com/vinoth12940/AIAssistant.git
cd AIAssistant
```

2. Set up environment:
```bash
conda create -n normalragwebserach python=3.11
conda activate normalragwebserach
```

3. Install project:
```bash
cd AIAssistant/normalragwebserach
pip install -e .
```

4. Configure environment:
Create `.env` file in the normalragwebserach directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
MODEL=gpt-4-0125-preview
```

### Run Application
```bash
conda activate normalragwebserach
streamlit run src/normalragwebserach/ui.py
```
Access at http://localhost:8501

## Features

- **Intelligent Query Processing**: Automatically identifies query type and routes to appropriate agent
- **Multi-Agent System**: Specialized agents for different tasks working in coordination
- **Knowledge Base Integration**: Local database search for customer information
- **Web Research**: Real-time internet search and content analysis
- **Interactive UI**: User-friendly Streamlit interface
- **Extensible Architecture**: Easy to customize and extend

## System Architecture

### Agents

1. **Conversation Agent**
   - Primary coordinator
   - Query analysis
   - Response formatting

2. **Knowledge Base Expert**
   - Local database operations
   - Customer data retrieval
   - Documentation search

3. **Web Research Expert**
   - Internet searches
   - Content retrieval
   - Source verification

### Query Types

1. **Knowledge Base Queries**
   - Customer information
   - Product details
   - Documentation

2. **Web Search Queries**
   - Current events
   - General information
   - Research topics

3. **Coding Questions**
   - Technical help
   - Implementation guidance
   - Code examples

4. **Conversational**
   - General chat
   - Opinions
   - Assistance

## Technical Implementation

### Task Flow
1. Query Analysis → query_analysis.md
2. Information Retrieval (based on type):
   - Knowledge Base Search → knowledge_output.md
   - Web Search → search_output.md
3. Response Generation → conversation_output.md

### CrewAI Integration
```python
# Two-Phase Execution
1. Analysis Phase:
   - Single agent (conversation_agent)
   - Query type determination

2. Task Phase:
   - Multiple agents
   - Dynamic task selection
   - Sequential processing
```

## Customization

Modify these files to customize behavior:
- `src/normalragwebserach/config/agents.yaml`: Agent definitions
- `src/normalragwebserach/config/tasks.yaml`: Task configurations
- `src/normalragwebserach/crew.py`: Core logic
- `src/normalragwebserach/main.py`: Input handling

## Performance Optimization

For better performance:
```bash
xcode-select --install  # macOS only
pip install watchdog
```

## Support & Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
- [Documentation Chat](https://chatg.pt/DWjSBZn)

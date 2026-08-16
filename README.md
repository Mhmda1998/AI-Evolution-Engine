🧬 AI-Evolution-Engine

V8 Real Agent Evolution Engine

AI-Evolution-Engine is an experimental framework for evaluating and evolving AI agents through iterative generations.

Instead of treating an AI agent as a fixed program, the engine creates a population of agents, evaluates their performance on tasks, identifies high-performing agents, protects elite agents, and generates new candidates for subsequent generations.

Core loop:

Evaluate → Select → Protect → Evolve → Evaluate Again

⸻

🚀 Key Features

* 🤖 AI agent population management
* 🧪 Automated task evaluation
* 📊 Performance scoring
* 🏆 Elite-agent selection
* 🛡️ Elite protection across generations
* 🧬 Child-agent generation
* 🔄 Multi-generation evolution
* 📈 Performance tracking
* 🔌 Gemini-powered AI backend
* 🔐 User-provided API keys
* 🌱 Reproducible experiments through configurable seeds

⸻

🧬 How the Evolution Works
Initial Population
        │
        ▼
   Task Evaluation
        │
        ▼
 Performance Scoring
        │
        ▼
   Elite Selection
        │
   ┌────┴────┐
   ▼         ▼
Elite      Children
Protected  Generated
   │         │
   └────┬────┘
        ▼
 Next Generation
        │
        ▼
   Re-evaluation
        │
        └──────────► Repeat

        Each generation evaluates the current population and uses measured performance to determine which agents should survive and which new agents should be created.

⸻

🧠 V8 Architecture

The V8 engine is organized around several concepts.

Agent Population

A generation contains multiple candidate agents that compete on the same evaluation tasks.

Evaluation

Each agent is tested against a defined task set.

Scoring

The engine calculates a performance score based on task results.

Elite Selection

The strongest-performing agents are selected as elites.

Elite Protection

Elite agents are preserved when creating the next generation.

Child Generation

New candidate agents are generated from successful evolutionary states.

Generational Evolution

The process repeats across multiple generations, allowing the population to explore different agent strategies.

📁 Project Structure

AI-Evolution-Engine/
│
├── V7_Elite_Evolution.py
├── V8_Real_Agent_Evolution.py
├── run_v8.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
V8_Real_Agent_Evolution.py

The main V8 Real Agent Evolution Engine.

run_v8.py

The main entry point used to launch the V8 experiment.

V7_Elite_Evolution.py

The previous experimental evolution engine.

requirements.txt

Python dependencies required by the project.

README.md

Project documentation and usage instructions.

⸻

⚡ Quick Start

1. Clone the repository
2. git clone https://github.com/Mhmda1998/AI-Evolution-Engine.git
cd AI-Evolution-Engine
2. Install dependencies
3. pip install -r requirements.txt
4. 3. Configure Gemini API

Create your own Gemini API key and expose it through the environment variable:
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
On Windows:setx GEMINI_API_KEY "YOUR_GEMINI_API_KEY"
Never put your API key directly inside the source code or commit it to GitHub.

⸻

▶️ Run the Engine

After configuring your API key:python run_v8.py
The engine will initialize the V8 evolutionary system and begin evaluating agents.

⸻

🔐 API Key Security

This repository does not require the author’s API key.

Every user should provide their own Gemini API key.

Recommended workflow:
User
 │
 ├── Creates their own Gemini API key
 │
 ├── Sets GEMINI_API_KEY
 │
 └── Runs AI-Evolution-Engine
          │
          ▼
      Gemini API
      For environments such as Kaggle, use the platform’s secret-management system instead of hardcoding API keys.

⸻

🧪 Example Test

The V8 engine successfully completed a development mini-evolution test:
====================================
🧬 V8 MINI EVOLUTION TEST
====================================

Score: 3/3
Accuracy: 100.00%

Categories:
{
    "planning": [1, 1],
    "coding": [2, 2]
}
This demonstrates that the evaluation and scoring pipeline can successfully execute the test workload.

Results from larger experiments may vary depending on the model, task set, configuration, API limits, and random seed.

⸻

📊 Example Evolution

A typical experiment can be configured with parameters such as:
Model
Seed
Generations
Population Size
Tasks per Generation
Elite Count
Example:
Model: Gemini
Generations: 2
Population: 3
Tasks / Generation: 5
Elite Count: 1
The engine evaluates agents, selects the strongest performer, protects the elite, and creates the next generation.

⸻

⚠️ API Rate Limits

AI-Evolution-Engine uses the Gemini API and is therefore subject to the limits of the user’s API plan.

Large populations and many generations can consume API quota quickly.

If you encounter:429 RESOURCE_EXHAUSTED
the API quota or rate limit has been reached.

Possible solutions include:

* Reduce population size.
* Reduce tasks per generation.
* Reduce the number of generations.
* Wait for the rate-limit window to reset.
* Use an API plan with higher limits.

This error generally indicates an API quota limitation rather than a failure of the evolution engine.

⸻

🔬 Research & Experimentation

AI-Evolution-Engine is designed as an experimental platform for exploring AI-agent evolution.

It can be used to investigate questions such as:

* Can AI agents improve through iterative selection?
* Which strategies consistently produce stronger agents?
* How does population diversity affect evolution?
* Does elite protection improve evolutionary stability?
* How does performance change between generations?
* Can specialized agent behaviors emerge?
* Which evaluation methods best measure agent improvement?

The project does not assume that evolution automatically makes an AI system better.

Instead, performance is measured experimentally.

⸻

🧬 Evolution Philosophy

The project follows a simple principle:

Agents should be evaluated by measurable performance rather than assumptions about which strategy is better.

The evolutionary engine uses task performance as the primary signal for selection.

This provides a foundation for reproducible experiments in AI-agent evolution.

⸻

🛠️ Future Development

Potential future improvements include:

* Larger agent populations
* Advanced mutation strategies
* Agent crossover
* Multi-model evolution
* Persistent agent genomes
* Longitudinal performance tracking
* Advanced benchmarks
* Agent diversity metrics
* Automatic experiment reports
* Evolution visualization
* Parallel agent evaluation
* Improved API rate-limit handling
* Reproducible experiment configuration files

⸻

🤝 Contributing

Contributions, experiments, ideas, benchmarks, and improvements are welcome.

You can:

1. Fork the repository.
2. Create a feature branch.
3. Implement your improvement.
4. Run the available tests.
5. Submit a pull request.

⸻

📜 License

This project is distributed under the license included in this repository.
See:LICENSE
👤 Author

Mohammed Ghabban

GitHub:

Mhmda1998

⸻

🌟 Project

AI-Evolution-Engine

Evaluate. Select. Protect. Evolve. Repeat.

An experimental platform for exploring what AI agents can become through measurable evolutionary processes.

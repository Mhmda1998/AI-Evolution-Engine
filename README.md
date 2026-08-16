🧬 AI Evolution Engine

V8 Real Agent Evolution Engine

AI Evolution Engine is an experimental framework for evaluating and evolving AI agents through iterative generations.

Instead of treating an AI agent as a static program, the engine creates populations of agents, evaluates them on defined tasks, measures their performance, selects high-performing agents, protects elite agents, and generates new candidate agents for subsequent generations.

Core Evolution Loop

Evaluate → Select → Protect → Evolve → Evaluate Again

⸻

🚀 Key Features

* AI agent population management
* Automated task evaluation
* Performance scoring
* Elite agent selection
* Elite protection across generations
* Child-agent generation
* Multi-generation evolution
* Performance tracking
* Gemini-powered AI backend
* User-provided API key support
* Configurable random seeds
* Reproducible experimental configurations
* Modular V7 and V8 evolution engines

⸻

🧬 How Evolution Works

The evolution process follows this cycle:

Initial Population
↓
Task Evaluation
↓
Performance Scoring
↓
Elite Selection
↓
Elite Protection + Child Generation
↓
Next Generation
↓
Re-Evaluation
↓
Repeat

Each generation evaluates the current population and uses measured performance to determine which agents should survive and which new agents should be created.

⸻

🧠 V8 Architecture

The V8 engine is organized around several core concepts.

Population

Each generation contains multiple candidate agents competing on the same evaluation tasks.

Evaluation

Every agent is evaluated against a predefined collection of tasks.

Scoring

The engine calculates performance scores based on task results.

Elite Selection

The strongest-performing agents are selected as elites.

Elite Protection

Elite agents are preserved when the next generation is created.

Child Generation

New candidate agents are generated from successful evolutionary states.

Generational Evolution

The process repeats across multiple generations, allowing the population to explore different agent strategies.

⸻

📁 Project Structure

AI-Evolution-Engine/

├── V7_Elite_Evolution.py
├── V8_Real_Agent_Evolution.py
├── run_v8.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

V8_Real_Agent_Evolution.py

The main V8 engine for real-agent evolutionary experiments.

run_v8.py

The primary entry point used to launch the V8 evolution engine.

V7_Elite_Evolution.py

The previous experimental evolution engine containing the V7 elite-evolution architecture.

requirements.txt

Python dependencies required by the project.

README.md

Project documentation and usage instructions.

⸻

⚡ Quick Start

1. Clone the Repository

git clone https://github.com/Mhmda1998/AI-Evolution-Engine.git

cd AI-Evolution-Engine

2. Install Dependencies

pip install -r requirements.txt

3. Configure Gemini API

Create your own Gemini API key and expose it through the environment.

Linux / macOS:

export GEMINI_API_KEY=“YOUR_GEMINI_API_KEY”

Windows:

setx GEMINI_API_KEY “YOUR_GEMINI_API_KEY”

IMPORTANT:

Never hard-code your API key inside the source code or commit it to GitHub.

⸻

▶️ Run V8

After configuring your API key:

python run_v8.py

The engine will initialize the V8 evolutionary system and begin evaluating agents.

⸻

🔐 API Key Security

This repository does not require the author’s API key.

Every user should provide their own Gemini API key.

Recommended workflow:

User
↓
Create a personal Gemini API key
↓
Set GEMINI_API_KEY
↓
Run AI Evolution Engine
↓
Gemini API

For environments such as Kaggle, use the platform’s secret-management system instead of hard-coding API keys.

⸻

🧪 Example Mini Evolution Test

The V8 engine successfully completed a miniature evolution test.

Result:

Score: 3/3
Accuracy: 100.00%

Categories:

Planning: 1/1
Coding: 2/2

This demonstrates that the evaluation and scoring pipeline can successfully execute the test workload.

Larger experiments may produce different results depending on:

* Model
* Task dataset
* Population size
* Number of generations
* API limits
* Random seed
* Evaluation configuration

⸻

📊 Example Evolution Configuration

A typical experiment can be configured with parameters such as:

Model: Gemini
Generations: 2
Population: 3
Tasks per Generation: 5
Elite Count: 1
Seed: 20260816

The engine evaluates agents, selects the strongest performer, protects the elite, generates the next generation, and repeats the evaluation process.

⸻

⚠️ API Rate Limits

AI Evolution Engine uses the Gemini API and is therefore subject to the API limits of the user’s account.

Large populations and many generations can consume API quota quickly.

If you encounter:

429 RESOURCE_EXHAUSTED

this generally means that the API quota or rate limit has been reached.

Possible solutions include:

* Reduce population size.
* Reduce tasks per generation.
* Reduce the number of generations.
* Wait for the rate-limit window to reset.
* Use an API plan with higher limits.

A 429 RESOURCE_EXHAUSTED error does not necessarily indicate a failure in the evolution engine itself. It can simply indicate that the configured API quota has been exhausted.

⸻

🔬 Research & Experimentation

AI Evolution Engine is designed as an experimental platform for exploring the evolution of AI agents.

It can be used to investigate questions such as:

* Can AI agents improve through iterative selection?
* Which strategies consistently produce stronger agents?
* How does population diversity affect evolution?
* Does elite protection improve evolutionary stability?
* How does performance change between generations?
* Can specialized agent behaviors emerge?
* What evaluation strategies provide reliable measurements of agent improvement?
* How does population size influence evolutionary search?
* Can evolutionary selection discover better agent strategies?

The project does not assume that evolution automatically makes an AI system better.

Instead, improvement is measured empirically through task performance.

⸻

🧬 Evolution Philosophy

The project follows a simple principle:

Agents should be evaluated based on measurable performance rather than assumptions about which strategy is best.

The evolutionary engine uses task performance as the primary signal for selection.

This provides a foundation for reproducible experiments in AI-agent evolution.

⸻

🧪 Reproducibility

Experiments can use configurable random seeds to make evolutionary runs easier to reproduce.

Example:

Seed: 20260816

Reproducibility may still depend on external factors such as:

* Model version
* API behavior
* API limits
* Task configuration
* Backend responses
* Software dependencies

Therefore, identical seeds do not necessarily guarantee identical results when external model behavior changes.

⸻

🛠️ Future Development

Potential future improvements include:

* Larger agent populations
* Advanced mutation strategies
* Agent crossover
* Multi-model evolution
* Persistent agent genomes
* Long-term performance tracking
* Advanced evaluation benchmarks
* Agent diversity metrics
* Automatic experiment reports
* Evolution visualization
* Parallel agent evaluation
* Improved API rate-limit handling
* Reproducible experiment configuration files
* Persistent evolutionary history
* Agent lineage tracking
* Benchmark comparison across generations

⸻

🤝 Contributing

Contributions, experiments, ideas, benchmarks, and improvements are welcome.

You can:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Run the available tests.
5. Commit your changes.
6. Open a Pull Request.

Example:

git checkout -b feature/my-improvement

git add .

git commit -m “Add evolutionary improvement”

git push origin feature/my-improvement

Then open a Pull Request on GitHub.

⸻

📜 License

This project is distributed under the license included in this repository.

See:

LICENSE

⸻

👤 Author

Mohammed Ghabban

GitHub: Mhmda1998

⸻

🌟 AI Evolution Engine

Evaluate. Select. Protect. Evolve. Repeat.

An experimental platform for exploring what AI agents can become through measurable, iterative evolutionary processes.

⸻

🧬 Project Vision

AI Evolution Engine explores a different approach to AI-agent development.

Instead of manually creating a single agent and continuously modifying its code, the system experiments with populations of agents and allows measured performance to guide evolutionary selection.

The long-term goal is to provide a research-oriented foundation for studying:

Agent → Evaluation → Selection → Evolution → Improvement

The project is experimental and intended to evolve alongside the research and engineering ideas behind it.

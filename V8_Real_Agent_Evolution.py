"""
V8 Real Agent Evolution
=======================

Real AI-agent evolutionary experiment using Google's Gemini API.

Pipeline:

    Benchmark Tasks
          ↓
    Real Gemini Agents
          ↓
    Evaluation
          ↓
    Score
          ↓
    Elite Selection
          ↓
    Prompt Mutation
          ↓
    New Generation

The API key is NEVER stored in this source file.

Set:

    GEMINI_API_KEY

before running the experiment.
"""

import os
import random
import re
import statistics
import time

from dataclasses import dataclass
from typing import Callable, List, Dict, Any

from google import genai


# ================================================================
# CONFIGURATION
# ================================================================

SEED = 20260816

GENERATIONS = 4
POPULATION_SIZE = 6
TASKS_PER_GENERATION = 50
ELITE_COUNT = 2

# Use a current Gemini model available to the API key.
MODEL_NAME = "gemini-3-flash-preview"

# Small delay between requests.
REQUEST_DELAY = 0.2

random.seed(SEED)


# ================================================================
# TASK
# ================================================================

@dataclass
class Task:
    question: str
    answer: str
    category: str


# ================================================================
# GEMINI BACKEND
# ================================================================

class GeminiBackend:
    """
    Real Gemini API backend.

    The API key is loaded from:

        GEMINI_API_KEY

    The key is never printed or stored in this source file.
    """

    def __init__(self, model_name: str):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. "
                "Set it as an environment variable or "
                "Kaggle Secret before running."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = model_name

    def generate(
        self,
        system_prompt: str,
        question: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=(
                system_prompt
                + "\n\n"
                + "Task:\n"
                + question
                + "\n\n"
                + "Return only the final answer."
            ),
        )

        text = getattr(
            response,
            "text",
            None
        )

        if text is None:
            return ""

        return str(text).strip()


# ================================================================
# REAL AGENT
# ================================================================

class RealAgent:

    def __init__(
        self,
        name: str,
        backend: GeminiBackend,
        system_prompt: str,
    ):

        self.name = name
        self.backend = backend
        self.system_prompt = system_prompt

    def solve(
        self,
        question: str,
    ) -> str:

        return self.backend.generate(
            self.system_prompt,
            question,
        )


# ================================================================
# BENCHMARK
# ================================================================

def build_benchmark(
    seed: int,
    count: int,
) -> List[Task]:

    rng = random.Random(seed)

    tasks = []

    # ------------------------------------------------------------
    # LOGIC
    # ------------------------------------------------------------

    logic_tasks = [

        (
            "If all A are B and all B are C, "
            "are all A necessarily C?",
            "yes",
            "logic",
        ),

        (
            "If no A is B, can something be both A and B?",
            "no",
            "logic",
        ),

        (
            "If some A is B and every B is C, "
            "must some A be C?",
            "yes",
            "logic",
        ),

        (
            "If some A are B and some B are C, "
            "must some A be C?",
            "no",
            "logic",
        ),
    ]

    # ------------------------------------------------------------
    # CODING
    # ------------------------------------------------------------

    coding_tasks = [

        (
            "What Python type stores key-value pairs?",
            "dict",
            "coding",
        ),

        (
            "What Python function returns the length of a list?",
            "len",
            "coding",
        ),

        (
            "What keyword defines a Python function?",
            "def",
            "coding",
        ),

        (
            "What keyword returns a value from a function?",
            "return",
            "coding",
        ),
    ]

    # ------------------------------------------------------------
    # PLANNING
    # ------------------------------------------------------------

    planning_tasks = [

        (
            "Should a critical resource normally be secured "
            "before an optional goal?",
            "yes",
            "planning",
        ),

        (
            "Should an urgent safety problem normally be "
            "handled before a non-urgent task?",
            "yes",
            "planning",
        ),

        (
            "If a required dependency is missing, should it "
            "normally be resolved before the dependent task?",
            "yes",
            "planning",
        ),
    ]

    all_templates = (
        logic_tasks
        + coding_tasks
        + planning_tasks
    )

    for _ in range(count):

        question, answer, category = rng.choice(
            all_templates
        )

        tasks.append(
            Task(
                question=question,
                answer=answer,
                category=category,
            )
        )

    return tasks


# ================================================================
# ANSWER NORMALIZATION
# ================================================================

def normalize_answer(
    value: Any,
) -> str:

    if value is None:
        return ""

    text = str(value).strip().lower()

    # Remove common Markdown/code formatting.
    text = re.sub(
        r"[`'\"]",
        "",
        text,
    )

    text = text.rstrip(".")

    # Extract very short final answers when possible.
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) == 1:
        text = lines[0]

    return text.strip()


# ================================================================
# EVALUATOR
# ================================================================

def evaluate_answer(
    prediction: str,
    expected: str,
) -> bool:

    predicted = normalize_answer(
        prediction
    )

    expected = normalize_answer(
        expected
    )

    # Exact match.
    if predicted == expected:
        return True

    # Handle responses such as:
    # "The answer is yes"
    # "Answer: dict"
    patterns = [
        rf"\b{re.escape(expected)}\b",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            predicted,
        ):

            # Only accept if response is reasonably short.
            if len(predicted) <= 120:
                return True

    return False


# ================================================================
# AGENT EVALUATION
# ================================================================

def evaluate_agent(
    agent: RealAgent,
    tasks: List[Task],
) -> Dict[str, Any]:

    correct = 0

    category_stats = {}

    for index, task in enumerate(tasks, start=1):

        try:

            prediction = agent.solve(
                task.question
            )

        except Exception as exc:

            print(
                f"⚠️ {agent.name} request error: {exc}"
            )

            prediction = ""

        success = evaluate_answer(
            prediction,
            task.answer,
        )

        if task.category not in category_stats:

            category_stats[
                task.category
            ] = [
                0,
                0,
            ]

        category_stats[
            task.category
        ][1] += 1

        if success:

            correct += 1

            category_stats[
                task.category
            ][0] += 1

        time.sleep(
            REQUEST_DELAY
        )

    accuracy = (
        correct / len(tasks) * 100
        if tasks
        else 0.0
    )

    return {

        "score": correct,

        "accuracy": accuracy,

        "categories": category_stats,
    }


# ================================================================
# MUTATIONS
# ================================================================

MUTATIONS = [

    (
        "concise_reasoning",
        (
            "Reason carefully internally. "
            "Return the final answer clearly "
            "and concisely."
        ),
    ),

    (
        "step_by_step",
        (
            "Analyze the task systematically "
            "before deciding on the final answer."
        ),
    ),

    (
        "verification",
        (
            "Check your reasoning and verify "
            "the final answer before responding."
        ),
    ),

    (
        "structured_reasoning",
        (
            "Use a structured reasoning process. "
            "Then provide the final answer."
        ),
    ),
]


def mutate_agent(
    parent: RealAgent,
    mutation_name: str,
    mutation_prompt: str,
    child_id: int,
) -> RealAgent:

    new_prompt = (
        parent.system_prompt
        + "\n\n"
        + mutation_prompt
    )

    return RealAgent(
        name=f"V8-Child-{child_id}",
        backend=parent.backend,
        system_prompt=new_prompt,
    )


# ================================================================
# AGENT RECORD
# ================================================================

@dataclass
class AgentRecord:

    agent: RealAgent

    score: float = 0.0

    elite: bool = False

    parent: str = ""

    mutation: str = ""


# ================================================================
# EVOLUTION ENGINE
# ================================================================

class EvolutionEngine:

    def __init__(
        self,
        initial_agents: List[RealAgent],
    ):

        self.population = [

            AgentRecord(
                agent=agent
            )

            for agent in initial_agents
        ]

        self.history = []

    def evaluate_generation(
        self,
        generation: int,
        tasks: List[Task],
    ):

        print()

        print("=" * 70)

        print(
            f"🧬 GENERATION {generation}"
        )

        print("=" * 70)

        for record in self.population:

            print(
                f"🤖 Evaluating "
                f"{record.agent.name}..."
            )

            result = evaluate_agent(
                record.agent,
                tasks,
            )

            record.score = result[
                "accuracy"
            ]

            print(
                f"   → {record.score:.2f}%"
            )

            self.history.append({

                "generation": generation,

                "agent": record.agent.name,

                "score": record.score,

                "parent": record.parent,

                "mutation": record.mutation,
            })

        self.population.sort(
            key=lambda record: record.score,
            reverse=True,
        )

        print()

        print(
            f"🏆 Generation {generation} best: "
            f"{self.population[0].agent.name} "
            f"→ "
            f"{self.population[0].score:.2f}%"
        )

    def evolve(
        self,
        generations: int,
        benchmark_factory: Callable,
    ):

        for generation in range(
            1,
            generations + 1,
        ):

            tasks = benchmark_factory(
                SEED + generation,
                TASKS_PER_GENERATION,
            )

            self.evaluate_generation(
                generation,
                tasks,
            )

            # ----------------------------------------------------
            # Final generation
            # ----------------------------------------------------

            if generation == generations:

                break

            # ----------------------------------------------------
            # Protect elites
            # ----------------------------------------------------

            elites = [

                AgentRecord(
                    agent=record.agent,
                    score=record.score,
                    elite=True,
                    parent=record.parent,
                    mutation=record.mutation,
                )

                for record in self.population[
                    :ELITE_COUNT
                ]
            ]

            next_population = elites.copy()

            child_id = 1

            # ----------------------------------------------------
            # Create children
            # ----------------------------------------------------

            while len(
                next_population
            ) < POPULATION_SIZE:

                parent = random.choice(
                    elites
                )

                mutation_name, mutation_prompt = (
                    random.choice(
                        MUTATIONS
                    )
                )

                child = mutate_agent(
                    parent.agent,
                    mutation_name,
                    mutation_prompt,
                    child_id,
                )

                next_population.append(

                    AgentRecord(

                        agent=child,

                        parent=parent.agent.name,

                        mutation=mutation_name,
                    )
                )

                child_id += 1

            self.population = (
                next_population
            )

            print()

            print(
                f"🧬 Generation "
                f"{generation + 1} created."
            )

            print(
                "🛡️ Elites protected."
            )

        self.population.sort(
            key=lambda record: record.score,
            reverse=True,
        )

        return self.population[0]


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 70)

    print(
        "🧬 V8 REAL AGENT EVOLUTION ENGINE"
    )

    print("=" * 70)

    print(
        f"Model: {MODEL_NAME}"
    )

    print(
        f"Seed: {SEED}"
    )

    print(
        f"Generations: {GENERATIONS}"
    )

    print(
        f"Population: {POPULATION_SIZE}"
    )

    print(
        f"Tasks / generation: "
        f"{TASKS_PER_GENERATION}"
    )

    print(
        f"Elite count: {ELITE_COUNT}"
    )

    print()

    # ------------------------------------------------------------
    # Real Gemini backend
    # ------------------------------------------------------------

    backend = GeminiBackend(
        model_name=MODEL_NAME
    )

    # ------------------------------------------------------------
    # Initial population
    # ------------------------------------------------------------

    agents = []

    base_prompt = (
        "You are an AI agent participating in "
        "an experimental evaluation benchmark. "
        "Analyze each task carefully and provide "
        "the most accurate answer possible."
    )

    for name in [

        "V8-Agent-A",
        "V8-Agent-B",
        "V8-Agent-C",
        "V8-Agent-D",
        "V8-Agent-E",
        "V8-Agent-F",

    ]:

        agents.append(

            RealAgent(

                name=name,

                backend=backend,

                system_prompt=base_prompt,
            )
        )

    # ------------------------------------------------------------
    # Evolution
    # ------------------------------------------------------------

    engine = EvolutionEngine(
        initial_agents=agents
    )

    best = engine.evolve(
        generations=GENERATIONS,
        benchmark_factory=build_benchmark,
    )

    # ------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------

    print()

    print("=" * 70)

    print(
        "👑 FINAL V8 ELITE"
    )

    print("=" * 70)

    print(
        f"Model: "
        f"{best.agent.name}"
    )

    print(
        f"Score: "
        f"{best.score:.2f}%"
    )

    print(
        f"Parent: "
        f"{best.parent or 'None'}"
    )

    print(
        f"Mutation: "
        f"{best.mutation or 'None'}"
    )

    print()

    print(
        "📊 EVOLUTION HISTORY"
    )

    print("-" * 70)

    for item in engine.history:

        print(
            f"G{item['generation']} | "
            f"{item['agent']:<20} | "
            f"{item['score']:.2f}%"
        )

    print()

    print(
        "✅ V8 REAL AGENT EVOLUTION COMPLETE"
    )


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":

    main()

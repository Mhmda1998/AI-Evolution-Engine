"""
V8 Real Agent Evolution Engine
==============================

An experimental evolutionary framework for real AI agents.

Pipeline:

    Benchmark
        ↓
    Real LLM Agent
        ↓
    Objective Evaluation
        ↓
    Fitness Score
        ↓
    Elite Selection
        ↓
    Prompt Mutation
        ↓
    New Generation
        ↓
    Final Elite

Backend:
    Google Gemini API

The API key is NEVER stored in this repository.
Users provide their own GEMINI_API_KEY environment variable.
"""

import os
import random
import re
import statistics
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

from google import genai
from google.genai import types


# ================================================================
# CONFIGURATION
# ================================================================

SEED = 20260816

GENERATIONS = 4
POPULATION_SIZE = 6
ELITE_COUNT = 2

TASKS_PER_GENERATION = 30

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

random.seed(SEED)


# ================================================================
# API CONFIGURATION
# ================================================================

def create_gemini_client():
    """
    Create a Gemini client using GEMINI_API_KEY.

    The key must be supplied by the user through
    an environment variable.

    Never hard-code an API key in this file.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "\n"
            "GEMINI_API_KEY was not found.\n\n"
            "Set your Gemini API key before running the engine.\n"
            "Example:\n\n"
            "Linux/macOS:\n"
            "    export GEMINI_API_KEY='YOUR_KEY'\n\n"
            "Windows PowerShell:\n"
            "    $env:GEMINI_API_KEY='YOUR_KEY'\n"
        )

    return genai.Client(api_key=api_key)


# ================================================================
# TASK
# ================================================================

@dataclass
class Task:
    question: str
    answer: str
    category: str


# ================================================================
# REAL AGENT
# ================================================================

class RealAgent:
    """
    Real AI agent backed by Gemini.

    Each evolutionary child receives a mutated system prompt.
    """

    def __init__(
        self,
        name: str,
        client,
        system_prompt: str,
        model_name: str = MODEL_NAME,
    ):
        self.name = name
        self.client = client
        self.system_prompt = system_prompt
        self.model_name = model_name

    def solve(self, question: str) -> str:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.2,
                max_output_tokens=100,
            ),
        )

        if not response.text:
            return ""

        return response.text.strip()


# ================================================================
# BENCHMARK
# ================================================================

def build_benchmark(
    seed: int,
    count: int,
) -> List[Task]:

    rng = random.Random(seed)

    tasks: List[Task] = []

    logic_tasks = [
        (
            "If all A are B and all B are C, are all A necessarily C?",
            "yes",
            "logic",
        ),
        (
            "If no A is B, can something be both A and B?",
            "no",
            "logic",
        ),
        (
            "If some A is B and every B is C, must some A be C?",
            "yes",
            "logic",
        ),
        (
            "If some A are B and some B are C, must some A be C?",
            "no",
            "logic",
        ),
        (
            "If all A are B and x is A, must x be B?",
            "yes",
            "logic",
        ),
    ]

    math_tasks = []

    for _ in range(10):
        a = rng.randint(10, 99)
        b = rng.randint(2, 30)

        math_tasks.append(
            (
                f"What is {a} × {b}?",
                str(a * b),
                "math",
            )
        )

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
        (
            "What Python type stores an ordered mutable collection?",
            "list",
            "coding",
        ),
        (
            "What keyword exits a loop immediately?",
            "break",
            "coding",
        ),
    ]

    planning_tasks = [
        (
            "Should a critical resource normally be secured before an optional goal?",
            "yes",
            "planning",
        ),
        (
            "Should an urgent safety problem normally be handled before a non-urgent task?",
            "yes",
            "planning",
        ),
        (
            "If a required dependency is missing, should it normally be resolved before the dependent task?",
            "yes",
            "planning",
        ),
        (
            "If resources are limited, should essential needs normally have priority?",
            "yes",
            "planning",
        ),
    ]

    reasoning_tasks = []

    for _ in range(10):
        start = rng.randint(20, 200)
        removed = rng.randint(1, start)

        reasoning_tasks.append(
            (
                f"A store has {start} products and sells "
                f"{removed}. How many remain?",
                str(start - removed),
                "reasoning",
            )
        )

    all_templates = (
        logic_tasks
        + math_tasks
        + coding_tasks
        + planning_tasks
        + reasoning_tasks
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

def normalize_answer(value: Any) -> str:

    if value is None:
        return ""

    text = str(value).strip().lower()

    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )

    text = text.strip()

    text = re.sub(
        r"^[`'\" ]+|[`'\" .,!?]+$",
        "",
        text,
    )

    # Remove common explanatory prefixes.
    prefixes = [
        "answer:",
        "final answer:",
        "the answer is:",
        "final:",
    ]

    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()

    # For short benchmark answers, use the first line.
    if "\n" in text:
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if lines:
            text = lines[-1]

    text = text.strip("`'\" .,!?")

    return text


# ================================================================
# OBJECTIVE EVALUATOR
# ================================================================

def evaluate_answer(
    prediction: str,
    expected: str,
) -> bool:

    predicted = normalize_answer(prediction)
    expected = normalize_answer(expected)

    if predicted == expected:
        return True

    # Handle simple responses such as:
    # "Yes, because..."
    if expected in {
        "yes",
        "no",
    }:

        first_word = predicted.split()[0] if predicted else ""

        return first_word == expected

    # Handle numeric answers embedded in a short explanation.
    if expected.isdigit():

        numbers = re.findall(
            r"\b\d+\b",
            predicted,
        )

        return expected in numbers

    return False


# ================================================================
# AGENT EVALUATION
# ================================================================

def evaluate_agent(
    agent: RealAgent,
    tasks: List[Task],
) -> Dict[str, Any]:

    correct = 0

    category_stats: Dict[
        str,
        List[int]
    ] = {}

    for index, task in enumerate(tasks, 1):

        try:

            prediction = agent.solve(
                task.question
            )

        except Exception as exc:

            print(
                f"⚠️ {agent.name} API error "
                f"on task {index}: {exc}"
            )

            prediction = ""

        success = evaluate_answer(
            prediction,
            task.answer,
        )

        if task.category not in category_stats:

            category_stats[
                task.category
            ] = [0, 0]

        category_stats[
            task.category
        ][1] += 1

        if success:

            correct += 1

            category_stats[
                task.category
            ][0] += 1

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

MUTATIONS: List[
    Tuple[str, str]
] = [

    (
        "concise_reasoning",
        (
            "Solve carefully. "
            "Return the final answer clearly and concisely."
        ),
    ),

    (
        "verification",
        (
            "Before returning your answer, "
            "verify it carefully."
        ),
    ),

    (
        "structured_reasoning",
        (
            "Analyze the task systematically. "
            "Check the relevant facts and then provide "
            "the most accurate final answer."
        ),
    ),

    (
        "precision",
        (
            "Prioritize factual correctness and precision. "
            "Avoid unnecessary assumptions."
        ),
    ),

    (
        "self_check",
        (
            "Perform an internal self-check before giving "
            "your final answer."
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
        client=parent.client,
        system_prompt=new_prompt,
        model_name=parent.model_name,
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
        client,
    ):

        self.population = [
            AgentRecord(agent=a)
            for a in initial_agents
        ]

        self.client = client

        self.history: List[Dict[str, Any]] = []

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

        generation_results = []

        for record in self.population:

            result = evaluate_agent(
                record.agent,
                tasks,
            )

            record.score = result[
                "accuracy"
            ]

            generation_results.append(
                {
                    "name": record.agent.name,
                    "score": record.score,
                    "parent": record.parent,
                    "mutation": record.mutation,
                    "categories": result[
                        "categories"
                    ],
                }
            )

            print(
                f"{record.agent.name:<25}"
                f" → {record.score:.2f}%"
            )

        self.population.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        self.history.append(
            {
                "generation": generation,
                "results": generation_results,
            }
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
        benchmark_factory,
    ) -> AgentRecord:

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

            if generation == generations:
                break

            elites = [
                AgentRecord(
                    agent=r.agent,
                    score=r.score,
                    elite=True,
                    parent=r.parent,
                    mutation=r.mutation,
                )
                for r in self.population[
                    :ELITE_COUNT
                ]
            ]

            next_population = elites.copy()

            child_id = 1

            while len(next_population) < POPULATION_SIZE:

                parent = random.choice(
                    elites
                )

                mutation_name, mutation_prompt = (
                    random.choice(MUTATIONS)
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

            self.population = next_population

            print()
            print(
                f"🧬 Generation "
                f"{generation + 1} created."
            )

            print(
                "🛡️ Elites protected."
            )

        self.population.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        return self.population[0]


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 70)
    print("🧬 V8 REAL AGENT EVOLUTION ENGINE")
    print("=" * 70)

    print(
        f"🤖 Gemini model: {MODEL_NAME}"
    )

    print(
        f"🧬 Generations: {GENERATIONS}"
    )

    print(
        f"👥 Population: {POPULATION_SIZE}"
    )

    print(
        f"🛡️ Elite count: {ELITE_COUNT}"
    )

    print(
        f"📋 Tasks/generation: {TASKS_PER_GENERATION}"
    )

    print()

    # ------------------------------------------------------------
    # Gemini connection
    # ------------------------------------------------------------

    try:

        client = create_gemini_client()

    except Exception as exc:

        print(
            f"❌ Configuration error:\n{exc}"
        )

        return

    print(
        "✅ Gemini API client initialized."
    )

    # ------------------------------------------------------------
    # Initial population
    # ------------------------------------------------------------

    base_prompt = (
        "You are an AI agent being evaluated on a benchmark. "
        "Solve each task accurately. "
        "Follow the user's question carefully. "
        "Return the most accurate answer."
    )

    agents: List[RealAgent] = []

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
                client=client,
                system_prompt=base_prompt,
                model_name=MODEL_NAME,
            )
        )

    # ------------------------------------------------------------
    # Evolution
    # ------------------------------------------------------------

    engine = EvolutionEngine(
        initial_agents=agents,
        client=client,
    )

    best = engine.evolve(
        generations=GENERATIONS,
        benchmark_factory=build_benchmark,
    )

    # ------------------------------------------------------------
    # Final result
    # ------------------------------------------------------------

    print()
    print("=" * 70)
    print("👑 FINAL V8 ELITE")
    print("=" * 70)

    print(
        f"Model: {best.agent.name}"
    )

    print(
        f"Score: {best.score:.2f}%"
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
        "🧬 Evolution history:"
    )

    for generation in engine.history:

        scores = [
            item["score"]
            for item in generation["results"]
        ]

        print(
            f"Generation "
            f"{generation['generation']}: "
            f"best={max(scores):.2f}% | "
            f"mean={statistics.mean(scores):.2f}%"
        )

    print()
    print(
        "🔐 API key was supplied externally."
    )

    print(
        "🚫 No API key is stored by this program."
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

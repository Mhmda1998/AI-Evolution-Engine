"""
V8 Real Agent Evolution
=======================

Experimental evolutionary framework for real AI agents.

Pipeline:
    Task
      ↓
    Real Agent
      ↓
    Evaluator
      ↓
    Score
      ↓
    Elite Selection
      ↓
    Mutation
      ↓
    New Agent

This version is intentionally provider-agnostic.
The AI backend is supplied through the RealAgent class.
"""


import random
import re
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any


# ================================================================
# CONFIGURATION
# ================================================================

SEED = 20260816
random.seed(SEED)

GENERATIONS = 4
POPULATION_SIZE = 6
TASKS_PER_GENERATION = 50
ELITE_COUNT = 2


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
    Adapter for a real AI model.

    Replace the `backend` function with a real
    LLM/API call.

    The evolutionary engine itself does not depend
    on a specific provider.
    """

    def __init__(
        self,
        name: str,
        backend: Callable[[str, str], str],
        system_prompt: str,
    ):
        self.name = name
        self.backend = backend
        self.system_prompt = system_prompt

    def solve(self, question: str) -> str:
        return self.backend(
            self.system_prompt,
            question
        )


# ================================================================
# BENCHMARK
# ================================================================

def build_benchmark(
    seed: int,
    count: int
) -> List[Task]:

    rng = random.Random(seed)

    tasks = []

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
    ]

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

def normalize_answer(value: Any) -> str:

    if value is None:
        return ""

    text = str(value).strip().lower()

    text = re.sub(
        r"^[`'\"]+|[`'\"]+$",
        "",
        text
    )

    text = text.rstrip(".")

    return text.strip()


# ================================================================
# EVALUATOR
# ================================================================

def evaluate_answer(
    prediction: str,
    expected: str
) -> bool:

    return (
        normalize_answer(prediction)
        ==
        normalize_answer(expected)
    )


# ================================================================
# AGENT EVALUATION
# ================================================================

def evaluate_agent(
    agent: RealAgent,
    tasks: List[Task]
) -> Dict[str, Any]:

    correct = 0

    category_stats = {}

    for task in tasks:

        try:
            prediction = agent.solve(
                task.question
            )

        except Exception as exc:

            print(
                f"⚠️ Agent error: {exc}"
            )

            prediction = ""

        success = evaluate_answer(
            prediction,
            task.answer
        )

        if task.category not in category_stats:
            category_stats[task.category] = [
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

    accuracy = (
        correct / len(tasks) * 100
        if tasks
        else 0
    )

    return {
        "score": correct,
        "accuracy": accuracy,
        "categories": category_stats,
    }


# ================================================================
# MUTATION
# ================================================================

MUTATIONS = [
    (
        "concise_reasoning",
        "Answer carefully and concisely. "
        "Give the final answer clearly."
    ),
    (
        "step_by_step",
        "Reason step by step before giving "
        "the final answer."
    ),
    (
        "verification",
        "Check your answer before returning "
        "the final response."
    ),
    (
        "structured_reasoning",
        "Analyze the task systematically and "
        "then provide the final answer."
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
# EVOLUTION ENGINE
# ================================================================

@dataclass
class AgentRecord:

    agent: RealAgent
    score: float = 0.0
    elite: bool = False
    parent: str = ""
    mutation: str = ""


class EvolutionEngine:

    def __init__(
        self,
        initial_agents: List[RealAgent],
    ):

        self.population = [
            AgentRecord(agent=a)
            for a in initial_agents
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

            result = evaluate_agent(
                record.agent,
                tasks,
            )

            record.score = result[
                "accuracy"
            ]

            print(
                f"{record.agent.name:<25}"
                f" → {record.score:.2f}%"
            )

        self.population.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        print()
        print(
            f"🏆 Generation {generation} "
            f"best: "
            f"{self.population[0].agent.name} "
            f"→ "
            f"{self.population[0].score:.2f}%"
        )

    def evolve(
        self,
        generations: int,
        benchmark_factory,
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

        return self.population[0]


# ================================================================
# DEMO BACKEND
# ================================================================

def demo_backend(
    system_prompt: str,
    question: str,
) -> str:

    """
    TEMPORARY BACKEND.

    This function exists only so the framework
    can be tested without an API key.

    Replace this function with a real LLM API
    backend when connecting Gemini, OpenAI, or
    another model.
    """

    answers = {

        "If all A are B and all B are C, are all A necessarily C?":
            "yes",

        "If no A is B, can something be both A and B?":
            "no",

        "If some A is B and every B is C, must some A be C?":
            "yes",

        "If some A are B and some B are C, must some A be C?":
            "no",

        "What Python type stores key-value pairs?":
            "dict",

        "What Python function returns the length of a list?":
            "len",

        "What keyword defines a Python function?":
            "def",

        "What keyword returns a value from a function?":
            "return",

        "Should a critical resource normally be secured before an optional goal?":
            "yes",

        "Should an urgent safety problem normally be handled before a non-urgent task?":
            "yes",

        "If a required dependency is missing, should it normally be resolved before the dependent task?":
            "yes",
    }

    return answers.get(
        question,
        "",
    )


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 70)
    print("🧬 V8 REAL AGENT EVOLUTION")
    print("=" * 70)

    print(
        "Experimental evolutionary framework "
        "for real AI-agent backends."
    )

    print(
        "⚠️ Current run uses a local demo backend."
    )

    print(
        "🔌 Replace demo_backend() with a real "
        "LLM API to activate a real model."
    )

    agents = []

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
                backend=demo_backend,
                system_prompt=(
                    "You are an AI agent. "
                    "Solve the user's task accurately."
                ),
            )
        )

    engine = EvolutionEngine(
        initial_agents=agents
    )

    best = engine.evolve(
        generations=GENERATIONS,
        benchmark_factory=build_benchmark,
    )

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
        "✅ V8 EVOLUTION COMPLETE"
    )


if __name__ == "__main__":
    main()

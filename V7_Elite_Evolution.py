"""
V7 Elite Evolution Engine
=========================

An experimental AI-agent evolution framework.

Pipeline:
    Population
        ↓
    Benchmark
        ↓
    Evaluation
        ↓
    Parent/Elite Selection
        ↓
    Adaptive Mutation
        ↓
    Offspring Generation
        ↓
    New Generation
        ↓
    Unseen Robustness Testing

Author: Mhmda1998
License: MIT
"""

from __future__ import annotations

import copy
import random
import statistics
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ================================================================
# CONFIGURATION
# ================================================================

SEED = 20260702

TASK_TYPES = [
    "logic",
    "math",
    "coding",
    "planning",
    "reasoning",
]

SKILLS = TASK_TYPES.copy()

TASKS_PER_BENCHMARK = 100
POPULATION_SIZE = 6
ELITE_COUNT = 2

MAX_GENERATIONS = 4

MUTATION_STEP = 0.05
MAX_SKILL = 0.99
MIN_SKILL = 0.20

ROBUSTNESS_SEEDS = list(range(1, 11))
ROBUSTNESS_TASKS_PER_SEED = 100


# ================================================================
# DATA STRUCTURES
# ================================================================

@dataclass
class Task:
    task_id: str
    task_type: str
    question: str
    answer: Any


@dataclass
class Agent:
    name: str
    skills: Dict[str, float]
    parent: Optional[str] = None
    mutation: Optional[str] = None
    generation: int = 0
    elite: bool = False

    def clone(self, name: str) -> "Agent":
        """Create a deep copy of the agent with a new name."""

        return Agent(
            name=name,
            skills=copy.deepcopy(self.skills),
            parent=self.name,
            mutation=None,
            generation=self.generation + 1,
            elite=False,
        )


# ================================================================
# TASK GENERATION
# ================================================================

def generate_tasks(
    seed: int,
    n: int = TASKS_PER_BENCHMARK,
) -> List[Task]:
    """
    Generate a deterministic benchmark.

    The benchmark contains five task categories:
        logic
        math
        coding
        planning
        reasoning
    """

    rng = random.Random(seed)

    tasks: List[Task] = []

    logic_templates = [
        (
            "If all A are B, and all B are C, are all A necessarily C?",
            "yes",
        ),
        (
            "If no A is B, can something be both A and B?",
            "no",
        ),
        (
            "If some A is B and every B is C, must some A be C?",
            "yes",
        ),
        (
            "If some A are B and some B are C, must some A be C?",
            "no",
        ),
        (
            "If all A are B and no B is C, can an A be C?",
            "no",
        ),
    ]

    coding_templates = [
        (
            "What Python function is commonly used to get the length of a list?",
            "len",
        ),
        (
            "What Python type stores key-value pairs?",
            "dict",
        ),
        (
            "What Python keyword starts a conditional statement?",
            "if",
        ),
        (
            "Which symbol is commonly used for a Python comment?",
            "#",
        ),
        (
            "What keyword is used to define a Python function?",
            "def",
        ),
        (
            "What keyword is used to return a value from a Python function?",
            "return",
        ),
        (
            "What Python type stores an ordered mutable collection?",
            "list",
        ),
        (
            "What function converts a value to an integer?",
            "int",
        ),
        (
            "What function converts a value to a string?",
            "str",
        ),
        (
            "What keyword exits a loop immediately?",
            "break",
        ),
    ]

    planning_templates = [
        (
            "If a critical resource is running low, should you secure it before optional goals?",
            "yes",
        ),
        (
            "You need food, water and shelter. Which should normally be secured first for immediate survival?",
            "water",
        ),
        (
            "If an urgent safety problem appears, should it be handled before a non-urgent task?",
            "yes",
        ),
        (
            "If a required dependency is missing, should you resolve it before the dependent task?",
            "yes",
        ),
        (
            "If a task is optional and another task is critical, which should receive priority?",
            "critical",
        ),
    ]

    # ------------------------------------------------------------
    # Logic tasks
    # ------------------------------------------------------------

    for i in range(max(1, n // 5)):
        question, answer = rng.choice(logic_templates)

        tasks.append(
            Task(
                task_id=f"logic-{i}",
                task_type="logic",
                question=question,
                answer=answer,
            )
        )

    # ------------------------------------------------------------
    # Math tasks
    # ------------------------------------------------------------

    for i in range(max(1, n // 5)):
        a = rng.randint(10, 999)
        b = rng.randint(2, 99)

        tasks.append(
            Task(
                task_id=f"math-{i}",
                task_type="math",
                question=f"What is {a} × {b}?",
                answer=a * b,
            )
        )

    # ------------------------------------------------------------
    # Coding tasks
    # ------------------------------------------------------------

    for i in range(max(1, n // 5)):
        question, answer = rng.choice(coding_templates)

        tasks.append(
            Task(
                task_id=f"coding-{i}",
                task_type="coding",
                question=question,
                answer=answer,
            )
        )

    # ------------------------------------------------------------
    # Planning tasks
    # ------------------------------------------------------------

    for i in range(max(1, n // 5)):
        question, answer = rng.choice(planning_templates)

        tasks.append(
            Task(
                task_id=f"planning-{i}",
                task_type="planning",
                question=question,
                answer=answer,
            )
        )

    # ------------------------------------------------------------
    # Reasoning tasks
    # ------------------------------------------------------------

    for i in range(max(1, n // 5)):
        start = rng.randint(20, 200)
        removed = rng.randint(1, start)

        tasks.append(
            Task(
                task_id=f"reasoning-{i}",
                task_type="reasoning",
                question=(
                    f"A store has {start} products and sells "
                    f"{removed}. How many remain?"
                ),
                answer=start - removed,
            )
        )

    # If rounding caused fewer than n tasks, fill the remainder.
    while len(tasks) < n:

        start = rng.randint(20, 200)
        removed = rng.randint(1, start)

        tasks.append(
            Task(
                task_id=f"reasoning-extra-{len(tasks)}",
                task_type="reasoning",
                question=(
                    f"A store has {start} products and sells "
                    f"{removed}. How many remain?"
                ),
                answer=start - removed,
            )
        )

    rng.shuffle(tasks)

    return tasks[:n]


# ================================================================
# ANSWER NORMALIZATION
# ================================================================

def normalize_answer(value: Any) -> str:
    """Normalize simple benchmark answers."""

    if value is None:
        return ""

    value = str(value).strip().lower()

    replacements = {
        "yes.": "yes",
        "no.": "no",
        "water.": "water",
        "critical.": "critical",
        "`dict`": "dict",
        "`len`": "len",
        "`if`": "if",
        "`#`": "#",
        "`def`": "def",
        "`return`": "return",
        "`list`": "list",
        "`int`": "int",
        "`str`": "str",
        "`break`": "break",
    }

    return replacements.get(value, value)


# ================================================================
# AGENT SIMULATION
# ================================================================

def simulate_agent(
    agent: Agent,
    task: Task,
    rng: random.Random,
) -> Any:
    """
    Simulate an agent answering a task.

    This is intentionally lightweight and deterministic under
    a supplied random generator.

    Skill values represent the agent's probability of solving
    a task from that category.
    """

    skill = task.task_type

    probability = agent.skills.get(
        skill,
        0.70,
    )

    probability = max(
        0.0,
        min(
            MAX_SKILL,
            probability,
        ),
    )

    success = rng.random() < probability

    if not success:
        return "__INCORRECT__"

    return task.answer


# ================================================================
# AGENT EVALUATION
# ================================================================

def evaluate_agent(
    agent: Agent,
    benchmark: List[Task],
    seed: int,
) -> Dict[str, Any]:
    """Evaluate one agent on a benchmark."""

    rng = random.Random(seed)

    correct = 0

    by_skill = {
        skill: [0, 0]
        for skill in SKILLS
    }

    for task in benchmark:

        prediction = simulate_agent(
            agent,
            task,
            rng,
        )

        expected = normalize_answer(
            task.answer
        )

        predicted = normalize_answer(
            prediction
        )

        is_correct = predicted == expected

        by_skill[task.task_type][1] += 1

        if is_correct:

            correct += 1

            by_skill[task.task_type][0] += 1

    accuracy = (
        correct /
        len(benchmark) *
        100
    )

    skill_scores = {}

    for skill, values in by_skill.items():

        skill_correct, skill_total = values

        if skill_total:

            skill_scores[skill] = (
                skill_correct /
                skill_total *
                100
            )

        else:

            skill_scores[skill] = 0.0

    return {
        "agent": agent.name,
        "score": correct,
        "accuracy": accuracy,
        "skills": skill_scores,
    }


# ================================================================
# INITIAL POPULATION
# ================================================================

def create_initial_population() -> List[Agent]:
    """Create the first generation."""

    return [
        Agent(
            name="Adaptive Alpha",
            generation=0,
            skills={
                "logic": 0.90,
                "math": 0.95,
                "coding": 0.80,
                "planning": 0.75,
                "reasoning": 0.90,
            },
            elite=True,
        ),

        Agent(
            name="Adaptive Beta",
            generation=0,
            skills={
                "logic": 0.95,
                "math": 0.95,
                "coding": 0.78,
                "planning": 0.70,
                "reasoning": 0.92,
            },
            elite=True,
        ),

        Agent(
            name="Adaptive Gamma",
            generation=0,
            skills={
                "logic": 0.80,
                "math": 0.85,
                "coding": 0.75,
                "planning": 0.82,
                "reasoning": 0.78,
            },
        ),

        Agent(
            name="Adaptive Delta",
            generation=0,
            skills={
                "logic": 0.84,
                "math": 0.88,
                "coding": 0.82,
                "planning": 0.78,
                "reasoning": 0.80,
            },
        ),

        Agent(
            name="Adaptive Epsilon",
            generation=0,
            skills={
                "logic": 0.82,
                "math": 0.90,
                "coding": 0.86,
                "planning": 0.72,
                "reasoning": 0.84,
            },
        ),

        Agent(
            name="Adaptive Zeta",
            generation=0,
            skills={
                "logic": 0.78,
                "math": 0.86,
                "coding": 0.80,
                "planning": 0.88,
                "reasoning": 0.82,
            },
        ),
    ]


# ================================================================
# MUTATION ANALYSIS
# ================================================================

def choose_weakest_skill(agent: Agent) -> str:
    """Find the weakest skill of an agent."""

    return min(
        agent.skills,
        key=agent.skills.get,
    )


def mutate_agent(
    parent: Agent,
    mutation: str,
    amount: float = MUTATION_STEP,
    child_name: str = "Child",
) -> Agent:
    """
    Create an offspring with a targeted mutation.

    The parent is never modified.
    """

    child = parent.clone(
        name=child_name
    )

    child.mutation = mutation

    child.skills[mutation] = min(
        MAX_SKILL,
        child.skills.get(
            mutation,
            0.70,
        ) + amount,
    )

    return child


# ================================================================
# ELITE SELECTION
# ================================================================

def select_elites(
    population: List[Agent],
    scores: Dict[str, float],
    elite_count: int,
) -> List[Agent]:
    """Select highest scoring agents."""

    ranked = sorted(
        population,
        key=lambda agent: scores[agent.name],
        reverse=True,
    )

    elites = []

    for agent in ranked[:elite_count]:

        elite = copy.deepcopy(agent)

        elite.elite = True

        elites.append(elite)

    return elites


# ================================================================
# GENERATE NEXT GENERATION
# ================================================================

def generate_next_generation(
    population: List[Agent],
    scores: Dict[str, float],
    generation: int,
    rng: random.Random,
) -> List[Agent]:
    """
    Preserve elites and generate targeted offspring.
    """

    elites = select_elites(
        population,
        scores,
        ELITE_COUNT,
    )

    next_population = []

    # ------------------------------------------------------------
    # Protected elites
    # ------------------------------------------------------------

    for elite in elites:

        elite.generation = generation

        next_population.append(
            elite
        )

    # ------------------------------------------------------------
    # Offspring
    # ------------------------------------------------------------

    child_id = 1

    while len(next_population) < POPULATION_SIZE:

        # Weighted parent selection.
        weights = [
            max(
                1.0,
                scores[e.name],
            )
            for e in elites
        ]

        parent = rng.choices(
            elites,
            weights=weights,
            k=1,
        )[0]

        # Focus mutation on the weakest skill.
        weakest = choose_weakest_skill(
            parent
        )

        # Occasionally explore another skill.
        if rng.random() < 0.25:
            mutation = rng.choice(
                SKILLS
            )
        else:
            mutation = weakest

        # Adaptive mutation size.
        amount = MUTATION_STEP

        if (
            parent.skills.get(
                weakest,
                0.0
            )
            < 0.80
        ):
            amount = 0.08

        child_name = (
            f"V7-G{generation}-Child-{child_id}"
        )

        child = mutate_agent(
            parent=parent,
            mutation=mutation,
            amount=amount,
            child_name=child_name,
        )

        child.generation = generation

        next_population.append(
            child
        )

        child_id += 1

    return next_population


# ================================================================
# GENERATION REPORT
# ================================================================

def print_generation_report(
    generation: int,
    results: Dict[str, Dict[str, Any]],
    population: List[Agent],
) -> None:
    """Print a readable leaderboard."""

    print()
    print("=" * 70)
    print(
        f"🏟️ V7 GENERATION {generation} "
        f"LEADERBOARD"
    )
    print("=" * 70)

    ranking = sorted(
        results.items(),
        key=lambda item: item[1]["accuracy"],
        reverse=True,
    )

    for position, (name, data) in enumerate(
        ranking,
        start=1,
    ):

        agent = next(
            a for a in population
            if a.name == name
        )

        marker = (
            "🏆"
            if agent.elite
            else "🧬"
        )

        print(
            f"{position}. "
            f"{marker} "
            f"{name:<24} "
            f"→ {data['accuracy']:.2f}%"
        )


# ================================================================
# MULTI-SEED ROBUSTNESS TEST
# ================================================================

def robustness_test(
    elite: Agent,
    seeds: List[int] = ROBUSTNESS_SEEDS,
) -> Dict[str, Any]:
    """
    Evaluate the final elite on independent unseen benchmarks.

    No learning.
    No mutation.
    No population changes.
    """

    print()
    print("=" * 70)
    print("🧪 V7.1 MULTI-SEED UNSEEN ROBUSTNESS TEST")
    print("=" * 70)

    print(
        f"🛡️ Elite: {elite.name}"
    )

    print(
        "🚫 Learning: DISABLED"
    )

    print(
        "🚫 Mutation: DISABLED"
    )

    print(
        f"🌱 Seeds: {len(seeds)}"
    )

    print(
        f"📋 Tasks per seed: "
        f"{ROBUSTNESS_TASKS_PER_SEED}"
    )

    results = []

    for seed in seeds:

        benchmark = generate_tasks(
            seed=seed,
            n=ROBUSTNESS_TASKS_PER_SEED,
        )

        result = evaluate_agent(
            elite,
            benchmark,
            seed=seed + 10000,
        )

        results.append(
            result
        )

        print(
            f"Seed {seed:2d}: "
            f"{result['score']:3d}/"
            f"{ROBUSTNESS_TASKS_PER_SEED} "
            f"({result['accuracy']:.2f}%)"
        )

    accuracies = [
        result["accuracy"]
        for result in results
    ]

    mean_accuracy = statistics.mean(
        accuracies
    )

    median_accuracy = statistics.median(
        accuracies
    )

    best_accuracy = max(
        accuracies
    )

    worst_accuracy = min(
        accuracies
    )

    std_accuracy = (
        statistics.stdev(
            accuracies
        )
        if len(accuracies) > 1
        else 0.0
    )

    skill_averages = {}

    for skill in SKILLS:

        values = [
            result["skills"][skill]
            for result in results
        ]

        skill_averages[skill] = (
            statistics.mean(values)
        )

    weakest_skill = min(
        skill_averages,
        key=skill_averages.get,
    )

    print()
    print("=" * 70)
    print("🏆 V7.1 ROBUSTNESS RESULTS")
    print("=" * 70)

    print(
        f"Elite: {elite.name}"
    )

    print(
        f"Average accuracy : "
        f"{mean_accuracy:.2f}%"
    )

    print(
        f"Median accuracy  : "
        f"{median_accuracy:.2f}%"
    )

    print(
        f"Best seed        : "
        f"{best_accuracy:.2f}%"
    )

    print(
        f"Worst seed       : "
        f"{worst_accuracy:.2f}%"
    )

    print(
        f"Std deviation    : "
        f"{std_accuracy:.2f}"
    )

    print()
    print("📚 SKILL AVERAGES")
    print("-" * 70)

    for skill in SKILLS:

        print(
            f"{skill:<10}: "
            f"{skill_averages[skill]:.2f}%"
        )

    print()
    print("=" * 70)
    print("🔬 GENERALIZATION VERDICT")
    print("=" * 70)

    if mean_accuracy >= 90:

        print(
            "🔥 EXCELLENT — "
            "average unseen accuracy >= 90%"
        )

    elif mean_accuracy >= 85:

        print(
            "🟢 STRONG — "
            "average unseen accuracy >= 85%"
        )

    elif mean_accuracy >= 80:

        print(
            "🟡 GOOD — "
            "average unseen accuracy >= 80%"
        )

    else:

        print(
            "🔴 NEEDS IMPROVEMENT — "
            "average unseen accuracy < 80%"
        )

    if std_accuracy <= 3:

        print(
            "🛡️ VERY STABLE — "
            "low variation between seeds"
        )

    elif std_accuracy <= 6:

        print(
            "🟢 STABLE — "
            "acceptable variation"
        )

    else:

        print(
            "⚠️ HIGH VARIANCE — "
            "performance varies significantly"
        )

    print(
        f"🎯 Weakest average skill: "
        f"{weakest_skill} "
        f"({skill_averages[weakest_skill]:.2f}%)"
    )

    print()
    print(
        "🛡️ Elite was NOT modified."
    )

    return {
        "elite": elite.name,
        "results": results,
        "average": mean_accuracy,
        "median": median_accuracy,
        "best": best_accuracy,
        "worst": worst_accuracy,
        "std": std_accuracy,
        "skill_averages": skill_averages,
    }


# ================================================================
# MAIN EVOLUTION ENGINE
# ================================================================

def run_evolution() -> Tuple[Agent, Dict[str, Any]]:
    """
    Run the complete V7 evolutionary experiment.
    """

    print()
    print("=" * 70)
    print("🧬 V7 ELITE EVOLUTION ENGINE")
    print("=" * 70)

    print(
        "Experimental AI-agent evolutionary benchmark"
    )

    print(
        f"Seed: {SEED}"
    )

    print(
        f"Generations: {MAX_GENERATIONS}"
    )

    print(
        f"Population: {POPULATION_SIZE}"
    )

    print(
        f"Elite count: {ELITE_COUNT}"
    )

    print()

    rng = random.Random(
        SEED
    )

    population = (
        create_initial_population()
    )

    all_history = []

    # ------------------------------------------------------------
    # Evolution loop
    # ------------------------------------------------------------

    for generation in range(
        1,
        MAX_GENERATIONS + 1,
    ):

        print()
        print("=" * 70)
        print(
            f"🧬 GENERATION {generation}"
        )
        print("=" * 70)

        benchmark = generate_tasks(
            seed=SEED + generation,
            n=TASKS_PER_BENCHMARK,
        )

        generation_results = {}

        scores = {}

        for agent in population:

            result = evaluate_agent(
                agent,
                benchmark,
                seed=SEED + generation * 100,
            )

            generation_results[
                agent.name
            ] = result

            scores[
                agent.name
            ] = result["accuracy"]

            print(
                f"{'🏆' if agent.elite else '🤖'} "
                f"{agent.name:<24} "
                f"→ {result['accuracy']:.2f}%"
            )

        print_generation_report(
            generation,
            generation_results,
            population,
        )

        # --------------------------------------------------------
        # Evolution summary
        # --------------------------------------------------------

        ranked = sorted(
            population,
            key=lambda agent: scores[agent.name],
            reverse=True,
        )

        best = ranked[0]

        print()
        print(
            f"👑 Generation {generation} best: "
            f"{best.name} "
            f"→ {scores[best.name]:.2f}%"
        )

        all_history.append(
            {
                "generation": generation,
                "results": generation_results,
                "best": best.name,
                "best_score": scores[best.name],
            }
        )

        # --------------------------------------------------------
        # Do not create another generation after final one.
        # --------------------------------------------------------

        if generation == MAX_GENERATIONS:

            final_population = population

            final_scores = scores

            final_elites = select_elites(
                final_population,
                final_scores,
                elite_count=1,
            )

            final_elite = final_elites[0]

            break

        # --------------------------------------------------------
        # Generate next generation
        # --------------------------------------------------------

        population = (
            generate_next_generation(
                population=population,
                scores=scores,
                generation=generation + 1,
                rng=rng,
            )
        )

        print()
        print(
            f"🧬 Generation "
            f"{generation + 1} created."
        )

        print(
            "🛡️ Elites protected."
        )

    # ------------------------------------------------------------
    # Final elite
    # ------------------------------------------------------------

    print()
    print("=" * 70)
    print("👑 FINAL ELITE")
    print("=" * 70)

    print(
        f"Model: {final_elite.name}"
    )

    print(
        f"Generation: "
        f"{final_elite.generation}"
    )

    print(
        f"Parent: "
        f"{final_elite.parent}"
    )

    print(
        f"Mutation: "
        f"{final_elite.mutation}"
    )

    print()
    print("🧠 FINAL SKILL PROFILE")

    for skill, value in (
        final_elite.skills.items()
    ):

        print(
            f"{skill:<10}: "
            f"{value:.3f}"
        )

    # ------------------------------------------------------------
    # Robustness test
    # ------------------------------------------------------------

    robustness = robustness_test(
        final_elite
    )

    print()
    print("=" * 70)
    print("✅ V7 EVOLUTION COMPLETE")
    print("=" * 70)

    print(
        f"Final Elite: "
        f"{final_elite.name}"
    )

    print(
        f"Unseen average: "
        f"{robustness['average']:.2f}%"
    )

    return (
        final_elite,
        {
            "history": all_history,
            "robustness": robustness,
        },
    )


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":

    final_agent, experiment = (
        run_evolution()
    )

    print()
    print("=" * 70)
    print("🏁 EXPERIMENT FINISHED")
    print("=" * 70)

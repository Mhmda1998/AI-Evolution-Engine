"""
============================================================
AI-Evolution-Engine
V7 Elite Evolution
============================================================

Experimental evolutionary framework for AI-agent populations.

Evolution pipeline:

    Generation 1
        ↓
    Arena Evaluation
        ↓
    Generation 2
        ↓
    Adaptive Mutation
        ↓
    Generation 3
        ↓
    Elite Selection
        ↓
    Generation 4
        ↓
    Smart Mutation
        ↓
    V7.1 Robustness Testing

Main concepts:
- Population-based evaluation
- Parent → Child evolution
- Elite preservation
- Adaptive mutation
- Skill-based mutation
- Unseen benchmarks
- Multi-seed robustness

IMPORTANT:
This repository is an experimental research framework.
The benchmark simulator is not evidence of general intelligence.
"""

import copy
import random
import statistics
from collections import defaultdict


# ============================================================
# CONFIGURATION
# ============================================================

SKILLS = [
    "logic",
    "math",
    "coding",
    "planning",
    "reasoning",
]

BENCHMARK_SIZE = 100


# ============================================================
# AGENT
# ============================================================

class AdaptiveAgent:
    """
    Lightweight experimental agent.

    The agent contains a skill profile representing
    its current capability configuration.
    """

    def __init__(self, name, skills):
        self.name = name
        self.skills = dict(skills)

        # Compatibility with the original V7
        # mutation mechanism.
        self.learning = dict(skills)

    def solve(self, task):
        """
        Simulated task solving.

        Returns a dictionary compatible with the
        original V7 arena.
        """

        task_type = task["type"]

        probability = self.skills.get(
            task_type,
            0.70
        )

        probability = max(
            0.0,
            min(0.99, probability)
        )

        correct = random.random() < probability

        return {
            "correct": correct
        }


# ============================================================
# BENCHMARK GENERATOR
# ============================================================

def generate_diverse_unseen_tasks(
    n=100,
    seed=20260702
):
    """
    Generate a deterministic benchmark.
    """

    rng = random.Random(seed)

    tasks = []

    logic_questions = [
        (
            "If all A are B, and all B are C, "
            "are all A necessarily C?",
            "yes",
        ),
        (
            "If no A is B, can something be both A and B?",
            "no",
        ),
        (
            "If some A is B and every B is C, "
            "must some A be C?",
            "yes",
        ),
        (
            "If some A are B and some B are C, "
            "must some A be C?",
            "no",
        ),
    ]

    coding_questions = [
        (
            "What Python function is commonly used "
            "to get the length of a list?",
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
            "What keyword is used to return a value?",
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

    planning_questions = [
        (
            "If a critical resource is running low, "
            "should you secure it before optional goals?",
            "yes",
        ),
        (
            "You need food, water and shelter. "
            "Which should normally be secured first?",
            "water",
        ),
        (
            "If an urgent safety problem appears, "
            "should it be handled before a non-urgent task?",
            "yes",
        ),
        (
            "If a required dependency is missing, "
            "should you resolve it first?",
            "yes",
        ),
        (
            "If a task is optional and another is critical, "
            "which should receive priority?",
            "critical",
        ),
    ]

    # -----------------------------
    # Math
    # -----------------------------

    for _ in range(20):

        a = rng.randint(10, 999)
        b = rng.randint(2, 99)

        tasks.append({
            "type": "math",
            "question": f"What is {a} × {b}?",
            "answer": a * b,
        })

    # -----------------------------
    # Reasoning
    # -----------------------------

    for _ in range(20):

        start = rng.randint(20, 200)
        removed = rng.randint(1, start)

        tasks.append({
            "type": "reasoning",
            "question": (
                f"A store has {start} products "
                f"and sells {removed}. "
                f"How many remain?"
            ),
            "answer": start - removed,
        })

    # -----------------------------
    # Coding
    # -----------------------------

    for _ in range(20):

        question, answer = rng.choice(
            coding_questions
        )

        tasks.append({
            "type": "coding",
            "question": question,
            "answer": answer,
        })

    # -----------------------------
    # Planning
    # -----------------------------

    for _ in range(20):

        question, answer = rng.choice(
            planning_questions
        )

        tasks.append({
            "type": "planning",
            "question": question,
            "answer": answer,
        })

    # -----------------------------
    # Logic
    # -----------------------------

    for _ in range(20):

        question, answer = rng.choice(
            logic_questions
        )

        tasks.append({
            "type": "logic",
            "question": question,
            "answer": answer,
        })

    rng.shuffle(tasks)

    return tasks[:n]


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_answer(value):

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

    return replacements.get(
        value,
        value
    )


# ============================================================
# GENERATION 1
# ============================================================

def generation_1():

    print()
    print("=" * 70)
    print("🏟️ V7 GENERATION 1 — ARENA")
    print("=" * 70)

    random.seed(20260702)

    benchmark = generate_diverse_unseen_tasks(
        BENCHMARK_SIZE,
        seed=20260702
    )

    population = {

        "Adaptive Alpha": {
            "agent": AdaptiveAgent(
                "Adaptive Alpha",
                {
                    "logic": 0.90,
                    "math": 0.90,
                    "coding": 0.85,
                    "planning": 0.80,
                    "reasoning": 0.90,
                },
            ),
            "parent": None,
            "mutation": None,
            "elite": True,
        },

        "Adaptive Beta": {
            "agent": AdaptiveAgent(
                "Adaptive Beta",
                {
                    "logic": 0.85,
                    "math": 0.90,
                    "coding": 0.75,
                    "planning": 0.75,
                    "reasoning": 0.90,
                },
            ),
            "parent": None,
            "mutation": None,
            "elite": True,
        },

        "Adaptive Gamma": {
            "agent": AdaptiveAgent(
                "Adaptive Gamma",
                {
                    "logic": 0.75,
                    "math": 0.80,
                    "coding": 0.80,
                    "planning": 0.75,
                    "reasoning": 0.75,
                },
            ),
            "parent": None,
            "mutation": None,
            "elite": True,
        },
    }

    results = {}

    for name, data in population.items():

        correct = 0

        for task in benchmark:

            result = data["agent"].solve(task)

            correct += int(
                result.get(
                    "correct",
                    False
                )
            )

        accuracy = (
            correct /
            len(benchmark) *
            100
        )

        results[name] = accuracy
        data["score"] = accuracy

        print(
            f"{name}: "
            f"{accuracy:.2f}%"
        )

    print()
    print("🏆 GENERATION 1 COMPLETE")

    return population, results


# ============================================================
# ADAPTIVE MUTATION
# ============================================================

def adaptive_mutation(
    population,
    results
):

    print()
    print("=" * 70)
    print("🧬 V7 GENERATION 2 — ADAPTIVE MUTATION")
    print("=" * 70)

    skills = list(SKILLS)

    mutation_history = {}

    for name, data in population.items():

        parent = data.get("parent")
        mutation = data.get("mutation")

        if not parent or not mutation:
            continue

        if parent not in results:
            continue

        change = (
            results[name] -
            results[parent]
        )

        mutation_history.setdefault(
            mutation,
            []
        ).append(change)

    weights = {}

    for skill in skills:

        history = mutation_history.get(
            skill,
            []
        )

        if not history:

            weights[skill] = 1.0
            continue

        avg = statistics.mean(history)

        if avg > 0:
            weights[skill] = 2.0

        elif avg < 0:
            weights[skill] = 0.5

        else:
            weights[skill] = 1.0

    print()
    print("🧠 MUTATION WEIGHTS")

    for skill, weight in weights.items():

        print(
            f"{skill:<10} → "
            f"{weight:.2f}"
        )

    # Protected elites

    ranking = sorted(
        population.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    elites = ranking[:3]

    next_population = {}

    print()
    print("🛡️ PROTECTED ELITES")

    for name, data in elites:

        next_population[name] = (
            copy.deepcopy(data)
        )

        next_population[name]["elite"] = True

        print(
            f"🏆 {name} → "
            f"{data['score']:.2f}%"
        )

    # Children

    print()
    print("🧬 NEW OFFSPRING")

    for child_id, (
        parent_name,
        parent_data
    ) in enumerate(
        elites,
        start=1
    ):

        child_agent = copy.deepcopy(
            parent_data["agent"]
        )

        mutation = random.choices(
            skills,
            weights=[
                weights[s]
                for s in skills
            ],
            k=1
        )[0]

        current = child_agent.learning.get(
            mutation,
            0.05
        )

        child_agent.learning[
            mutation
        ] = min(
            0.40,
            current + 0.05
        )

        child_agent.skills[
            mutation
        ] = child_agent.learning[
            mutation
        ]

        child_name = (
            f"V7-G2-Child-{child_id}"
        )

        next_population[
            child_name
        ] = {
            "agent": child_agent,
            "parent": parent_name,
            "mutation": mutation,
            "elite": False,
            "score": None,
        }

        print(
            f"🧬 {child_name} "
            f"| Parent: {parent_name} "
            f"| Mutation: {mutation}"
        )

    return next_population


# ============================================================
# ARENA EVALUATION
# ============================================================

def evaluate_population(
    population,
    seed
):

    random.seed(seed)

    benchmark = generate_diverse_unseen_tasks(
        BENCHMARK_SIZE,
        seed=seed
    )

    results = {}

    print()
    print("=" * 70)
    print("🏟️ ADAPTIVE ARENA")
    print("=" * 70)

    for name, data in population.items():

        correct = 0

        for task in benchmark:

            try:

                result = (
                    data["agent"]
                    .solve(task)
                )

                correct += int(
                    result.get(
                        "correct",
                        False
                    )
                )

            except Exception:

                pass

        accuracy = (
            correct /
            len(benchmark) *
            100
        )

        data["score"] = accuracy

        results[name] = accuracy

        print(
            f"{name:<25} "
            f"→ {accuracy:.2f}%"
        )

    return results


# ============================================================
# GENERATION 3
# ============================================================

def generation_3(
    population,
    results
):

    print()
    print("=" * 70)
    print("🧬 V7 GENERATION 3")
    print("=" * 70)

    ranking = sorted(
        population.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    elites = ranking[:3]

    print()
    print("🛡️ PROTECTED ELITES")

    generation = {}

    for name, data in elites:

        generation[name] = (
            copy.deepcopy(data)
        )

        generation[name]["elite"] = True
        generation[name]["generation"] = 3

        print(
            f"🏆 {name} → "
            f"{data['score']:.2f}%"
        )

    # Parent weights

    parent_names = [
        name
        for name, _
        in elites
    ]

    parent_weights = []

    for name, data in elites:

        weight = max(
            1.0,
            data["score"] / 50
        )

        parent_weights.append(weight)

    # Mutation performance

    mutation_weights = {
        skill: 1.0
        for skill in SKILLS
    }

    for name, data in population.items():

        mutation = data.get(
            "mutation"
        )

        parent = data.get(
            "parent"
        )

        if (
            mutation in mutation_weights
            and parent in results
        ):

            change = (
                results[name] -
                results[parent]
            )

            if change >= 5:

                mutation_weights[
                    mutation
                ] = 3.0

            elif change > 0:

                mutation_weights[
                    mutation
                ] = 2.0

            elif change < 0:

                mutation_weights[
                    mutation
                ] = 0.4

    print()
    print("🧬 MUTATION WEIGHTS")

    for skill, weight in (
        mutation_weights.items()
    ):

        print(
            f"{skill:<10} → "
            f"{weight:.2f}"
        )

    # Generate children

    print()
    print("🧬 GENERATING OFFSPRING")

    for child_id in range(1, 4):

        parent_name = random.choices(
            parent_names,
            weights=parent_weights,
            k=1
        )[0]

        parent = generation[
            parent_name
        ]

        child_agent = copy.deepcopy(
            parent["agent"]
        )

        mutation = random.choices(
            SKILLS,
            weights=[
                mutation_weights[s]
                for s in SKILLS
            ],
            k=1
        )[0]

        current = (
            child_agent.learning.get(
                mutation,
                0.05
            )
        )

        child_agent.learning[
            mutation
        ] = min(
            0.45,
            current + 0.05
        )

        child_agent.skills[
            mutation
        ] = child_agent.learning[
            mutation
        ]

        name = (
            f"V7-G3-Child-{child_id}"
        )

        generation[name] = {
            "agent": child_agent,
            "parent": parent_name,
            "mutation": mutation,
            "elite": False,
            "generation": 3,
            "score": None,
        }

        print(
            f"🧬 {name}"
        )

        print(
            f"   Parent: {parent_name}"
        )

        print(
            f"   Mutation: {mutation}"
        )

    return generation


# ============================================================
# GENERATION 4
# ============================================================

def generation_4(
    elite_name,
    elite_agent,
    elite_score,
    seed=2027
):

    print()
    print("=" * 70)
    print(
        "🧬 V7 GENERATION 4 — "
        "SMART ELITE EVOLUTION"
    )
    print("=" * 70)

    random.seed(seed)

    elite_skills = dict(
        elite_agent.skills
    )

    print()
    print("🛡️ PROTECTED ELITE")

    print(
        f"{elite_name} → "
        f"{elite_score:.2f}%"
    )

    print(
        "Elite will NOT be mutated directly."
    )

    weakness = min(
        elite_skills,
        key=elite_skills.get
    )

    print()
    print(
        f"🎯 Detected weakness: "
        f"{weakness}"
    )

    mutation_plan = [
        ("logic", 0.08),
        ("logic", 0.12),
        ("planning", 0.08),
        ("reasoning", 0.08),
        ("coding", 0.05),
    ]

    children = {}

    for i, (
        mutation,
        amount
    ) in enumerate(
        mutation_plan,
        start=1
    ):

        skills = dict(
            elite_skills
        )

        skills[mutation] = min(
            0.99,
            skills[mutation] + amount
        )

        # Controlled trade-off

        if mutation != "math":

            skills["math"] = max(
                0.80,
                skills["math"] - 0.01
            )

        name = (
            f"V7-G4-Child-{i}"
        )

        children[name] = {
            "agent": AdaptiveAgent(
                name,
                skills
            ),
            "parent": elite_name,
            "mutation": mutation,
            "skills": skills,
        }

    # Benchmark

    benchmark = generate_diverse_unseen_tasks(
        100,
        seed=seed
    )

    # Evaluate elite

    elite_results = evaluate_agent(
        elite_agent,
        benchmark
    )

    leaderboard = [
        (
            elite_name,
            elite_results["score"],
            "PROTECTED ELITE"
        )
    ]

    print()
    print(
        "🏆 PROTECTED ELITE EVALUATION"
    )

    print(
        f"{elite_name}: "
        f"{elite_results['score']}/100"
    )

    # Evaluate children

    for name, data in children.items():

        result = evaluate_agent(
            data["agent"],
            benchmark
        )

        leaderboard.append(
            (
                name,
                result["score"],
                f"Mutation: "
                f"{data['mutation']}"
            )
        )

        print()
        print(
            f"🤖 {name}"
        )

        print(
            f"   Parent: "
            f"{data['parent']}"
        )

        print(
            f"   Mutation: "
            f"{data['mutation']}"
        )

        print(
            f"   Score: "
            f"{result['score']}/100"
        )

    leaderboard.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print()
    print(
        "🏆 V7 GENERATION 4 LEADERBOARD"
    )

    print("=" * 70)

    for rank, (
        name,
        score,
        info
    ) in enumerate(
        leaderboard,
        start=1
    ):

        print(
            f"{rank}. "
            f"{name:<20} "
            f"→ {score:.2f}% "
            f"| {info}"
        )

    best_name, best_score, _ = (
        leaderboard[0]
    )

    print()
    print(
        "👑 V7 GENERATION 4 "
        "ELITE DECISION"
    )

    if best_name == elite_name:

        print(
            f"🛡️ Elite preserved: "
            f"{elite_name}"
        )

    else:

        print(
            f"🔥 NEW ELITE: "
            f"{best_name}"
        )

        print(
            f"Improvement: "
            f"{best_score - elite_results['score']:+.2f}"
        )

    return {
        "elite": best_name,
        "score": best_score,
        "leaderboard": leaderboard,
        "children": children,
    }


# ============================================================
# GENERIC AGENT EVALUATOR
# ============================================================

def evaluate_agent(
    agent,
    tasks
):

    correct = 0

    by_skill = defaultdict(
        lambda: [0, 0]
    )

    for task in tasks:

        try:

            result = agent.solve(task)

            prediction = (
                result.get(
                    "answer",
                    result.get(
                        "correct",
                        False
                    )
                )
            )

            if isinstance(
                prediction,
                bool
            ):

                success = prediction

            else:

                success = (
                    normalize_answer(
                        prediction
                    )
                    ==
                    normalize_answer(
                        task["answer"]
                    )
                )

        except Exception:

            success = False

        skill = task["type"]

        by_skill[skill][1] += 1

        if success:

            correct += 1
            by_skill[skill][0] += 1

    skill_scores = {}

    for skill in SKILLS:

        c, total = (
            by_skill[skill]
        )

        skill_scores[skill] = (
            c / total * 100
            if total
            else 0.0
        )

    return {
        "score": correct,
        "accuracy": (
            correct /
            len(tasks) *
            100
        ),
        "skills": skill_scores,
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_v7():

    print()
    print("=" * 70)
    print("🧬 AI-EVOLUTION-ENGINE — V7")
    print("=" * 70)

    # -------------------------
    # Generation 1
    # -------------------------

    population, results = (
        generation_1()
    )

    # -------------------------
    # Generation 2
    # -------------------------

    population = adaptive_mutation(
        population,
        results
    )

    results = evaluate_population(
        population,
        seed=20260703
    )

    # -------------------------
    # Generation 3
    # -------------------------

    population = generation_3(
        population,
        results
    )

    results = evaluate_population(
        population,
        seed=2026
    )

    # -------------------------
    # Select elite
    # -------------------------

    best_name = max(
        results,
        key=results.get
    )

    best_data = population[
        best_name
    ]

    # -------------------------
    # Generation 4
    # -------------------------

    final = generation_4(
        best_name,
        best_data["agent"],
        best_data["score"]
    )

    print()
    print("=" * 70)
    print("✅ V7 EVOLUTION COMPLETE")
    print("=" * 70)

    print(
        f"Final elite: "
        f"{final['elite']}"
    )

    print(
        f"Final score: "
        f"{final['score']:.2f}%"
    )

    return final


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_v7()

# Test-Time Scaling — Inference Computing para Razonamiento en LLMs

> **Fecha:** 2026-07-08
> **Autor:** Mastermind (David Antizar)
> **Tema:** Test-Time Compute / Test-Time Scaling (TTC/TTS)
> **Categoría:** Deep Learning → Inferencia Avanzada

---

## 1. ¿Qué es Test-Time Scaling?

**Test-Time Compute (TTC)** o **Test-Time Scaling (TTS)** es el paradigma de **desviar cómputo del entrenamiento a la inferencia**. En lugar de depender exclusivamente de parámetros más grandes o más datos de entrenamiento, TTC **asigna dinámicamente más recursos computacionales durante la inferencia** para mejorar el razonamiento del modelo.

**Analogía:** Tradicionalmente, un LLM respondía por "instinto" (un forward pass). Con TTC, el modelo "piensa más antes de responder", verificando su trabajo múltiples veces.

### La Premisa Fundamental

```
Performance = f(Parámetros, Datos de Entrenamiento, Cómputo de Inferencia)
```

Las tres últimas décadas se centraron en los dos primeros factores. TTC demuestra que el **tercer factor** —cómputo de inferencia— es una palanca poderosa y a menudo más eficiente que escalar parámetros.

**Paper clave:** *"Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"* (Snell et al., Google DeepMind / UC Berkeley, 2024) — arXiv:2408.03314

---

## 2. Taxonomía de Métodos TTC

### 2.1 Métodos de Camino Único (Single-Path)

#### Chain-of-Thought (CoT)
- **Idea:** Forzar al modelo a generar pasos intermedios de razonamiento
- **Paper:** Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in LLMs" (2022)
- **Implementación:** Few-shot prompting con ejemplos que muestran reasoning chains

```python
# CoT básico con OpenAI
prompt = """Q: Roger tiene 5 bolas. Compra 2 más y luego vende 3.
¿Cuántas bolas tiene ahora?
A: Vamos paso a paso:
- Roger empieza con 5 bolas
- Compra 2 más: 5 + 2 = 7
- Vende 3: 7 - 3 = 4
A: 4

Q: Un restaurante vende 23 pasteles de manzana por semana.
Si hace 4 pasteles cada lunes y el triple cada viernes que lunes,
¿cuántos pasteles hace cada viernes?
A: """
```

#### Self-Consistency
- **Idea:** Muestrear N reasoning chains independientes y tomar voto mayoritario
- **Mejora:** +10-15pp en GSM8K con N=5 vs greedy decoding
- **Costo:** Crecimiento lineal en tokens consumidos

```python
import json
from collections import Counter

def self_consistency(model, prompt, n_samples=5, temperature=0.7):
    """Voto mayoritario sobre N cadenas de razonamiento"""
    answers = []
    for _ in range(n_samples):
        response = model.generate(prompt, temperature=temperature, max_tokens=1024)
        # Extraer respuesta final (último número o texto después de "A:")
        answer = extract_answer(response)
        answers.append(answer)
    
    # Voto mayoritario
    most_common = Counter(answers).most_common(1)[0]
    return most_common[0], most_common[1] / n_samples
```

### 2.2 Métodos de Búsqueda Múltiple (Multi-Path Search)

#### Best-of-N (BoN)
- **Idea:** Generar N candidatos y seleccionar el mejor con un verifier
- **Verificador:** Puede ser un ORM (Outcome Reward Model) o un modelo de lenguaje

```python
def best_of_n(model, verifier, prompt, n_candidates=16):
    """Generar N candidatos y seleccionar el mejor con verifier"""
    candidates = []
    for _ in range(n_candidates):
        response = model.generate(prompt, temperature=0.8, max_tokens=2048)
        score = verifier.score(response)
        candidates.append((response, score))
    
    # Seleccionar el mejor
    best = max(candidates, key=lambda x: x[1])
    return best[0], best[1]
```

#### Beam Search (Verifier-Guided)
- **Idea:** Mantener N mejores traces parciales en cada paso
- **Ventaja:** Más eficiente que BoN (no regenera desde cero)
- **Paper:** "Scaling LLM Test-Time Compute Optimally" (Snell et al., 2024)

```python
def verifier_guided_beam_search(model, verifier, prompt, beam_width=4, max_steps=20):
    """Beam search guiado por verificador"""
    # Inicializar con el prompt
    beams = [{"trace": [prompt], "score": 1.0}]
    
    for step in range(max_steps):
        new_beams = []
        for beam in beams:
            # Generar continuaciones
            continuation = model.generate(
                "\n".join(beam["trace"]), 
                temperature=0.7, 
                max_tokens=128
            )
            # Scorear con verificador
            score = verifier.score(beam["trace"] + [continuation])
            new_beams.append({
                "trace": beam["trace"] + [continuation],
                "score": score
            })
        
        # Mantener los beam_width mejores
        beams = sorted(new_beams, key=lambda x: x["score"], reverse=True)[:beam_width]
    
    return max(beams, key=lambda x: x["score"])["trace"]
```

#### Monte Carlo Tree Search (MCTS)
- **Idea:** Construir un árbol de búsqueda durante la inferencia, balanceando exploración y explotación
- **Inspiración:** AlphaZero, pero aplicado a texto
- **Uso:** Tareas de razonamiento complejo (matemáticas, programación)

```python
class MCTSNode:
    """Nodo del árbol MCTS para razonamiento LLM"""
    def __init__(self, trace, parent=None, action=None):
        self.trace = trace          # Lista de pasos de razonamiento
        self.parent = parent
        self.action = action        # Acción/token generado
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions = []
    
    def ucb1_score(self, c_param=1.41):
        """Upper Confidence Bound para balancear exploración/explotación"""
        if self.visits == 0:
            return float('inf')
        exploitation = self.value / self.visits
        exploration = c_param * (2 * self.parent.visits ** 0.5 / self.visits) ** 0.5
        return exploitation + exploration


class MCTSReasoner:
    """MCTS para mejorar razonamiento en LLMs"""
    
    def __init__(self, model, verifier, c_param=1.41, n_simulations=16):
        self.model = model
        self.verifier = verifier
        self.c_param = c_param
        self.n_simulations = n_simulations
    
    def search(self, prompt, max_steps=30):
        """Buscar la mejor cadena de razonamiento"""
        root = MCTSNode([prompt])
        
        for _ in range(self.n_simulations):
            node = self._select(root)
            
            if not self._is_terminal(node):
                node = self._expand(node)
            
            value = self._simulate(node)
            self._backpropagate(node, value)
        
        # Retornar el hijo con más visitas (más confiable)
        best_child = max(root.children, key=lambda c: c.visits)
        return "\n".join(best_child.trace), best_child.visits / self.n_simulations
    
    def _select(self, node):
        """Seleccionar el mejor nodo según UCB1"""
        while node.children:
            node = max(node.children, key=lambda c: c.ucb1_score(self.c_param))
        return node
    
    def _expand(self, node):
        """Expandir el nodo generando continuaciones"""
        last_step = node.trace[-1]
        continuation = self.model.generate(
            last_step, temperature=0.8, max_tokens=128
        )
        child = MCTSNode(node.trace + [continuation], parent=node, action=continuation)
        node.children.append(child)
        return child
    
    def _simulate(self, node):
        """Simulación: scorear el trace con el verificador"""
        return self.verifier.score(node.trace)
    
    def _backpropagate(self, node, value):
        """Backpropagar el valor al árbol"""
        while node:
            node.visits += 1
            node.value += value
            node = node.parent
    
    def _is_terminal(self, node):
        """Verificar si el trace ha llegado a una respuesta"""
        return len(node.trace) > 5 and self._has_answer(node.trace[-1])
```

#### Diverse Verifier Tree Search (DVTS)
- **Idea:** Combinar diversidad en el muestreo con búsqueda guiada por verificador
- **Ventaja:** Mayor cobertura del espacio de soluciones vs beam search

### 2.3 Métodos de Revisión

#### Revision / Self-Correction
- **Idea:** Generar una respuesta, luego pedir al modelo que la revise y corrija
- **Paper:** "Self-Consistency Improves Chain of Thought Reasoning in Language Models" (Wang et al., 2022)
- **Variante:** "Let's Verify Step by Step" (Yan et al., 2023)

```python
def self_correction_loop(model, verifier, prompt, max_iterations=3):
    """Loop de auto-corrección iterativa"""
    current_trace = [prompt]
    
    for iteration in range(max_iterations):
        # Generar respuesta
        response = model.generate("\n".join(current_trace), max_tokens=1024)
        current_trace.append(response)
        
        # Verificar
        score = verifier.score(current_trace)
        
        if score > 0.9:  # Threshold de confianza
            break
        
        # Pedir revisión
        revision_prompt = f"""El siguiente razonamiento tiene errores.
Identifica el error y proporciona una corrección:

{chr(10).join(current_trace)}

Paso 1: Identifica el error exacto.
Paso 2: Explica por qué es un error.
Paso 3: Proporciona la corrección."""
        
        revision = model.generate(revision_prompt, max_tokens=512)
        current_trace.append(revision)
    
    return current_trace
```

---

## 3. Verificadores: ORM vs PRM

El corazón de TTC son los **verificadores** — modelos que evalúan la calidad de las respuestas. Hay dos paradigmas:

### 3.1 Outcome Reward Model (ORM)
- **Qué hace:** Scorea solo la respuesta final
- **Ventaja:** Más fácil de entrenar, requiere menos datos de labeling
- **Desventaja:** No da feedback granular sobre pasos intermedios
- **Uso:** Mejor para tareas con respuesta única y verificable

```python
class OutcomeRewardModel:
    """ORM: scorea solo el resultado final"""
    
    def __init__(self, model_name="openai/prm800k-orm"):
        self.model = load_model(model_name)
    
    def score(self, trace):
        """Scorea la respuesta final del trace"""
        final_answer = extract_final_answer(trace)
        score = self.model.predict(trace[0], final_answer)
        return score  # [0, 1]
```

### 3.2 Process Reward Model (PRM)
- **Qué hace:** Scorea **cada paso intermedio** del razonamiento
- **Ventaja:** Feedback granular, mejor credit assignment
- **Desventaja:** Requiere labeling paso a paso (más costoso)
- **Uso:** Mejor para búsqueda (beam search, MCTS) donde necesitas scorear traces parciales

```python
class ProcessRewardModel:
    """PRM: scorea cada paso del razonamiento"""
    
    def __init__(self, model_name="openai/prm800k-prm"):
        self.model = load_model(model_name)
    
    def score_step(self, trace, step_idx):
        """Scorea un paso individual del trace"""
        context = "\n".join(trace[:step_idx+1])
        return self.model.predict(context)  # Score del paso actual dado el contexto
    
    def score_trace(self, trace):
        """Scorea un trace completo como producto de scores por paso"""
        step_scores = [self.score_step(trace, i) for i in range(len(trace))]
        # Producto (o media ponderada)
        return product(step_scores)
```

### Comparación ORM vs PRM

| Aspecto | ORM | PRM |
|---------|-----|-----|
| **Señal** | Escalar final | Paso a paso |
| **Señal densidad** | Baja (1 por trace) | Alta (N por trace) |
| **Credit assignment** | Difícil | Fácil |
| **Costo de labeling** | Bajo | Alto |
| **Mejor para** | BoN, voting | Beam search, MCTS |
| **Robustez a search** | Baja (reward hacking) | Alta |

**Paper clave:** "A Survey of Process Reward Models: From Outcome Signals to Step-Level Feedback" (2025) — arXiv:2510.08049

---

## 4. Hallazgos Clave de la Investigación Reciente

### 4.1 "The Art of Scaling Test-Time Compute" (Agarwal et al., Microsoft Research, 2025)
**Paper:** arXiv:2512.02008

**Experimento:** Estudio a gran escala con 8 LLMs open-source (7B-235B), >30B tokens generados, 4 datasets de razonamiento.

**Tres hallazgos consistentes:**
1. **No hay estrategia universalmente mejor** — La óptima depende del modelo, tarea y presupuesto
2. **Los reasoning models se dividen en dos categorías:**
   - **Short-horizon:** R1, DAPO-32B, QwQ-32B — mejoran con traces cortos
   - **Long-horizon:** Qwen3-32B, GPT-OSS-120B, R1-32B — mejoran con traces largos
3. **La performance óptima escala monótonamente con el presupuesto de cómputo** para un modelo dado

**Receta práctica:**
- **Cómputo bajo →** Shortest trace (greedy decoding)
- **Cómputo medio →** Beam search
- **Cómputo alto →** Majority voting (Self-Consistency)

### 4.2 "Scaling LLM Test-Time Compute Optimally" (Snell et al., Google DeepMind, 2024)
**Paper:** arXiv:2408.03314

**Hallazgos clave:**
- Escalar test-time compute óptimamente puede ser **más efectivo que escalar parámetros**
- La búsqueda contra PRMs es más efectiva que contra ORMs para tareas complejas
- Refinar la distribución del proposal (revision models) mejora significativamente los resultados

### 4.3 Inverse Scaling en TTC
- **Paper:** "Inverse Scaling of Test-Time Compute" (Gema et al., 2025)
- **Hallazgo:** En tareas sintéticas diseñadas para aislar habilidades de razonamiento específicas, **traces más largos pueden empeorar el rendimiento**
- **Implicación:** Más cómputo no siempre es mejor — depende de la naturaleza de la tarea

---

## 5. Implementación Práctica: Sistema Completo TTC

```python
"""
Sistema completo de Test-Time Compute Scaling
Implementación práctica con múltiples estrategias y selección adaptativa
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from enum import Enum


class TTSStrategy(Enum):
    GREEDY = "greedy"
    SELF_CONSISTENCY = "self_consistency"
    BEST_OF_N = "best_of_n"
    BEAM_SEARCH = "beam_search"
    MCTS = "mcts"
    SELF_CORRECTION = "self_correction"


@dataclass
class TTCConfig:
    """Configuración del sistema TTC"""
    max_tokens: int = 2048
    temperature: float = 0.7
    n_samples: int = 8
    beam_width: int = 4
    mcts_simulations: int = 16
    mcts_c_param: float = 1.41
    max_self_correction: int = 3
    verify_every_n_steps: int = 3
    early_stop_threshold: float = 0.95
    compute_budget: int = 100000  # Tokens budget


@dataclass
class ReasoningResult:
    """Resultado de un razonamiento TTC"""
    trace: List[str]
    answer: str
    confidence: float
    tokens_used: int
    strategy: str
    verification_scores: List[float] = field(default_factory=list)


class TestTimeComputeEngine:
    """Motor principal de Test-Time Compute Scaling"""
    
    def __init__(self, generator, verifier, difficulty_estimator=None):
        self.generator = generator  # Función que genera texto
        self.verifier = verifier    # Función que scorea respuestas
        self.difficulty_estimator = difficulty_estimator  # Estimador de dificultad
        self.config = TTCConfig()
    
    def estimate_difficulty(self, prompt: str) -> float:
        """Estimar dificultad de la pregunta (0-1)"""
        if self.difficulty_estimator:
            return self.difficulty_estimator(prompt)
        # Heurística simple: longitud del prompt + complejidad léxica
        word_count = len(prompt.split())
        if word_count < 30:
            return 0.2
        elif word_count < 80:
            return 0.5
        else:
            return 0.8
    
    def adaptive_strategy(self, prompt: str) -> TTSStrategy:
        """Seleccionar estrategia adaptativa basada en dificultad y budget"""
        difficulty = self.estimate_difficulty(prompt)
        budget = self.config.compute_budget
        
        if difficulty < 0.3 and budget < 10000:
            return TTSStrategy.GREEDY
        elif difficulty < 0.5 and budget < 50000:
            return TTSStrategy.SELF_CONSISTENCY
        elif difficulty < 0.7 and budget < 100000:
            return TTSStrategy.BEST_OF_N
        elif difficulty < 0.8:
            return TTSStrategy.BEAM_SEARCH
        else:
            return TTSStrategy.MCTS
    
    def run(self, prompt: str, strategy: Optional[TTSStrategy] = None) -> ReasoningResult:
        """Ejecutar TTC con estrategia adaptativa"""
        if strategy is None:
            strategy = self.adaptive_strategy(prompt)
        
        print(f"🔍 Estrategia seleccionada: {strategy.value}")
        
        if strategy == TTSStrategy.GREEDY:
            return self._greedy(prompt)
        elif strategy == TTSStrategy.SELF_CONSISTENCY:
            return self._self_consistency(prompt)
        elif strategy == TTSStrategy.BEST_OF_N:
            return self._best_of_n(prompt)
        elif strategy == TTSStrategy.BEAM_SEARCH:
            return self._beam_search(prompt)
        elif strategy == TTSStrategy.MCTS:
            return self._mcts(prompt)
        elif strategy == TTSStrategy.SELF_CORRECTION:
            return self._self_correction(prompt)
    
    def _greedy(self, prompt: str) -> ReasoningResult:
        """Greedy decoding (single pass)"""
        response = self.generator.generate(
            prompt, temperature=0.0, max_tokens=self.config.max_tokens
        )
        answer = extract_answer(response)
        score = self.verifier.score([prompt, response])
        return ReasoningResult(
            trace=[prompt, response],
            answer=answer,
            confidence=score,
            tokens_used=len(response.split()),
            strategy="greedy"
        )
    
    def _self_consistency(self, prompt: str) -> ReasoningResult:
        """Self-Consistency: N samples + majority vote"""
        answers = []
        scores = []
        traces = []
        
        for i in range(self.config.n_samples):
            response = self.generator.generate(
                prompt, 
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            answer = extract_answer(response)
            score = self.verifier.score([prompt, response])
            
            answers.append(answer)
            scores.append(score)
            traces.append(response)
        
        # Majority vote
        from collections import Counter
        most_common_answer, count = Counter(answers).most_common(1)[0]
        confidence = count / len(answers)
        
        # Seleccionar el trace con la respuesta más común y mejor score
        best_idx = next(i for i, a in enumerate(answers) if a == most_common_answer)
        
        return ReasoningResult(
            trace=[prompt] + traces,
            answer=most_common_answer,
            confidence=confidence,
            tokens_used=sum(len(t.split()) for t in traces),
            strategy="self_consistency",
            verification_scores=scores
        )
    
    def _best_of_n(self, prompt: str) -> ReasoningResult:
        """Best-of-N con verifier"""
        candidates = []
        
        for _ in range(self.config.n_samples):
            response = self.generator.generate(
                prompt, temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            score = self.verifier.score([prompt, response])
            candidates.append((response, score))
        
        # Best by verifier score
        best = max(candidates, key=lambda x: x[1])
        answer = extract_answer(best[0])
        
        return ReasoningResult(
            trace=[prompt] + [c[0] for c in candidates],
            answer=answer,
            confidence=best[1],
            tokens_used=sum(len(c[0].split()) for c in candidates),
            strategy="best_of_n",
            verification_scores=[c[1] for c in candidates]
        )
    
    def _beam_search(self, prompt: str) -> ReasoningResult:
        """Verifier-guided beam search"""
        beams = [{"trace": [prompt], "score": 1.0}]
        all_candidates = []
        
        for step in range(self.config.max_tokens // 50):  # ~50 tokens por paso
            new_beams = []
            for beam in beams:
                continuation = self.generator.generate(
                    "\n".join(beam["trace"][-1:] if len(beam["trace"]) > 1 else prompt),
                    temperature=0.7,
                    max_tokens=50
                )
                score = self.verifier.score(beam["trace"] + [continuation])
                new_beams.append({
                    "trace": beam["trace"] + [continuation],
                    "score": score
                })
            
            # Keep top beam_width
            beams = sorted(new_beams, key=lambda x: x["score"], reverse=True)[
                :self.config.beam_width
            ]
            
            # Early stopping
            if beams[0]["score"] > self.config.early_stop_threshold:
                break
        
        best = max(beams, key=lambda x: x["score"])
        answer = extract_answer(best["trace"][-1])
        
        return ReasoningResult(
            trace=best["trace"],
            answer=answer,
            confidence=best["score"],
            tokens_used=sum(len(t.split()) for t in best["trace"]),
            strategy="beam_search",
            verification_scores=[b["score"] for b in beams]
        )
    
    def _mcts(self, prompt: str) -> ReasoningResult:
        """Monte Carlo Tree Search para razonamiento"""
        root = MCTSNode([prompt])
        
        for _ in range(self.config.mcts_simulations):
            node = self._mcts_select(root)
            if not self._is_terminal(node):
                node = self._mcts_expand(node)
            value = self._mcts_simulate(node)
            self._mcts_backpropagate(node, value)
        
        # Best child by visits
        best = max(root.children, key=lambda c: c.visits)
        answer = extract_answer(best.trace[-1])
        
        return ReasoningResult(
            trace=best.trace,
            answer=answer,
            confidence=best.visits / self.config.mcts_simulations,
            tokens_used=sum(len(t.split()) for t in best.trace),
            strategy="mcts",
            verification_scores=[]
        )
    
    def _mcts_select(self, node: 'MCTSNode') -> 'MCTSNode':
        while node.children:
            node = max(node.children, key=lambda c: self._ucb1(c))
        return node
    
    def _mcts_expand(self, node: 'MCTSNode') -> 'MCTSNode':
        last = node.trace[-1]
        continuation = self.generator.generate(
            last, temperature=0.8, max_tokens=128
        )
        child = MCTSNode(node.trace + [continuation], parent=node)
        node.children.append(child)
        return child
    
    def _mcts_simulate(self, node: 'MCTSNode') -> float:
        return self.verifier.score(node.trace)
    
    def _mcts_backpropagate(self, node: 'MCTSNode', value: float):
        while node:
            node.visits += 1
            node.value += value
            node = node.parent
    
    def _ucb1(self, node: 'MCTSNode') -> float:
        if node.visits == 0:
            return float('inf')
        exploitation = node.value / node.visits
        exploration = self.config.mcts_c_param * (
            2 * math.log(node.parent.visits) / node.visits
        ) ** 0.5
        return exploitation + exploration
    
    def _is_terminal(self, node: 'MCTSNode') -> bool:
        return len(node.trace) > 3 and self._has_answer(node.trace[-1])
    
    def _self_correction(self, prompt: str) -> ReasoningResult:
        """Self-correction loop"""
        trace = [prompt]
        
        for _ in range(self.config.max_self_correction):
            response = self.generator.generate(
                "\n".join(trace), max_tokens=self.config.max_tokens
            )
            trace.append(response)
            
            score = self.verifier.score(trace)
            if score > self.config.early_stop_threshold:
                break
            
            # Revision prompt
            revision = self.generator.generate(
                f"Este razonamiento tiene errores. Corrígelo:\n\n{''.join(trace)}",
                max_tokens=512
            )
            trace.append(revision)
        
        answer = extract_answer(trace[-1])
        return ReasoningResult(
            trace=trace,
            answer=answer,
            confidence=score,
            tokens_used=sum(len(t.split()) for t in trace),
            strategy="self_correction"
        )
```

---

## 6. OpenAI o1 y DeepSeek R1: Implementaciones Reales

### 6.1 OpenAI o1

**Arquitectura:**
- RL training con PPO para aprender a producir reasoning chains
- Reasoning tokens ocultos (no visibles al usuario)
- Modelo decide autónomamente la profundidad de pensamiento
- Verifier training separado para scoring de respuestas

**Características clave:**
- El modelo aprende a "pensar antes de responder" durante el RL
- No usa CoT prompting explícito — el reasoning es parte del modelo
- Verifier scorea la respuesta final (ORM-style)

### 6.2 DeepSeek R1

**Arquitectura:**
- GRPO (Group Relative Policy Optimization) sin reward models costosos
- Reasoning tokens **visibles** al usuario (dentro de tags `<think>`)
- Cold data: pretraining con datos de reasoning generados por modelos más grandes
- Dos fases: SFT con reasoning data → RL con GRPO

**Características clave:**
- Más transparente que o1 (reasoning visible)
- Más barato de entrenar (sin reward model costoso)
- Reasoning tags: `<think>...reasoning...</think>...answer`

---

## 7. Benchmarks y Evaluación

### Datasets principales:
- **GSM8K:** Matemáticas de escuela primaria (fácil)
- **MATH:** Problemas de matemáticas de competición (difícil)
- **AIME:** Olimpiada de matemáticas (muy difícil)
- **GPQA Diamond:** Preguntas de ciencia de PhD (extremo)
- **HumanEval:** Programación (coding)
- **SVAMP:** Problemas de word problems

### Métricas:
- **Accuracy@N:** Porcentaje de respuestas correctas con N samples
- **Tokens por respuesta correcta:** Eficiencia del TTC
- **Latencia:** Tiempo hasta primera respuesta
- **Costo por respuesta:** En $ para APIs

---

## 8. Limitaciones y Críticas

1. **No es universal:** Inverse scaling en ciertas tareas sintéticas
2. **Latencia:** Más tokens = más tiempo de respuesta
3. **Costo:** N samples = N× tokens = N× coste
4. **Verificador fiable:** Necesitas un buen verifier, que es difícil de entrenar
5. **Error acumulado:** Traces largos pueden acumular errores tempranos
6. **Overthinking:** A veces el modelo "piensa demasiado" y se desvía

---

## 9. Recursos y Referencias

### Papers fundamentales:
1. **Snell et al. (2024)** — "Scaling LLM Test-Time Compute Optimally" — arXiv:2408.03314
2. **Agarwal et al. (2025)** — "The Art of Scaling Test-Time Compute" — arXiv:2512.02008
3. **Wei et al. (2022)** — "Chain-of-Thought Prompting" — https://arxiv.org/abs/2201.11903
4. **Wang et al. (2022)** — "Self-Consistency Improves Chain of Thought" — https://arxiv.org/abs/2203.11171
5. **Yan et al. (2023)** — "Let's Verify Step by Step" — https://arxiv.org/abs/2305.20050
6. **Gema et al. (2025)** — "Inverse Scaling of Test-Time Compute"
7. **Survey (2025)** — "What, How, Where, and How Well? A Survey on Test-Time Scaling" — https://testtimescaling.github.io/

### Recursos prácticos:
- **HuggingFace H4 Space:** https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute
- **HuggingFace Blog:** https://huggingface.co/blog/Kseniase/testtimecompute
- **Awesome-LLM-Strawberry:** https://github.com/hijkzzz/Awesome-LLM-Strawberry
- **Awesome-System2-Reasoning-LLM:** https://github.com/zzli2022/Awesome-System2-Reasoning-LLM
- **hermes (engine TTC):** https://github.com/Hritikd/hermes — Test-time compute scaling engine con PRM, MCTS y beam search

---

## 10. Conclusiones

Test-Time Scaling representa un **cambio de paradigma** en cómo pensamos sobre la mejora de LLMs:

1. **No necesitas más parámetros** — puedes obtener mejoras significativas con más cómputo de inferencia
2. **La estrategia óptima depende del contexto** — no hay una solución única
3. **Los verificadores son el cuello de botella** — un buen PRM/ORM es esencial
4. **El futuro es híbrido** — combinar TTC con training (RL, GRPO) da los mejores resultados
5. **Es práctico ya** — las técnicas open-source están disponibles y son eficientes

**La relación fundamental:**
```
Performance = f(Parámetros × Datos × Cómputo de Inferencia)
```
TTC nos enseña que los tres factores son igualmente importantes.

---

## Tema Sugerido para la Próxima Sesión

**Neural Architecture Search (NAS) y AutoML para LLMs**

Justificación:
- Complementa TTC: si TTC optimiza el cómputo de inferencia, NAS optimiza la arquitectura del modelo
- Muy relevante para el ecosistema actual (cada día hay un nuevo modelo con arquitectura diferente)
- Conexión directa con lo cubierto: MoE, SSM/Mamba, ViT, DiT — todos son resultados de búsqueda de arquitectura
- Papers recientes: GShard, Switch Transformers, Mixtral, y los nuevos architectures como RWKV-7, Mamba-3

**Alternativa:** **Tokenizers y Modelos de Subword** (BPE, Unigram, WordPiece, SentencePiece) — fundamental para entender cómo los LLMs procesan texto, y muy poco cubierto en el ecosistema.

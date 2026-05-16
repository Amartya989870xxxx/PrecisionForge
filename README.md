<div align="center">
  <h1>PrecisionForge</h1>
  <p><em>Memory that steers itself. Inference-time precision control for neural memory agents.</em></p>
</div>

---

## 🧠 The Concept: Breaking the Scalar Paradigm

In classical neural memory networks (such as continuous Hopfield networks or modern dense associative memories), retrieval is typically controlled by a **single scalar temperature parameter** (often denoted as $\beta$). This single knob governs the softmax distribution uniformly across all features. 

**The Problem:** One scalar is never enough. When query vectors encounter real-world noise, partial masks, or heavy corruption, a global temperature forces the model to treat all dimensions equally. This lack of granularity often leads to hallucinated retrievals, blurred outputs, or unstable convergence.

**The PrecisionForge Solution:** 
Instead of a single scalar $\beta$, PrecisionForge introduces $\Pi$—a **64-dimensional diagonal precision matrix**. 

By calculating 64 independent precision weights dynamically at *inference-time*, the agent can effectively "steer" its own memory retrieval. It assigns high confidence to reliable signal dimensions and aggressively suppresses noise in corrupted dimensions. Crucially, this is achieved **entirely deterministically**, requiring absolutely zero backpropagation, gradient descent, or model retraining.

---

## 🏛️ The Architecture

PrecisionForge is divided into two primary domains: the **Core AI Engine** and the **Full-Stack Application Layer**.

### 1. Two-Regime Intelligence (The Python Engine)
At the heart of the system is the `Engine` adapter, which evaluates incoming queries and dynamically splits its logic into two distinct mathematical regimes based on nearest-pattern cosine confidence:

* **Regime 1: Retrieval (Corrupted Queries)**
  * *Trigger:* Confidence $\le 0.82$
  * *Mechanism:* Computes a continuous corruption map by comparing the query's magnitude against stored pattern scales. It allocates massive precision weights to masked/missing dimensions, forcing the network's gradient dynamics to rapidly refill the missing signal.
* **Regime 2: Geometry (Near-Clean Probes)**
  * *Trigger:* Confidence $\ge 0.90$
  * *Mechanism:* Operates near the true equilibrium state. It calculates the live Hessian matrix $H$ and determines the optimal diagonal preconditioner to minimize the eigenvalue spread (condition number) of $\Pi^{1/2} H \Pi^{1/2}$, resolving the objective via subgradient projection.

### 2. The Application Layer
To make this heavy computational engine accessible and visual, the architecture incorporates a robust web layer:
* **The Python Harness:** Executes the `bench-p04-pcam` evaluations natively.
* **The API Gateway:** An Express.js Node server that safely spawns Python child processes. It monitors the execution stream, intercepts the terminal `stdout`, and uses regex to parse the raw evaluation metrics (Accuracy, Anisotropy Spread, and Points) into a clean JSON payload.
* **The Cinematic Presentation:** A Vite + React frontend built to handle asynchronous long-polling gracefully. It visualizes the complex Python metrics via a scroll-driven, 3D-integrated web interface.

---

## 💻 Tech Stack

### Artificial Intelligence & Data Science
* **Python 3**: Core algorithm execution.
* **NumPy**: High-performance, deterministic array and matrix operations for the Hessian and precision maps.
* **PCAM Framework**: The benchmark harness used to score and inject noise into the synthetic memory patterns.

### Backend Gateway
* **Node.js & Express.js**: Lightweight, non-blocking API server bridging the web client and the local Python processes.
* **Child Process Execution (`exec`)**: Spawns and manages the 70+ second Python benchmark jobs directly from the OS.

### Frontend Application
* **React 19 & Vite**: Lightning-fast component rendering and local development environment.
* **Framer Motion**: Drives the physics-based spring counters, scroll-triggered reveals (`whileInView`), and continuous SVG transformation loops.
* **Lenis**: Overrides native browser scrolling to provide a buttery-smooth, interpolated timeline that enhances the physical "weight" of the site.
* **Spline 3D (`@splinetool/react-spline`)**: Integrates a live, interactive WebGL 3D scene natively into the React tree without requiring heavy custom Three.js implementations.
* **Vanilla CSS**: Strict, design-token-based styling (`#0A0A0A` dark modes, `Playfair Display` typography) prioritizing editorial aesthetics over utility frameworks.

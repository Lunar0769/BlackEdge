"""
Flask Web Server for BlackEdge
Streams agent outputs in real-time via Server-Sent Events (SSE)
"""
import json
import time
import threading
from flask import Flask, render_template, request, Response, jsonify
from memory.feedback_manager import FeedbackManager

app = Flask(__name__)

# Global lock to ensure only one query is processed at a time
analysis_lock = threading.Lock()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Stream market analysis results step-by-step via SSE."""
    data = request.get_json()
    query = (data or {}).get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    def generate():
        yield _sse("step", {"step": "rag", "status": "loading", "label": "⏳ Waiting in queue for other analysis to finish…"})
        
        with analysis_lock:
            try:
                # --- Step 1: RAG ---
                yield _sse("step", {"step": "rag", "status": "loading", "label": "📚 Loading market context…"})
                from rag.vector_store import build_vector_store
                from rag.retriever import retrieve_history
                vectorstore = build_vector_store()
                rag_context = retrieve_history(vectorstore, query)
                yield _sse("step", {"step": "rag", "status": "done", "label": "📚 Market context loaded", "content": rag_context})

                # --- Step 2: Researcher ---
                yield _sse("step", {"step": "researcher", "status": "loading", "label": "🔍 Researcher analysing…"})
                from memory.feedback_manager import FeedbackManager
                feedback_manager = FeedbackManager()
                adaptive_prompt = feedback_manager.generate_adaptive_prompt()
                state = {
                    "query": query,
                    "context": f"{query}\n\nMarket History Context:\n{rag_context}",
                    "adaptive_prompt": adaptive_prompt,
                }
                from agents.researcher import researcher_node
                state = researcher_node(state)
                yield _sse("step", {"step": "researcher", "status": "done", "label": "🔍 Research complete", "content": state["research"]})

                # --- Step 3: Analyst ---
                yield _sse("step", {"step": "analyst", "status": "loading", "label": "📈 Analyst processing…"})
                from agents.analyst import analyst_node
                state = analyst_node(state)
                yield _sse("step", {"step": "analyst", "status": "done", "label": "📈 Analysis complete", "content": state["analysis"]})

                # --- Step 4: Trader ---
                yield _sse("step", {"step": "trader", "status": "loading", "label": "💰 Trader deciding…"})
                from agents.trader import trader_node
                state = trader_node(state)
                yield _sse("step", {"step": "trader", "status": "done", "label": "💰 Decision made", "content": state["decision"]})

                # --- Step 5: Critic ---
                yield _sse("step", {"step": "critic", "status": "loading", "label": "🎯 Critic evaluating…"})
                from agents.critic import CriticAgent
                critic = CriticAgent()
                decision = state.get("final_decision", state.get("decision", "No decision"))
                evaluation = critic.evaluate(query, decision, state)
                state["evaluation"] = evaluation
                state["critic_score"] = evaluation["score"]

                # Log if low score
                if evaluation["score"] < 7:
                    feedback_manager.log_failure(evaluation)

                yield _sse("step", {"step": "critic", "status": "done", "label": "🎯 Evaluation complete", "content": json.dumps(evaluation)})

                # --- Final result ---
                yield _sse("result", {
                    "research": state.get("research", ""),
                    "analysis": state.get("analysis", ""),
                    "decision": state.get("decision", ""),
                    "evaluation": evaluation,
                    "critic_score": evaluation["score"],
                })

            except Exception as e:
                yield _sse("error", {"message": str(e)})

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/memory")
def memory():
    """Return recent mistakes and common weaknesses."""
    fm = FeedbackManager()
    return jsonify({
        "recent_mistakes": fm.get_recent_mistakes(5),
        "common_weaknesses": fm.get_common_weaknesses(),
    })


@app.route("/api/clear_memory", methods=["POST"])
def clear_memory():
    fm = FeedbackManager()
    fm.clear_logs()
    return jsonify({"status": "cleared"})


def _sse(event: str, data: dict) -> str:
    """Format a Server-Sent Event string."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)

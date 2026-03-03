from rag.vector_store import build_vector_store
from rag.retriever import retrieve_history
from agents.researcher import researcher_node
from agents.analyst import analyst_node
from agents.trader import trader_node
from agents.critic import CriticAgent
from memory.feedback_manager import FeedbackManager

CRITIC_THRESHOLD = 7  # Score below this triggers feedback logging


def run_workflow(query: str, enable_critic: bool = True, retry_on_failure: bool = True):
    """
    Enhanced workflow with critic evaluation and feedback loop

    Args:
        query: Investment question
        enable_critic: Whether to run critic evaluation
        retry_on_failure: Whether to retry if critic score < threshold
    """
    feedback_manager = FeedbackManager()
    critic = CriticAgent()

    # Inject adaptive prompt from past mistakes
    adaptive_prompt = feedback_manager.generate_adaptive_prompt()

    # Build RAG vector store and retrieve relevant market history
    vectorstore = build_vector_store()
    rag_context = retrieve_history(vectorstore, query)

    state = {
        "query": query,
        "context": f"{query}\n\nMarket History Context:\n{rag_context}",
        "adaptive_prompt": adaptive_prompt,
    }

    # Execute main workflow
    state = researcher_node(state)
    state = analyst_node(state)
    state = trader_node(state)

    # Critic evaluation
    if enable_critic:
        decision = state.get('final_decision', state.get('trader_output', 'No decision'))
        evaluation = critic.evaluate(query, decision, state)

        state['evaluation'] = evaluation
        state['critic_score'] = evaluation['score']

        # Log failures
        if evaluation['score'] < CRITIC_THRESHOLD:
            feedback_manager.log_failure(evaluation)

            # Optional: Retry with enhanced context
            if retry_on_failure and not state.get('is_retry', False):
                print(f"\n Low critic score ({evaluation['score']}/10). Retrying with enhanced context...\n")
                state['is_retry'] = True
                state['context'] += f"\n\nPREVIOUS ATTEMPT WEAKNESSES:\n{evaluation['summary']}\n"

                state = researcher_node(state)
                state = analyst_node(state)
                state = trader_node(state)

                # Re-evaluate
                decision = state.get('final_decision', state.get('trader_output', 'No decision'))
                evaluation = critic.evaluate(query, decision, state)
                state['evaluation'] = evaluation
                state['critic_score'] = evaluation['score']

    return state
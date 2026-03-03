from workflow.graph import run_workflow
from rate_limiter import RateLimiter


def main():
    print("\n" + "="*60)
    print("🔥 BlackEdge - AI Market Intelligence")
    print("="*60)
    print("Self-Correcting Market Analysis System")
    print("⏱️  Rate Limit: 1 analysis per 30 minutes")
    print("="*60 + "\n")
    
    # Rate limiting check
    limiter = RateLimiter()
    can_proceed, remaining_minutes = limiter.can_proceed()
    
    if not can_proceed:
        print("⏳ RATE LIMIT REACHED")
        print(f"Please wait {remaining_minutes} more minutes before your next analysis.")
        print(f"Demo version allows 1 analysis per 30 minutes.\n")
        return

    query = input("Enter your market question: ").strip()

    if not query:
        print("Query cannot be empty.")
        return

    try:
        # Record usage
        limiter.record_usage()
        
        print("\n🔄 Analyzing... This may take a moment.\n")
        
        result = run_workflow(query, enable_critic=True, retry_on_failure=True)

        print("\n" + "="*60)
        print("📊 RESEARCH")
        print("="*60)
        print(result.get("research", "No research output."))

        print("\n" + "="*60)
        print("📈 ANALYSIS")
        print("="*60)
        print(result.get("analysis", "No analysis output."))

        print("\n" + "="*60)
        print("💰 DECISION")
        print("="*60)
        print(result.get("decision", "No decision output."))
        
        # Show critic evaluation
        if 'evaluation' in result:
            evaluation = result['evaluation']
            print("\n" + "="*60)
            print("🎯 CRITIC EVALUATION")
            print("="*60)
            print(f"Score: {evaluation['score']}/10")
            print(f"Summary: {evaluation['summary']}")
            
            if evaluation.get('weaknesses'):
                print("\n⚠️ Weaknesses:")
                for w in evaluation['weaknesses']:
                    print(f"  - {w}")
            
            if evaluation.get('recommendations'):
                print("\n💡 Recommendations:")
                for r in evaluation['recommendations']:
                    print(f"  - {r}")
        
        print("\n" + "="*60)
        print("⏱️  Next analysis available in 30 minutes")
        print("="*60 + "\n")

    except Exception as e:
        print("\n[ERROR]")
        print(str(e))


if __name__ == "__main__":
    main()

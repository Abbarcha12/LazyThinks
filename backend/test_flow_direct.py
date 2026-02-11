import os
from dotenv import load_dotenv
load_dotenv()

from utils import generate_proposal_multiagent_flow

def test_flow():
    job_desc = "Seeking a Senior AI Engineer to build a RAG-based chatbot. Must have experience with Pinecone, LangChain, and Groq."
    print("Starting multi-agent flow...")
    try:
        from proposal_agents import create_proposal_agents
        from a2a_protocol import protocol
        
        conversation_id = protocol.create_conversation()
        print(f"Conversation ID: {conversation_id}")
        
        from utils import process_job_and_generate_proposal
        print("Extracting job details...")
        extraction_result = process_job_and_generate_proposal(job_description=job_desc)
        job_details = extraction_result["job_details"]
        print(f"Extracted Role: {job_details.get('role')}")

        agents = create_proposal_agents()
        print("Writer starting...")
        writer_res = agents["writer"].write_initial_proposal(conversation_id, job_details)
        draft = writer_res["draft"]
        print(f"Draft written ({len(draft)} chars)")

        print("Reviewer starting...")
        review_res = agents["reviewer"].review_proposal(conversation_id, draft, job_details)
        print(f"Review score: {review_res.get('scores', {}).get('overall')}")

        print("Optimizer starting...")
        optimizer_res = agents["optimizer"].optimize_proposal(conversation_id, draft, review_res)
        final_proposal = optimizer_res["final_proposal"]
        print(f"✅ FLOW SUCCESSFUL. Final Proposal length: {len(final_proposal)}")
        print("\n--- FINAL PROPOSAL ---\n")
        print(final_proposal)
        print("\n-----------------------\n")
        
    except Exception as e:
        print(f"❌ FLOW FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_flow()

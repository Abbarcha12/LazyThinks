"""
Agent-to-Agent (A2A) Communication Protocol
Handles message routing and conversation management between agents
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid


class AgentMessage(BaseModel):
    """Message structure for agent communication"""
    message_id: str
    conversation_id: str
    sender: str  # Agent name
    receiver: str  # Agent name or "all"
    message_type: str  # "REQUEST", "RESPONSE", "CONSENSUS", "FINAL_DECISION"
    data: Dict
    timestamp: datetime
    parent_message_id: Optional[str] = None


class A2AProtocol:
    """
    Agent-to-Agent Protocol Handler
    Manages communication between agents in the multi-agent system
    """
    
    def __init__(self):
        self.conversations: Dict[str, List[AgentMessage]] = {}
        self.agents: Dict[str, 'BaseAgent'] = {}
    
    def register_agent(self, agent_name: str, agent: 'BaseAgent'):
        """Register an agent in the protocol"""
        self.agents[agent_name] = agent
        print(f"✅ Registered agent: {agent_name}")
    
    def create_conversation(self) -> str:
        """Create a new conversation and return its ID"""
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = []
        return conversation_id
    
    def send_message(
        self,
        conversation_id: str,
        sender: str,
        receiver: str,
        message_type: str,
        data: Dict,
        parent_message_id: Optional[str] = None
    ) -> AgentMessage:
        """
        Send a message from one agent to another
        """
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            data=data,
            timestamp=datetime.utcnow(),
            parent_message_id=parent_message_id
        )
        
        # Store message in conversation history
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append(message)
        
        # Deliver message to receiver
        if receiver in self.agents:
            self.agents[receiver].receive_message(message)
        elif receiver == "all":
            # Broadcast to all agents except sender
            for agent_name, agent in self.agents.items():
                if agent_name != sender:
                    agent.receive_message(message)
        
        return message
    
    def get_conversation(self, conversation_id: str) -> List[AgentMessage]:
        """Get full conversation history"""
        return self.conversations.get(conversation_id, [])
    
    def get_messages_for_agent(self, conversation_id: str, agent_name: str) -> List[AgentMessage]:
        """Get all messages sent to or from a specific agent"""
        conversation = self.get_conversation(conversation_id)
        return [
            msg for msg in conversation
            if msg.sender == agent_name or msg.receiver == agent_name or msg.receiver == "all"
        ]
    
    def facilitate_consensus(
        self,
        conversation_id: str,
        agents: List[str],
        topic: str
    ) -> Dict:
        """
        Facilitate consensus building between multiple agents
        Returns agreed findings and disagreements
        """
        # Get all relevant messages
        messages = self.get_conversation(conversation_id)
        
        # Extract agent positions
        positions = {}
        for agent_name in agents:
            agent_messages = [m for m in messages if m.sender == agent_name]
            if agent_messages:
                # Get latest position from agent
                latest = agent_messages[-1]
                positions[agent_name] = latest.data
        
        # Find agreements (simplified - in production, use LLM to analyze)
        agreed_findings = {}
        disagreements = []
        
        # This is a simplified consensus - you can enhance with LLM analysis
        return {
            "agreed_findings": positions,
            "disagreements": disagreements,
            "consensus_reached": len(disagreements) == 0
        }
    
    def format_conversation_for_display(self, conversation_id: str) -> List[Dict]:
        """Format conversation for frontend display"""
        messages = self.get_conversation(conversation_id)
        
        formatted = []
        for msg in messages:
            formatted.append({
                "id": msg.message_id,
                "sender": msg.sender,
                "receiver": msg.receiver,
                "type": msg.message_type,
                "content": msg.data,
                "timestamp": msg.timestamp.isoformat(),
                "parent_id": msg.parent_message_id
            })
        
        return formatted


# Global protocol instance
protocol = A2AProtocol()

import streamlit as st
import google.generativeai as genai
import os
from typing import Optional

# Configure Gemini API


 # Replace with your actual Gemini API key



genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize the model properly

class CodeBuddy:
    @staticmethod
    def analyze_code(code: str) -> str:
        """Analyze code with friendly feedback"""
        prompt = f"""
        Hey Gemini! Could you help me review this code? I'd appreciate:
        - A friendly assessment of the code structure
        - Any potential gotchas or edge cases I might have missed
        - Performance tips in simple terms
        - Security check in plain English
        - Suggestions for improvement with examples
        
        Here's the code I'm working on:
        ```python
        {code}
        ```
        """
        return CodeBuddy._chat_with_gemini(prompt)
    
    @staticmethod
    def generate_code(description: str, language: str = "python") -> str:
        """Generate code with beginner-friendly explanations"""
        prompt = f"""
        Hello! Could you create some {language} code for me? Here's what I need:
        {description}
        
        Please:
        - Write it like you're teaching a friend
        - Add smiley-face comments for complex parts
        - Show me how to use it with a real example
        - Help me handle common mistakes gracefully
        - Bonus points for a quick test example!
        """
        return CodeBuddy._chat_with_gemini(prompt)
    
    @staticmethod
    def explain_code(code: str) -> str:
        """Explain code in simple terms"""
        prompt = f"""
        Can you break this down for me like I'm new to coding?
        ```python
        {code}
        ```
        
        I'd love to understand:
        - What the big picture is
        - How different parts work together
        - Any cool patterns or tricks used
        - What goes in/comes out
        - How it plays with other components
        """
        return CodeBuddy._chat_with_gemini(prompt)
    
    @staticmethod
    def debug_code(code: str, error: Optional[str] = None) -> str:
        """Debug with empathy"""
        prompt = f"""
        I'm stuck with this code 😅
        Here's what's happening: {error if error else "Unexpected behavior"}
        
        Could you:
        1. Tell me what's wrong in plain English
        2. Explain why it's happening
        3. Show the fix with before/after comparison
        4. Share a pro tip to avoid this next time
        5. Give me a virtual high-five if it's an easy fix 🙌
        
        My code:
        ```python
        {code}
        ```
        """
        return CodeBuddy._chat_with_gemini(prompt)
    
    @staticmethod
    def _chat_with_gemini(prompt: str) -> str:
        """Have natural conversation with Gemini"""
        try:
            response = model.generate_content(prompt)
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            return "Hmm, I'm having trouble with that. Could you try rephrasing?"
        except Exception as e:
            return f"Whoops! Something went sideways: {str(e)}"

def understand_user_request(user_input: str) -> tuple:
    """Natural language understanding with common phrases"""
    lower_input = user_input.lower()
    
    conversation_triggers = {
        "debug": ["fix", "error", "why isn't", "not working", "help with", "bug"],
        "explain": ["how does", "what does", "explain", "break down", "teach me"],
        "analyze": ["review", "check my", "look at", "feedback on", "```"],
        "generate": ["create", "write", "how to", "make a", "generate"]
    }
    
    for tool, phrases in conversation_triggers.items():
        if any(phrase in lower_input for phrase in phrases):
            return tool, user_input if tool == "analyze" else None
    return "analyze", user_input  # Default to code review

def handle_conversation(user_input: str) -> str:
    """Manage natural coding conversation"""
    tool, context = understand_user_request(user_input)
    
    try:
        if tool == "analyze":
            return CodeBuddy.analyze_code(context or user_input)
        elif tool == "generate":
            return CodeBuddy.generate_code(user_input)
        elif tool == "explain":
            return CodeBuddy.explain_code(user_input)
        elif tool == "debug":
            if "error:" in user_input.lower():
                code_part, _, error_part = user_input.partition("error:")
                return CodeBuddy.debug_code(code_part.strip(), error_part.strip())
            return CodeBuddy.debug_code(user_input)
        return "Let me think about that... Could you rephrase your request?"
    except Exception as e:
        return f"Yikes! I tripped over myself: {str(e)}"

def main():
    st.set_page_config(page_title="CodingMitra - Your Code Buddy! ", page_icon="💻")
    st.title(" 💻 CodingMitra - Your Code Buddy! ")
    st.caption("Your friendly neighborhood coding assistant - Let's build something awesome!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Hi! I'm CodingMitra 🎉\n\nYou can:\n- Ask for code help\n- Paste code for review\n- Request explanations\n- Get debugging help\n\nTry something like:\n\"Can you check this Python function?\"\n\"How do I make a REST API in Go?\"\n\"Why is my loop infinite?\"\n\nLet's code!"
        })
    
    # Display conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Type your code or question here..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Let me think..."):
                try:
                    response = handle_conversation(user_input)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    oops_msg = f"⚠️ Oops! Let's try that again: {str(e)}"
                    st.markdown(oops_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": oops_msg})

if __name__ == "__main__":
    main()


# Footer
with st.sidebar:
    st.markdown("---")
    st.markdown(
        '<div class="footer">Built with Streamlit • Powered by Google Gemini<br>Developed by Amresh Yadav • maithiligeek@gmail.com</div>',
        unsafe_allow_html=True
    )

import os
import sqlite3
from dotenv import load_dotenv
from google import genai
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_rules = """
Act as a Receptionist for Heeramoti Jewelers. 
CRITICAL RULES:
1. Answer the customers politely. 
2. ONLY greet the customer on the very first message.
3. Don't answer blindly about prices, delivery dates, or custom orders.
4. NEVER tell the customer what you "can" or "cannot" check. If the inventory tool says 0 or returns an error, simply tell the customer we do not carry that item in plain, natural English.
5. LEAD GENERATION PROTOCOL: If a customer asks for a custom order, you MUST follow these exact steps in order:
   - STEP 1: Ask the customer for their Name AND Phone Number. DO NOT use the save_lead tool yet.
   - STEP 2: Wait for the customer to reply.
   - STEP 3: If they provide both, use the save_lead tool. If they provide a name but explicitly refuse to give a number, politely accept their decision and use the save_lead tool.
6. Policy Check: If a customer asks about returns, warranties, diamond certifications, or store rules, check the check store policy tool. 
"""

def check_store_policy():
    """
    Use this tool whenever a customer asks about returns, warranties, diamond certifications, or store rules.
    """
    with open ("policies.txt", "r") as file:
        policy_content = file.read()
        return policy_content

conn = sqlite3.connect("chat_history.db", check_same_thread = False)
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS messages(
    user_id TEXT,
    role TEXT,
    content TEXT)"""
)
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS leads(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_name TEXT,
                   phone_number TEXT)
                   """)
conn.commit()


def check_inventory(item_name : str):
    """
    Check the store database for the stock count of any jewelry item the customer asks about.
    """     
    stock = {
        "gold_chain" : 5,
        "diamond_ring" : 2
    }

    return f"Stock count: {stock.get(item_name, '0')}"

def save_lead(customer_name : str, phone_number : str = "Refused"):
    """
    Use this tool ONLY when a customer explicitly asks for a custom order, 
    wants a callback, or provides their contact information.
    """
    cursor.execute("INSERT INTO leads(customer_name, phone_number) VALUES(?,?)",
                   (customer_name, phone_number))
    conn.commit()

    # --- NEW WEBHOOK ENGINE ---
    alert_message = f"🚨 **NEW HIGH-TICKET LEAD!** 🚨\n**Name:** {customer_name}\n**Phone:** {phone_number}\n*Check the database for full details.*"

    payload = {
        "content" : alert_message
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Webhook failed: {e}") # Fails silently so it doesn't crash the bot
    # --------------------------
    return "Lead successfully saved to database and sales team notified. Thank the customer."

def get_ai_response(user_id, content):

    chat_history = ""

    cursor.execute("INSERT INTO messages(user_id, role, content) VALUES(?,?,?)",
                   (user_id, "user", content)
                   )
    conn.commit()

    # Grab the 6 most recent messages (backwards)
    cursor.execute("SELECT role, content FROM messages WHERE user_id=? ORDER BY rowid DESC LIMIT 6",
                    (user_id,)
    )
    all_chat_history = cursor.fetchall()
    # Flip them back to chronological order (oldest to newest)
    all_chat_history.reverse()

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents= f"Follow the {system_rules} while answering to the customer, this is the message from the user {content}, and for your referance this is the chat history of the customer {all_chat_history}",
        config={'tools':[check_inventory, save_lead, check_store_policy]}
    )

    cursor.execute("INSERT INTO messages (user_id, role, content) VALUES(?,?,?)",
                    (user_id, "assistant", response.text))
    conn.commit()

    return (response.text)

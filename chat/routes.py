from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_socketio import emit
from models import Chat, Message, db
from datetime import datetime
import openai
import os

chat = Blueprint('chat', __name__)

@chat.route('/chat')
@login_required
def chat_home():
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).all()
    return render_template('chat/home.html', chats=chats)

@chat.route('/chat/new', methods=['POST'])
@login_required
def new_chat():
    new_chat = Chat(title="New Chat", user_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'chat_id': new_chat.id})

@chat.route('/chat/<int:chat_id>')
@login_required
def chat_detail(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return "Unauthorized", 403
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    return render_template('chat/detail.html', chat=chat, messages=messages)

@chat.route('/chat/<int:chat_id>/message', methods=['POST'])
@login_required
def send_message(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return "Unauthorized", 403
        
    content = request.json.get('content')
    if not content:
        return "Message content is required", 400
        
    message = Message(
        content=content,
        chat_id=chat_id,
        user_id=current_user.id
    )
    db.session.add(message)
    db.session.commit()
    
    # Get AI response
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": content}
            ]
        )
        ai_response = response.choices[0].message.content
        
        # Save AI response
        ai_message = Message(
            content=ai_response,
            chat_id=chat_id,
            is_bot=True
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            'user_message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat()
            },
            'ai_message': {
                'id': ai_message.id,
                'content': ai_message.content,
                'timestamp': ai_message.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting AI response: {str(e)}")
        return jsonify({
            'user_message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat()
            },
            'error': 'Failed to get AI response'
        })

from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# HTML template for the game
GAME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock Paper Scissors</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .game-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .choices {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .choice-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 20px 30px;
            border-radius: 15px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 120px;
        }
        .choice-btn:hover {
            background: #5a67d8;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .result-section {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 15px;
        }
        .choices-display {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .choice-display {
            text-align: center;
            margin: 10px;
        }
        .choice-emoji {
            font-size: 4em;
            margin-bottom: 10px;
        }
        .vs {
            font-size: 2em;
            font-weight: bold;
            color: #666;
        }
        .result-text {
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
        }
        .win { color: #28a745; }
        .lose { color: #dc3545; }
        .tie { color: #ffc107; }
        .score-board {
            background: #e9ecef;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }
        .score {
            display: flex;
            justify-content: space-around;
            font-size: 1.2em;
            font-weight: bold;
        }
        .reset-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            margin-top: 20px;
            transition: background 0.3s ease;
        }
        .reset-btn:hover {
            background: #c82333;
        }
        .rules {
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 0.9em;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🎮 Rock Paper Scissors</h1>
        
        <div class="rules">
            <strong>Rules:</strong> Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        </div>
        
        <div class="score-board">
            <h3>Score Board</h3>
            <div class="score">
                <div>You: {{ session.get('user_score', 0) }}</div>
                <div>Computer: {{ session.get('computer_score', 0) }}</div>
            </div>
        </div>
        
        {% if not result %}
        <h2>Choose your weapon:</h2>
        <div class="choices">
            <form method="POST" style="display: inline;">
                <input type="hidden" name="choice" value="rock">
                <button type="submit" class="choice-btn">🪨 Rock</button>
            </form>
            <form method="POST" style="display: inline;">
                <input type="hidden" name="choice" value="paper">
                <button type="submit" class="choice-btn">📄 Paper</button>
            </form>
            <form method="POST" style="display: inline;">
                <input type="hidden" name="choice" value="scissors">
                <button type="submit" class="choice-btn">✂️ Scissors</button>
            </form>
        </div>
        {% else %}
        <div class="result-section">
            <div class="choices-display">
                <div class="choice-display">
                    <div class="choice-emoji">{{ user_emoji }}</div>
                    <div><strong>You</strong></div>
                    <div>{{ user_choice.title() }}</div>
                </div>
                <div class="vs">VS</div>
                <div class="choice-display">
                    <div class="choice-emoji">{{ computer_emoji }}</div>
                    <div><strong>Computer</strong></div>
                    <div>{{ computer_choice.title() }}</div>
                </div>
            </div>
            
            <div class="result-text {{ result_class }}">
                {{ result_message }}
            </div>
        </div>
        
        <div class="choices">
            <a href="{{ url_for('game') }}" class="choice-btn">🎮 Play Again</a>
        </div>
        {% endif %}
        
        <form method="POST" action="{{ url_for('reset_game') }}" style="display: inline;">
            <button type="submit" class="reset-btn">🔄 Reset Score</button>
        </form>
    </div>
</body>
</html>
'''

def get_choice_emoji(choice):
    """Return emoji for the choice"""
    emojis = {
        'rock': '🪨',
        'paper': '📄',
    }
    return emojis.get(choice, '❓')

def determine_winner(user_choice, computer_choice):
    """Determine the winner of the game"""
    if user_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    if winning_combinations[user_choice] == computer_choice:
        return 'win'
    else:
        return 'lose'

@app.route('/')
def game():
    """Main game route"""
    # Initialize session scores if they don't exist
    if 'user_score' not in session:
        session['user_score'] = 0
    if 'computer_score' not in session:
        session['computer_score'] = 0
    
    return render_template_string(GAME_TEMPLATE)

@app.route('/', methods=['POST'])
def play_game():
    """Handle game play"""
    user_choice = request.form.get('choice')
    
    if user_choice not in ['rock', 'paper', 'scissors']:
        return redirect(url_for('game'))
    
    # Generate computer choice
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    
    # Determine winner
    result = determine_winner(user_choice, computer_choice)
    
    # Update scores
    if result == 'win':
        session['user_score'] = session.get('user_score', 0) + 1
        result_message = "🎉 You Win!"
        result_class = "win"
    elif result == 'lose':
        session['computer_score'] = session.get('computer_score', 0) + 1
        result_message = "😔 You Lose!"
        result_class = "lose"
    else:
        result_message = "🤝 It's a Tie!"
        result_class = "tie"
    
    return render_template_string(GAME_TEMPLATE,
                                result=True,
                                user_choice=user_choice,
                                computer_choice=computer_choice,
                                user_emoji=get_choice_emoji(user_choice),
                                computer_emoji=get_choice_emoji(computer_choice),
                                result_message=result_message,
                                result_class=result_class)

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game scores"""
    session['user_score'] = 0
    session['computer_score'] = 0
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True)

from website import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Quiz, Question, Answer


question = Blueprint('question', __name__)


@question.route('/create-quiz', methods = ['GET','POST'])
def create_quiz():
   if request.method == 'POST':
        subject = request.form['subject']
        question_text = request.form['question']
        choices = request.form.getlist('choices')
        correct_answer = request.form['correct_answer']
        
        
        # Create the quiz
        quiz = Quiz(title=subject, subject=subject, description=f"Quiz on {subject}")
        db.session.add(quiz)
        db.session.commit()
        
        # Create the question
        question = Question(text=question_text, quiz_id=quiz.id)
        db.session.add(question)
        db.session.commit()
        
        # Create the answers
        for choice in choices:
            is_correct = (choice == correct_answer)
            answer = Answer(text=choice, is_correct=is_correct, question_id=question.id)
            db.session.add(answer)
        
        db.session.commit()
        
        return redirect(url_for('question.display_quiz', quiz_id=quiz.id))
    
    
   return render_template('create-quiz.html')
   


@question.route('/result')
def result():
    return render_template('result.html')

@question.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def display_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz=quiz)


@question.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = 0
    total_questions = len(quiz.questions)
    for question in quiz.questions:
        selected_answer_id = request.form.get(f'question_{question.id}')
        selected_answer = Answer.query.get(selected_answer_id)
        if selected_answer and selected_answer.is_correct:
            score += 1
    
    return render_template('result.html', quiz=quiz, score=score, total_questions=total_questions)
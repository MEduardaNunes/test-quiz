import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)

    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a')
    choice = question.choices[0]

    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0

def test_remove_choice_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    choice = question.choices[0]

    with pytest.raises(Exception):
        question.remove_choice_by_id(choice.id + 1)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    choice_a = question.choices[0]
    choice_b = question.choices[1]
    choice_c = question.choices[2]

    assert not choice_a.is_correct
    assert not choice_b.is_correct
    assert not choice_c.is_correct

    question.set_correct_choices([choice_a.id, choice_b.id])

    assert choice_a.is_correct
    assert choice_b.is_correct
    assert not choice_c.is_correct

def test_set_correct_choices_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    choice_a = question.choices[0]
    choice_b = question.choices[1]

    with pytest.raises(Exception):
        question.set_correct_choices([999])

def test_correct_selections_exceed_max():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a')
    question.add_choice('b')
    choice_a = question.choices[0]
    choice_b = question.choices[1]

    with pytest.raises(Exception):
        question.correct_selected_choices([choice_a.id, choice_b.id])

def test_correct_selections_with_valid_choice_id():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    choice_a = question.choices[0]
    choice_b = question.choices[1]

    response = question.correct_selected_choices([choice_a.id, choice_b.id])

    assert response == [1]

def test_correct_selections_with_invalid_choice_id():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)

    response = question.correct_selected_choices([999])

    assert response == []

def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)
    return question

def test_correct_selected_choices_with_multiple_correct(question_with_choices):
    question = question_with_choices
    choice_a = question.choices[0]
    choice_b = question.choices[1]
    choice_c = question.choices[2]

    response = question.correct_selected_choices([choice_a.id, choice_c.id])

    assert response == [1, 3]

def test_correct_selected_choices_with_no_correct(question_with_choices):
    question = question_with_choices
    choice_b = question.choices[1]

    response = question.correct_selected_choices([choice_b.id])

    assert response == []
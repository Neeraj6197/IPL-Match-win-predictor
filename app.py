import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Kolkata', 'Mumbai', 'Raipur', 'Jaipur', 'Visakhapatnam', 'Delhi',
       'Chennai', 'Hyderabad', 'Port Elizabeth', 'Centurion',
       'Dharamsala', 'Bangalore', 'Bengaluru', 'Johannesburg', 'Mohali',
       'Ahmedabad', 'Abu Dhabi', 'Chandigarh', 'Ranchi', 'Durban', 'Pune',
       'Nagpur', 'Indore', 'Sharjah', 'Cape Town', 'Kimberley',
       'Bloemfontein', 'Cuttack', 'East London']

pipe = pickle.load(open('pipe.pkl','rb'))
pipe2 = pickle.load(open('pipe2.pkl','rb'))

st.title('IPL Match Predictor')
st.image('https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/1200px-Indian_Premier_League_Official_Logo.svg.png')
user_input = st.selectbox('Select an option',('1st innings score predictor','Match winning probability predictor'))

if user_input == '1st innings score predictor':
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    selected_city = st.selectbox('Select the city', sorted(cities))

    col3, col4, col5 = st.columns(3)

    with col3:
        current_score = st.number_input('Current Score',1)

    with col4:
        overs = st.number_input('Overs played(works for overs>3)',3,20)

    with col5:
        wickets = st.number_input('Wickets',0,10)

    last_three = st.number_input('Runs scored in last three overs',1)

    if st.button('Predict Score'):
        balls_left = 120 - (overs * 6)
        wickets = 10 - wickets
        crr = current_score/overs

        score_input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                                 'city': [selected_city], 'current_score': [current_score], 'balls_left': [balls_left],
                                 'wickets': [wickets],
                                 'crr': [crr],'last_three' : [last_three]})

        result = pipe2.predict(score_input_df)
        st.header("Predicted Score: " + str(int(result[0])))


if user_input == 'Match winning probability predictor':
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team',sorted(teams))
    with col2:
     bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    selected_city = st.selectbox('Select the city', sorted(cities))

    target = st.number_input('Target',1)

    col3, col4, col5 = st.columns(3)

    with col3:
         score = st.number_input('Score')
    with col4:
      overs = st.number_input('Overs Completed',0.1,20.0)
    with col5:
      wickets = st.number_input('Wickets Lost',0,10)

    if st.button('Predict Probability'):
     runs_left = target - score
     balls_left = 120 - (overs*6)
     wickets = 10 - wickets
     crr = score/overs
     rrr = (runs_left*6)/balls_left

     input_df = pd.DataFrame({'batting_team' : [batting_team], 'bowling_team' : [bowling_team],
                   'city' : [selected_city], 'runs_left' : [runs_left], 'balls_left':[balls_left],
                   'wickets' : [wickets], 'total_runs_x' : [target],
                   'crr':[crr],'rrr':[rrr]})

     result = pipe.predict_proba(input_df)
     loss = result[0][0]
     win = result[0][1]
     st.header(batting_team + "-" + str(round(win*100)) + "%")
     st.header(bowling_team + "-" + str(round(loss*100)) + "%")


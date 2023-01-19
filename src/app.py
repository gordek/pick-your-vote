# from pycaret.classification import load_model, predict_model
import streamlit as st
import sys,hashlib
import logging
import json
import time
from datetime import datetime
import uuid
import secrets
import os


# Updates the active session for a given user
@st.experimental_singleton
def get_active_session(username):
    # return str(uuid.uuid4())
    return secrets.token_urlsafe(16)

@st.experimental_singleton
def init_(*args):
    logging.error("test")
    # Run the initial conditions
    return look_up_keys(*args)    
    
# @st.cache(allow_output_mutation=True)
def look_up_keys(**kwargs):
    config_file = kwargs.get('config_filepath')
    op_type = kwargs.get('op_type',None)
    final_data = kwargs.get('data',None)
    if op_type=='read':
        with open(config_file) as f:
            dta=json.load(f)
        return dta    
    elif op_type=='write':
        with open(config_file,'w') as f:
            json.dump(final_data,f)
    else:
        logging.error("error reading file")
    # for key in args:
    #     if key not in st.session_state:
    #         if key=='run_date':
    #             st.session_state[key] = datetime.today().date().isoformat()
    #         else:
    #             st.session_state[key] = 1
    
def naive_choice(pick:int,xtra=None):
    return
def generate(choice:int,up_data):
    ddate = datetime.today().date().isoformat()
    session_id = st.session_state.session_id
    
    if up_data['session_id']==session_id:
        st.error("Thank you for your response")
    else:
        if ddate == up_data['date']:
            if choice=='yes':
                up_data['data']['yes']+=1
            else:
                up_data['data']['no']+=1
        else:
            up_data['date'] = ddate
            up_data['data']['yes']=1
            up_data['data']['no']=1
        up_data['session_id'] = session_id   
    return up_data
def main():
    t1 = time.time()
    # with streamlit_analytics.track():
    #     st.text_input("Write something")
    #     st.button("Click me")
    session_time = f"{datetime.now().hour}-{datetime.now().minute}"
    session_id = get_active_session(session_time)
    st.session_state.session_id  = session_id

    
    st.sidebar.title("Social Trend Experiment")
    st.sidebar.caption("This is a completely un-biased view of our society. Please pick your choice freely without trying to skew the result")
    st.sidebar.markdown("---")


    st.title('Vote for Today')
    st.write('This is a web app for a random questions pick your answer.')
    
    col1, col2 = st.columns(2)
    left_column, right_column = st.columns(2)
    

    metrics_data = look_up_keys(config_filepath='src/config.json',op_type='read')
    
    with left_column:
        pick_yes = st.button(
        label="YES",
        type="primary",
        on_click=naive_choice,
        args=('yes',None)
        )    
    with right_column:
        pick_no = st.button(
        label="NO",
        type="primary",
        on_click=naive_choice,
        args=('no',None)
        )
    if pick_yes:
        metrics_data = generate('yes',metrics_data)
    elif pick_no:
        metrics_data = generate('no',metrics_data)
    else:
        st.error("you have to make a selection")
    
    look_up_keys(config_filepath='src/config.json',op_type='write',data=metrics_data)
    # print(new_data)
        
    # y_count,n_count = st.session_state['yes'],st.session_state['no']
    y_count,n_count = metrics_data['data']['yes'],metrics_data['data']['no']

    with left_column:
        st.metric(label="Yes Picks", value=f'{int(y_count/(y_count+n_count)*100)}%',
            delta_color="off")
    with right_column:
        st.metric(label="No Picks", value=f'{int(n_count/(y_count+n_count)*100)}%',
            delta_color="off")
    
    # st.sidebar.write(f"Today: {st.session_state['run_date']}")
    st.sidebar.markdown("--------")
    st.sidebar.write(f"Current participation: {y_count+n_count}")
    # st.sidebar.write(f"user: {st.session_state['session_id']}")

    # st.write("## Current Vote Count:",int(y_count+n_count))

    t2 = time.time()
    logging.info(f"time of execution: {(t2-t1)*1e3}")


main()
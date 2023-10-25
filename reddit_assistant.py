

import streamlit as st
import pandas as pd
import random
from utils import get_todays_top_posts, get_top_10_comments, get_comment_thread, generate_gpt_response, submit_reddit_comment
import textwrap





with st.sidebar:
    subreddit_name = st.text_input('Subreddit', 'DungeonsAndDragons')


st.title(f"{subreddit_name} Comment Assistant")

todays_top_posts = get_todays_top_posts(subreddit_name) 

# st.write(todays_top_posts)
if 'page_number' not in st.session_state:
    st.session_state['page_number'] = 0
    
    

if 'comment_thread_text' not in st.session_state:
    st.session_state['comment_thread_text'] = ''
    
    
if 'comment_thread' not in st.session_state:
    st.session_state['comment_thread'] = []
    

last_page = len(todays_top_posts)


post_prev, _ ,post_next = st.columns([3,6, 3])


current_post = todays_top_posts[st.session_state['page_number']]

if post_next.button("Next Post"):
    st.session_state['comment_thread'] = []
    st.session_state['comment_thread_text'] = ''
    
    print(f'next, page_number: {st.session_state["page_number"]}')

    if st.session_state['page_number'] + 1 > last_page:
        st.session_state['page_number'] = 0
    else:
        st.session_state['page_number'] += 1
    current_post = todays_top_posts[st.session_state['page_number']]

    
if post_prev.button("Previous Post"):
    st.session_state['comment_thread'] = []
    st.session_state['comment_thread_text'] = ''
    
    print(f'previous, page_number: {st.session_state["page_number"]}')
    if st.session_state['page_number'] - 1 < 0:
        st.session_state['page_number'] = last_page
    else:
        st.session_state['page_number'] -= 1
    current_post = todays_top_posts[st.session_state['page_number']]

        

print(current_post)
st.write(current_post.title)




if 'post_comments' not in st.session_state:
        st.session_state['post_comments'] = []

    


comment_prev, _ ,comment_next = st.columns([2,8, 2])


top_comments = get_top_10_comments(current_post)


if st.session_state['comment_thread_text'] == '':
    st.session_state['comment_thread'] = None
    comment_thread = None
    comment_threads_tried = []
    depth = 2
    while comment_thread is None:
        comment_thread_to_check = random.sample(top_comments, 1)[0]
        comment_thread = get_comment_thread(comment_thread_to_check, thread=[], depth=depth)
        comment_threads_tried.append(comment_thread_to_check)
        if set(comment_threads_tried) == set(top_comments):
            st.write(f'Failed to find a valid thread for this post at depth {depth}')
            break

    print('comment_thread')
    print(comment_thread)
    

    insert_point = random.randint(depth, len(comment_thread)-1)
    print(f'using insert_point: {insert_point}')
    comment_thread = comment_thread[:insert_point]


    indent = 0
    line_string = ''

    for comment in comment_thread:
        indents = (' ' * indent * 2)
        wrapper = textwrap.TextWrapper(width=100,
                                        initial_indent=indents + '- ',
                                        subsequent_indent=indents + '  ')
        for line in wrapper.wrap(comment.body):
            # print(line)
            line_string += line + '\n'
            # st.write(line)
        indent += 1
    
    st.session_state['comment_thread_text'] = line_string
    st.session_state['comment_thread'] = comment_thread
    
    

st.write(st.session_state['comment_thread_text'])


if "generated" not in st.session_state:
    response = generate_gpt_response(current_post.title, current_post.selftext, st.session_state['comment_thread'])    
    response = response.replace('"', '').replace("'", "")
    st.session_state["generated"] = response
    

regnerate = st.button("Regenerate Response")    

if regnerate:
    response = generate_gpt_response(current_post.title, current_post.selftext, st.session_state['comment_thread'])    
    response = response.replace('"', '').replace("'", "")
    st.session_state["generated"] = response
    
    
# st.title("GPT Response")
text_area = st.text_area('GPT Response', st.session_state["generated"])
# st.button("Generate Regenerate")

if st.button("Submit Comment"):
    submit_reddit_comment(st.session_state['comment_thread'][-1], text_area)
    st.session_state['page_number'] + 1
    st.session_state['comment_thread_text'] = ''
    st.session_state['comment_thread'] = []



    
    
    
import os
from dotenv import load_dotenv
import praw

# Load variables from .env
load_dotenv()

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("REDDIT_USER_AGENT")


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent,
)



def get_todays_top_posts(subreddit_name):
    todays_top_posts = [x for x in list(reddit.subreddit(subreddit_name).top("day")) if x.is_self]
    return todays_top_posts
    


def get_top_10_comments(top_post):
    
    return list(top_post.comments)[:10]
    



def get_comment_thread(comment, thread=[], count=0, depth=3):    
    
    
    for i, sub_comment in enumerate(comment.replies):
        if i == 0:
            thread.append(sub_comment)
            count += 1
            if count>depth:
                thread.insert(0, comment)
                return thread
            
            result = get_comment_thread(sub_comment, thread, count, depth)
            if result:
                return result
            


system_prompt = """
You are a Reddit bot, you are making a comment in a thread on the Dungeons and Dragons subreddit. Your comedic style is similar to Mark Normand, Tom Segura, and Bill Burr. Keep the response to the thread humorous but dry, relevant to the topic, and not too excited.

You will receive the original Reddit post title and body as well as a thread of comments, come up with a funny response to the thread and post it as a comment. The response should be short, no longer than a sentence. Don't repeat the context of the comments, instead offer a direct reply and carry on the conversation.

"""


def setup_prompt(post_title, post_body, comment_thread):
    
    formatted_comments = ''
    for i, c in enumerate(comment_thread, 1):
        formatted_comments += f"""
            COMMENT #{i}:
            {c.body}
            _______________________
            
        """
    final_prompt = f"""

    Post Title: {post_title}
    Post Body: {post_body}

    Comments:
    {formatted_comments}
    """
    return final_prompt
    


import openai

def generate_gpt_response(post_title, post_body, comment_thread):
    
    final_prompt = setup_prompt(post_title, post_body, comment_thread)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt},
            
        ]
    )
    
    return response.choices[0].message.content
    
    
    
def submit_reddit_comment(comment, text):
    replied = comment.reply(text)
    
    print(replied)
    
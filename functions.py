import json
from datetime import datetime
import logging
import os

pipelogger = logging.getLogger('pipeline')


def subcomments(comment, allComments, inst, childof):
  data = {}
  #data['title']=comment.title
  data['institution'] = inst
  data['body']=comment.body
  data['tstamp']=datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
  data['id']=comment.id
  #data['n_comments']=comment.num_comments
  data['score']=comment.score
  data['type']='comment'
  data['childof'] = childof
  #data['voteratio']=comment.upvote_ratio
  allComments.append(json.dumps(data))
  if not hasattr(comment, "replies"):
    replies = comment.comments()
  else:
    replies = comment.replies
  for child in replies:
    subcomments(child, allComments, inst, childof)


def getAll(r, submissionId, inst):
  submission = r.submission(submissionId)
  comments = submission.comments
  data = {}
  data['institution'] = inst
  data['body']=submission.title
  data['tstamp']=datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
  data['id']=submission.id
  data['n_comments']=submission.num_comments
  data['score']=submission.score
  data['type']='headline'
  data['childof'] = ''
  #data['voteratio']=comment.upvote_ratio
  commentsList = [data]
  pipelogger.info("{} comments found.".format(submission.num_comments))
  if comments:
    for comment in comments:
      try:
        subcomments(comment, commentsList, inst, submission.id)
      except:
        pipelogger.error("couldn't extract comments")
  return commentsList



def mkdirs(dirs):
  if not os.path.exists(dirs):
    os.makedirs(dirs)

def dict_from_module(module):
  context = {}
  for setting in dir(module):
    # you can write your filter here
    if setting.islower() and setting.isalpha():
      context[setting] = getattr(module, setting)

  return context

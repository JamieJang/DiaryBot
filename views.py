from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Diary, Writer

import json, re
from datetime import date

def keyboard(request):
	return JsonResponse({
		'type':'buttons',
		'buttons':['읽기','쓰기']
	})

@csrf_exempt
def answer(request):
	json_str = ((request.body).decode('utf-8'))
	received_json_data = json.loads(json_str)
	user = Writer.objects.get_or_create(name=received_json_data['user_key'])[0]
	content = received_json_data['content']

	if content == '읽기':
		return JsonResponse({
			'message':{
				'text':'날짜를 입력하세요 ex)2017.10.28'
			},
		})
	elif content == '쓰기':
		return JsonResponse({
			'message':{
				'text':'다이어리를 작성하세요.'
			},
		})
	else:
		if re.match(r'\d{4}.\d{1,2}.\d{1,2}', content):
			diary_date = list(map(int,content.split('.')))
			diary_date = date(diary_date[0],diary_date[1],diary_date[2])
			diary = Diary.objects.filter(owner=user).filter(date=diary_date)
			if diary:
				context = [str(i+1)+"번째\n"+x.daily for i,x in enumerate(diary)]
				return JsonResponse({
					'message':{
						'text': "\n\n".join(context)
					},
					'keyboard':{
						'type':'buttons',
						'buttons':['읽기','쓰기']
					}
				})
			else:
				return JsonResponse({
					'message':{
						'text': "해당 날짜에 일기를 쓰지 않으셨네요.."
					},
					'keyboard':{
						'type':'buttons',
						'buttons':['읽기','쓰기']
					}
				})
		else:
			Diary.objects.create(owner=user,daily=content)
			return JsonResponse({
				'message':{
					'text':'일기를 저장했어요.'
				},
				'keyboard':{
					'type':'buttons',
					'buttons':['읽기','쓰기']
				}
			})

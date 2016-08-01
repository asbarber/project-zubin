from django.shortcuts import render
from django.http import HttpResponse

def log(msg):
	print "\033[91m", msg, "\033[0m"

# Intro Questions
# -----------------------------------------------------------------------------
GOLDEN_TICKET_QUESTION = {
	'title': 'Enter The Secret Key',
	'acceptor': lambda x: x in ['713760']	
}

UNIVERSITY_QUESTION = {
	'title': 'What university do I attend?',
	'acceptor': lambda x: x.lower() in ['university of michigan']
}

BHASKAR_QUESTION = {
	'title': 'Who did I consistently defeat in a staring contest?',
	'acceptor': lambda x: x.lower() in ['bhaskar']
}

EMAIL_QUESTION = {
	'title': 'What is my school email address?',
	'acceptor': lambda x: x.lower() == 'asbarber@umich.edu'
}

GRADUATE_QUESTION = {
	'title': 'How many semesters do I have left before I graduate?',
	'acceptor': lambda x: x.lower() in ['2', 'two']
}
# -----------------------------------------------------------------------------


# Funny Questions
# -----------------------------------------------------------------------------
HIRE_ME_QUESTION = {
	'title': 'Is this making you want to hire me more?',
	'acceptor': lambda x: x.lower() in ['yes', 'y']
}

NO_REGRETS_QUESTION = {
	'title': 'Are you regretting your commitment to this hunt yet?',
	'acceptor': lambda x: x.lower() in ['no', 'n']
}
# -----------------------------------------------------------------------------


# Intro Interactive Questions
# -----------------------------------------------------------------------------
ASCII_QUESTION = {
	'title': 'What is next in the sequence?',
	'hint': 'You should probably check your charset.',
	'subtitle': '90, 117, 98, 105, ...',
	'acceptor': lambda x: x.lower() in ['110']
}

CS_QUESTION = {
	'title': 'What\'s the object-oriented way to become wealthy?',
	'acceptor': lambda x: x.lower() in ['inheritance']
}
# -----------------------------------------------------------------------------

# Social Media Questions
# -----------------------------------------------------------------------------
FACEBOOK_QUESTION = {
	'specialRender': True,
	'template': 'facebook.html',
	'acceptor': lambda x: x.lower() in ['facebookkey']
}

LINKEDIN_QUESTION = {
	'specialRender': True,
	'template': 'linkedin.html',
	'acceptor': lambda x: x.lower() in ['linkedinkey']
}
# -----------------------------------------------------------------------------


# Final Interactive Questions
# -----------------------------------------------------------------------------
DHMIS_QUESTION = {
	'title': 'What color is not the creative color?',
	'subtitle': '<a href=\'https://www.youtube.com/watch?v=9C_HReR_McQ\' target=\'_blank\'>Watch the video!</a>',
	'acceptor': lambda x: x.lower() in ['green']
}

COMMENT_QUESTION = {
	'title': 'Find the key hidden in this page.',
	'subtitle': '<!-- Key: 1337H4X -->',
	'acceptor': lambda x: x in ['1337H4X']
}

NAME_QUESTION = {
	'title': 'What is your name?',
	'acceptor': lambda x: x.lower() in ['zubin']
}

TROPHY = {
	'specialRender': True,
	'template': 'trophy.html'
}
# -----------------------------------------------------------------------------


# Setup
# -----------------------------------------------------------------------------
NUM_KEYS = 14
CHALLENGES = [
	GOLDEN_TICKET_QUESTION,
	TROPHY,
	GRADUATE_QUESTION,
	EMAIL_QUESTION,
	BHASKAR_QUESTION,

	HIRE_ME_QUESTION,
	NO_REGRETS_QUESTION,

	ASCII_QUESTION,
	CS_QUESTION,

	FACEBOOK_QUESTION,
	LINKEDIN_QUESTION,

	DHMIS_QUESTION,
	COMMENT_QUESTION,
	NAME_QUESTION,

	# TROPHY
]

# Default constructor
for i, question in enumerate(CHALLENGES):
	if not 'template' in question:
		question['template'] = 'base_challenge.html'
	if not 'specialRender' in question:
		question['specialRender'] = None
	question['key'] = 'key' + str(i+1)
	question['failMessage'] = 'Key ' + str(i+1) + ' is invalid'
# -----------------------------------------------------------------------------


# Challenges
# -----------------------------------------------------------------------------
def render_challenge(request, question, keys, isFail):
	if question.get('specialRender'):
		return render(request, question.get('template'), 
			{
				'key': question.get('key'),
				'keys': keys
			}
		)

	return render(request, question.get('template'),
		{
			'title': question.get('title'),
			'subtitle': question.get('subtitle'),
			'hint': question.get('hint'),
			'key': question.get('key'),
			'keys': keys,
			'failMessage': question.get('failMessage') if isFail else None
		}
	)


def is_challenge_completed(request, keys, id, question):
	keyValue = keys[id-1].get('value')
	isKeyMissing = keyValue == None

	log(keys)

	if isKeyMissing or not question.get('acceptor')(keyValue):
		return render_challenge(request, question, keys, not isKeyMissing)
	else:
		return None


def get_keys(request, numKeys):
	keys = []
	for i in range(numKeys):
		keys.append({
			'name': 'key' + str(i+1),
			'value': request.POST.get('key' + str(i+1))
		})
	return keys
# -----------------------------------------------------------------------------


def index_post(request):
	keys = get_keys(request, NUM_KEYS)

	for i, challenge in enumerate(CHALLENGES):
		challengeResponse = is_challenge_completed(request, keys, i+1, challenge)
		if not challengeResponse == None:
			return challengeResponse

	# Unexpected
	return index_get(request)
	

def index_get(request):
	return is_challenge_completed(request, get_keys(request, NUM_KEYS), 1, GOLDEN_TICKET_QUESTION)


def index(request):
	if request.method == 'GET':
		return index_get(request)
	if request.method == 'POST':
		return index_post(request)

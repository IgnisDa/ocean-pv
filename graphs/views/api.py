from django.http import JsonResponse

from interactions.models import SelfAnswerGroup


def update_accuracy(request):
    if request.method == 'GET' or request.is_ajax():
        accuracy = float(request.GET.get('accuracy'))
        pk = request.GET.get('pk')
        if not 0 <= accuracy <= 100:
            response = {
                'error': True,
                'remove': False,
                'message': 'Please enter a valid percentage'
            }
            return JsonResponse(response)
        answer_group = SelfAnswerGroup.objects.get(pk=pk)
        if answer_group.accuracy:
            response = {
                'error': True,
                'remove': True,
                'message': 'You have already provided feedback for this test'
            }
            return JsonResponse(response)
        answer_group.accuracy = accuracy
        answer_group.save()
        response = {
            'error': False,
            'remove': True,
            'message': 'Your feedback has been saved successfully!'
        }
        return JsonResponse(response)

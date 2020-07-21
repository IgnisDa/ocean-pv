from interactions.models import SelfAnswerGroup, RelationAnswerGroup


def get_home_context():
    self_count = SelfAnswerGroup.objects.all().count()
    relation_count = RelationAnswerGroup.objects.all().count()
    total = self_count+relation_count
    data = {
        'tests_attempted': {'data_to': total, 'data_speed': 5000},
        'peers_invited': {'data_to': relation_count, 'data_speed': 5000},
    }
    return data

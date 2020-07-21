from interactions.models import SelfAnswerGroup


def clean_multiple_results_data(master_pk: int, *primary_keys: list) -> tuple:
    """ Takes in the form submitted in ``multiple_result_view`` and cleans it
    by removing all the duplicate IDs and invalid IDs. Then returns a json list
    containing only the valid IDs (the ones present in database). """

    primary_keys = list(
        int(primary_key) for
        primary_key in primary_keys if primary_key.strip().isdigit()
    )
    primary_keys.append(master_pk.pk)
    valid_pks, unavailable_pks, duplicate_pks = set(), set(), set()
    for primary_key in primary_keys:
        if primary_key in [
            ans_gp['pk'] for ans_gp in SelfAnswerGroup.objects.values('pk')
        ]:
            if primary_key not in valid_pks:
                valid_pks.add(primary_key)
            else:
                duplicate_pks.add(primary_key)
        else:
            if primary_key not in unavailable_pks:
                unavailable_pks.add(primary_key)
            else:
                duplicate_pks.add(primary_key)

    another = list()
    for pk in valid_pks:
        ans_gp = SelfAnswerGroup.objects.get(pk=pk)
        master_bool = True if pk is int(master_pk.pk) else False
        another.append({
            'name': ans_gp.self_user_profile.user.username,
            'master': master_bool,
            'answer_group_pk': pk
        })

    return another, unavailable_pks, duplicate_pks

import plotly.graph_objects as go
from plotly.offline import plot


OCEAN_SUBCLASSES = [
    'Openness', 'Conscientiousness',
    'Extraversion', 'Agreeableness', 'Neuroticism'
]


def draw_plot(valid_dict: dict) -> str:

    score_list = []
    tag_list = []
    for dictionary in valid_dict:
        score_list.append([dictionary['score'][subclass]
                           for subclass in dictionary['score']])
        tag = f"{dictionary['name']}"
        if len(tag) > 10:
            tag = f"{tag[:10]}..."
        tag_list.append(
            f"{dictionary['answer_group_pk']}: {tag}"
        )

    fig = go.Figure()
    for score, legend_tag in zip(score_list, tag_list):
        fig.add_trace(go.Scatterpolar(
            r=score,
            theta=OCEAN_SUBCLASSES,
            fill='toself',
            connectgaps=True,
            name=legend_tag,
            # visible='legendonly', # confuses users where their graph is
        ))

    max_num = 0
    min_num = 0
    for score in score_list:
        if max_num < max(score):
            max_num = max(score)
        if min_num > min(score):
            min_num = min(score)

    max_num = round(max_num + 5.1, -1)
    min_num = round(min_num - 5.1, -1)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[min_num, max_num]
            )),
        showlegend=True,
        legend=dict(x=1.15, y=0.8, title='Test ID: Name'),
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="#5a2f7c"
        )
    )
    return plot(
        fig, output_type='div',
        auto_open=False, image_filename='ocean_plot',
    )


def draw_comparison_plot(valid_dict: list) -> str:
    """ Create a comparison_plot which is displayed in ``comparison_view``.
    It is a bar graph and has is plotted with ``OCEAN_SUBCLASSES`` on x-axis
    and corresponding values on y-axis. """

    actual_scores = list(valid_dict[0]['score'].values())
    deviations = list(valid_dict[1]['deviation'].values())
    guesses = list(valid_dict[1]['score'].values())

    def deviation_percentage(score, guess):
        deviation = guess-score
        if deviation == 0:
            return "Perfect!"
        return f"{deviation}"

    percentages = list(
        deviation_percentage(score, guess) for
        score, guess in zip(actual_scores, guesses)
    )
    print(actual_scores, guesses, percentages)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=OCEAN_SUBCLASSES,
        y=actual_scores,
        name='Their actual personality',
    ))
    fig.add_trace(go.Bar(
        x=OCEAN_SUBCLASSES,
        y=guesses,
        name='Your guess',
    ))
    fig.add_trace(go.Bar(
        x=OCEAN_SUBCLASSES,
        y=deviations,
        name='Deviation with error percent',
        text=percentages,
        textposition='outside',
    ))
    fig.update_layout(barmode='group', showlegend=True)

    return plot(
        fig, output_type='div',
        auto_open=False, image_filename='comparison_plot',
    )

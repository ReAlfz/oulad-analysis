import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def student_info(data):
    module_data = data.groupby('code_module') \
        .agg({'id_student': 'count'}) \
        .reset_index() \
        .rename(columns={'code_module': 'Module', 'id_student': 'Quantity'})

    module_data['Percentage'] = module_data.apply(
        lambda x: round(100 * (x['Quantity'] / module_data['Quantity'].sum()), 2),
        axis=1
    )

    result_module = data.groupby(['code_module', 'final_result']) \
        .agg({'id_student': 'count'}) \
        .reset_index() \
        .rename(columns={'code_module': 'Module', 'id_student': 'Quantity', 'final_result': 'Result'})

    result_module['Percentage'] = result_module.apply(
        lambda x: round(
            100 * (x['Quantity'] / result_module[result_module['Result'] == x['Result']]['Quantity'].sum()), 2
        ),
        axis=1
    )

    print(f'Module:\n{module_data}\n\nresult percentage:\n{result_module}\n\n')

    course_data = data.groupby('code_presentation') \
        .agg({'id_student': 'count'}) \
        .reset_index() \
        .rename(columns={'code_presentation': 'Period', 'id_student': 'Quantity'})

    course_data['Percentage'] = course_data.apply(
        lambda x: round(100 * (x['Quantity'] / course_data['Quantity'].sum()), 2),
        axis=1
    )

    result_course = data.groupby(['code_presentation', 'final_result']) \
        .agg({'id_student': 'count'}) \
        .reset_index() \
        .rename(columns={'code_presentation': 'Period', 'id_student': 'Quantity', 'final_result': 'Result'})

    result_course['Percentage'] = result_course.apply(
        lambda x: round(
            100 * (x['Quantity'] / result_course[result_course['Result'] == x['Result']]['Quantity'].sum()), 2
        ),
        axis=1
    )

    print(f'Period:\n{course_data}\n\nresult percentage:\n{result_course}\n\n')

    return module_data, result_module, course_data, result_course


def visualization1(module_data, result_module):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Module Distribution', 'Result Distribution'))
    colors_scale = {
        'AAA': 'blue',
        'BBB': 'orange',
        'CCC': 'green',
        'DDD': 'red',
        'EEE': 'purple',
        'FFF': 'brown',
        'GGG': 'yellow',
    }

    fig.add_trace(
        go.Bar(
            x=module_data['Module'],
            y=module_data['Quantity'],
            text=module_data['Percentage'],
            hoverinfo='x+y+text',
            marker=dict(color=[colors_scale[color] for color in module_data['Module']]),
            textposition='auto'
        ), row=1, col=1)

    fig.add_trace(
        go.Bar(
            x=result_module['Result'],
            y=result_module['Percentage'],
            text=result_module['Percentage'],
            hoverinfo='x+y+text',
            marker=dict(color=[colors_scale[color] for color in result_module['Module']]),
            textposition='auto'
        ), row=1, col=2
    )

    fig.update_xaxes(title_text="Taken Module", row=1, col=1)
    fig.update_yaxes(title_text="Quantity [Students]", row=1, col=1)

    fig.update_xaxes(title_text="Result", row=1, col=2)
    fig.update_yaxes(title_text="Quantity [Students]", row=1, col=2)

    fig.update_annotations(
        {'text': 'Distribution - Taken Module', 'x': 0.5, 'xref': 'paper', 'y': 1.05, 'yref': 'paper'},
        selector=dict(row=1, col=1))
    fig.update_annotations({'text': 'Distribution - Result', 'x': 0.5, 'xref': 'paper', 'y': 1.05, 'yref': 'paper'},
                           selector=dict(row=1, col=2))
    fig.update_traces(barmode='stack', selector=dict(row=1, col=2))

    fig.show()


def visualization2(course_data, result_course):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Period Distribution', 'Result Distribution'))

    colors_scale = {
        '2013B': 'blue',
        '2013J': 'orange',
        '2014B': 'green',
        '2014J': 'red',
    }

    fig.add_trace(
        go.Bar(
            x=course_data['Period'],
            y=course_data['Quantity'],
            text=course_data['Percentage'],
            hoverinfo='x+y+text',
            marker=dict(color=[colors_scale[color] for color in course_data['Period']]),
            textposition='auto'
        ), row=1, col=1)

    fig.add_trace(
        go.Bar(
            x=result_course['Result'],
            y=result_course['Percentage'],
            text=result_course['Percentage'],
            hoverinfo='x+y+text',
            marker=dict(color=[colors_scale[color] for color in result_course['Period']]),
            textposition='auto'
        ), row=1, col=2
    )

    fig.update_xaxes(title_text="Taken Period", row=1, col=1)
    fig.update_yaxes(title_text="Quantity [Students]", row=1, col=1)

    fig.update_xaxes(title_text="Result", row=1, col=2)
    fig.update_yaxes(title_text="Quantity [Students]", row=1, col=2)

    fig.update_annotations(
        {'text': 'Distribution - Taken Period', 'x': 0.5, 'xref': 'paper', 'y': 1.05, 'yref': 'paper'},
        selector=dict(row=1, col=1))
    fig.update_annotations({'text': 'Distribution - Result', 'x': 0.5, 'xref': 'paper', 'y': 1.05, 'yref': 'paper'},
                           selector=dict(row=1, col=2))
    fig.update_traces(barmode='stack', selector=dict(row=1, col=2))

    fig.show()


if __name__ == '__main__':
    _student_info = pd.read_csv('studentInfo.csv')
    _assessment = pd.read_csv('assessments.csv')
    _course = pd.read_csv('courses.csv')
    _student_assessment = pd.read_csv('studentAssessment.csv')
    _student_registration = pd.read_csv('studentRegistration.csv')
    _student_vle = pd.read_csv('studentVle.csv')
    _vle = pd.read_csv('vle.csv')

    module_datas, result_modules, course_datas, result_courses = student_info(_student_info)
    # visualization1(module_data=module_datas, result_module=result_modules)
    visualization2(course_data=course_datas, result_course=result_courses)


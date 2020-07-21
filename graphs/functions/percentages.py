import math


def calculate_coordinates(valid_dict: list) -> list:
    """ Calculate the coordinates using trigonometry

    This takes a list of dictionaries of the format
    `[{'testuser':[6, 4, 3, 10, 5]}, {'testuser2':[1, 5, 17, 20, 6]}]` and
    then returns a list of coordinates. These coordinates can be used to
    represent an irregular polygon whose area
    can be calculated using shoelace method.

    :param valid_dict: List of dictionaries having key-value of
    `{username:[score_list]}`

    :type valid_dict: list

    :returns: A list of coordinates `[(2, 0.00), (1, 3.34)]`
    :rtype: list """

    score_list = []
    for dictionary in valid_dict:
        score_list.append([dictionary['score'][subclass]
                           for subclass in dictionary['score']])
    theta = (2*math.pi)/len(score_list[0])

    coordinate_list = []
    for score in score_list:
        coordinates = []
        for index, coordinate in enumerate(score):
            angle = (theta/(2*math.pi))*index
            slope = math.tan(angle)
            coordinates.append((coordinate, coordinate*slope))
        coordinate_list.append(coordinates)

    return coordinate_list


def find_determinant(matrix: list) -> float:
    """ Find the determinant of a 2*2 matrix

    Only 2*2 matrices are supported. Anything else will raise a TypeError """
    if len(matrix) == 2:
        return (matrix[0][0]*matrix[1][1])-(matrix[0][1]*matrix[1][0])
    else:
        raise TypeError("Only 2*2 matrices are supported")


def find_summation(matrix: list) -> float:
    """ Find the area of an irregular polygon

    This function uses the shoelace method to find the area of an irregular
    polygon (pentagon in this case). """

    matrix.append(matrix[0])
    determinants = []
    for index, coordinate in enumerate(matrix, 1):
        sub_matrix = []
        sub_matrix.append(coordinate)
        try:
            sub_matrix.append(matrix[index])
        except IndexError:
            sub_matrix.append(matrix[0])
        determinants.append(find_determinant(sub_matrix))
    return abs(sum(determinants))*0.5


def calculate_areas(valid_dict: list) -> list:
    """ A function that takes a list of dictionaries and returns the area of
     the graphs that these dictionaries would generate.

    This function acts as a wrapper for all the above functions and returns
    the required area """

    matrices = calculate_coordinates(valid_dict)
    for matrix, dictionary in zip(matrices, valid_dict):
        dictionary.update({
            'area': find_summation(matrix)
        })
    return valid_dict


def calculate_percentages(valid_dict: dict) -> list:
    """ Calculate the percentage difference from [0]'s score area """

    for d in valid_dict:
        if d['master'] is True:
            focus = d['area']
    for dictionary in valid_dict:
        avg = (focus+dictionary['area'])/2
        dictionary.update({
            'percentage': round(abs((dictionary['area']-avg)/avg)*100, 2)
        })
        dictionary.pop('area')
        dictionary.pop('score')

    return valid_dict

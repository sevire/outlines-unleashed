"""
Functionality to transform a data object extracted from an outline to powerpoint files (or specific slides)
"""

def create_power_point_skeleton():
    """
    Takes the output of a data node transformation (a table) with a specific structure and uses it to
    generate a PowerPoint file with associated slides.

    The idea is to be able to create a skeleton presentation quickly.  The use case is professionals
    who use PPT as a status reporting tool (for example) who create a lot of presentations which aren't
    sophisticated but just structure notes into a slide form.

    Can also be used as the first iteration of a more sophisticated presentation.
    :return:
    """
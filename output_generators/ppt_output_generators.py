"""
Functionality to transform a data object extracted from an outline to powerpoint files (or specific slides)
"""
from pptx import Presentation
import collections

powerpoint_field_names = ('section_name', 'slide_name', 'bullet')


class PowerPointGenerator:
    @staticmethod
    def _add_section_slide(presentation, title_text, sub_title_text):
        """
        :param presentation:
        :param title_text:
        :param sub_title_text:
        :return:
        """
        title_slide_layout = presentation.slide_layouts[0]
        slide = presentation.slides.add_slide(title_slide_layout)

        for shape in slide.placeholders:
            print('%d %s' % (shape.placeholder_format.idx, shape.name))

        title = slide.shapes.title
        subtitle = slide.placeholders[10]

        title.text = title_text
        subtitle.text = sub_title_text

    @staticmethod
    def _add_content_slide(presentation, title_text):
        bullet_slide_layout = presentation.slide_layouts[1]

        slide = presentation.slides.add_slide(bullet_slide_layout)

        for shape in slide.placeholders:
            print('%d %s' % (shape.placeholder_format.idx, shape.name))

        shapes = slide.shapes

        title_shape = shapes.title
        title_shape.text = title_text

        body_shape = shapes.placeholders[10]
        text_frame = body_shape.text_frame

        return text_frame

    @staticmethod
    def _add_slide_bullet(text_frame, bullet_text):
        """
        Adds a slide of bullets to the presentation.

        :param text_frame:
        :param bullet_text:
        :return:
        """

        paragraph = text_frame.add_paragraph()
        paragraph.text = bullet_text
        paragraph.level = 0

    def create_power_point_skeleton(self, data_node_table, template_ppt_path, output_ppt_path):
        """
        Takes the output of a data node transformation (a table) with a specific structure and uses it to
        generate a PowerPoint file with associated slides.

        The idea is to be able to create a skeleton presentation quickly.  The use case is professionals
        who use PPT as a status reporting tool (for example) who create a lot of presentations which aren't
        sophisticated but just structured notes into a slide form.

        Can also be used as the first iteration of a more sophisticated presentation.
        :return:
        """
        # Check that field names are correct for a powerpoint slide deck.
        field_list = data_node_table[0]
        for field in powerpoint_field_names:
            if field not in field_list:
                raise KeyError(f'Wrong data node format to drive PPT (field_name: {field})')

        prs = Presentation(template_ppt_path)

        section = ""
        slide = ""
        text_frame = None  # Should be set before referenced as first row will always invoke a new slide

        for row in data_node_table:
            if row['section_name'] != section:
                # Section has changed so add section slide
                section = row['section_name']
                self._add_section_slide(prs, section, "")
            if row['slide_name'] != slide:
                slide = row['section_name']
                text_frame = self._add_content_slide(prs, slide)
            self._add_slide_bullet(text_frame, row['bullet'])

        prs.save(output_ppt_path)

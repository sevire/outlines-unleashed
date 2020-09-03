from output_generators.ppt_output_generators import PowerPointGenerator


class PptOutputGeneratorGeneric:
    @staticmethod
    def generate_ppt(driver_table, output_path, template_ppt=None):
        """
        Method which will be overridden by each example of the PPT generator.

        Each implementation will either take a different driver file format or create a different output
        file format (or more likely both).

        :param driver_table: Table (typically from an outline data node) which represents the structure of the
                             required slide deck
        :param output_path: Path of .pptx file to create.
        :param template_ppt: Template file to use.  Must conform to standard .pptx structure for slide types
                             and placeholders, or elements will be incorrectly placed.
        :return:
        """

    @staticmethod
    def _add_title_slide(presentation, deck_title="(un-specified)", deck_sub_title="(un-specified)"):
        """
        Add the overall title slide for a slide deck

        There are potentially two fields to add; Title and Sub-title.

        :param deck_title:
        :param deck_sub_title:
        :return:
        """
        title_slide_layout_index = PowerPointGenerator._get_layout_index('deck_title')
        title_slide_layout = presentation.slide_layouts[title_slide_layout_index]
        slide = presentation.slides.add_slide(title_slide_layout)
        # PowerPointGenerator._print_placeholders_in_slide(slide)

        if deck_title is not None:
            title_placeholder_key = PowerPointGenerator._get_placeholder_index('deck_title', 'deck_title')
            title_placeholder = slide.placeholders[title_slide_layout_index]
            title_placeholder.text = deck_title

        if deck_sub_title is not None:
            subtitle_placeholder_key = PowerPointGenerator._get_placeholder_index('deck_title', 'deck_subtitle')
            subtitle_placeholder = slide.placeholders[subtitle_placeholder_key]
            subtitle_placeholder.text = deck_sub_title

    @staticmethod
    def _add_section_slide(presentation, section_title_text=None, section_sub_title_text=None):
        """
        :param presentation:
        :param section_title_text:
        :param section_sub_title_text:
        :return:
        """
        section_title_slide_layout_index = PowerPointGenerator._get_layout_index('section_header')
        section_title_slide_layout = presentation.slide_layouts[section_title_slide_layout_index]
        slide = presentation.slides.add_slide(section_title_slide_layout)
        # PowerPointGenerator._print_placeholders_in_slide(slide)

        if section_title_text is not None:
            section_title_placeholder_key = PowerPointGenerator._get_placeholder_index('section_header', 'section_header')
            section_title = slide.shapes.placeholders[section_title_placeholder_key]
            section_title.text = section_title_text

        if section_sub_title_text is not None:
            section_subtitle_placeholder_key = PowerPointGenerator._get_placeholder_index('section_header', 'section_header_text')
            section_subtitle = slide.shapes.placeholders[section_subtitle_placeholder_key]
            section_subtitle.text = section_sub_title_text

    @staticmethod
    def _add_content_slide(presentation, title_text=None):
        if title_text is None:
            title_text = ""
        bullet_slide_layout_index = PowerPointGenerator._get_layout_index('content')
        bullet_slide_layout = presentation.slide_layouts[bullet_slide_layout_index]

        slide = presentation.slides.add_slide(bullet_slide_layout)
        # PowerPointGenerator._print_placeholders_in_slide(slide)

        shapes = slide.shapes

        title_placeholder_key = PowerPointGenerator._get_placeholder_index('content', 'content_title')
        title_shape = shapes.placeholders[title_placeholder_key]
        title_shape.text = title_text

        body_shape_key = PowerPointGenerator._get_placeholder_index('content', 'content_bullets')
        body_shape = shapes.placeholders[body_shape_key]
        text_frame = body_shape.text_frame

        return text_frame

    @staticmethod
    def _add_slide_bullet(text_frame, bullet_text, bullet_level, first_bullet=False):
        """
        Adds a slide of bullets to the presentation.

        :param text_frame:
        :param bullet_text:
        :param bullet_level:
        :param first_bullet: If the first bullet is being added, we don't need to add a paragraph as one would have
                             been created when the slide was created.
        :return:
        """

        if first_bullet is True:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()
        paragraph.text = bullet_text
        paragraph.level = bullet_level

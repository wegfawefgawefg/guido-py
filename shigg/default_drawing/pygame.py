################ DEFAULT PYGAME DRAWING ################
import glm
import pygame


def draw_button(surface, button, resolution):
    absolute_position = resolution * button.position
    absolute_dimensions = resolution * button.scale

    ap = absolute_position
    ad = absolute_dimensions
    min_dim = min(ad.x, ad.y)
    offset = glm.vec2(1, 1)

    if not button.pressed:
        if not button.hovered:
            # shadow
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (ap.to_tuple(), (ad + offset).to_tuple()),
            )

            # highlight
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (ap.to_tuple(), (ad).to_tuple()),
            )

            # button
            pygame.draw.rect(
                surface,
                button.color,
                ((ap + offset).to_tuple(), (ad - offset).to_tuple()),
            )
        else:  # button hovered
            # shadow
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (ap.to_tuple(), (ad + offset).to_tuple()),
            )

            # highlight
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (ap.to_tuple(), (ad).to_tuple()),
            )

            # button
            pygame.draw.rect(
                surface,
                (
                    button.color[0] * 0.65,
                    button.color[1] * 0.65,
                    button.color[2] * 0.65,
                ),
                ((ap + offset).to_tuple(), (ad - offset).to_tuple()),
            )
    elif button.pressed:
        # under shadow
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (ap.to_tuple(), (ad + offset).to_tuple()),
        )

        # under highlight
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (ap.to_tuple(), (ad).to_tuple()),
        )

        # button
        pygame.draw.rect(
            surface,
            (
                button.color[0] * 0.65,
                button.color[1] * 0.65,
                button.color[2] * 0.65,
            ),
            ((ap + offset).to_tuple(), (ad - offset).to_tuple()),
        )

    if button.image:
        # scale the image to fit the button
        # scale both dimensions by the same amount, but scale the larger dimension to fit the button
        image_dimensions = glm.vec2(button.image.get_width(), button.image.get_height())
        larger_dimension = max(image_dimensions.x, image_dimensions.y)
        scale_factor = (ad * 0.9) / larger_dimension
        scaled_dimensions = image_dimensions * scale_factor
        centered_offset = scaled_dimensions * 0.05

        image_position = offset + ap + ad / 2 - scaled_dimensions / 2

        # draw the image
        if not button.pressed:
            surface.blit(
                pygame.transform.scale(
                    button.image,
                    (int(scaled_dimensions.x), int(scaled_dimensions.y)),
                ),
                image_position.to_tuple(),
            )
        else:
            image_position = glm.vec2(
                image_position.x,
                image_position.y + centered_offset.y,
            )
            surface.blit(
                pygame.transform.scale(
                    button.image,
                    (int(scaled_dimensions.x), int(scaled_dimensions.y)),
                ),
                image_position.to_tuple(),
            )

    elif button.label:
        font_offset = 0

        font = pygame.font.SysFont("Arial", 24)
        text = font.render(button.label, True, (0, 0, 0))
        text_position = (
            ap.x + ad.x / 2 - text.get_width() / 2,
            ap.y + ad.y / 2 - text.get_height() / 2,
        )

        if button.pressed:
            # offset text_position down by offset.y
            text_position = (
                text_position[0],
                text_position[1] + offset.y,
            )

        surface.blit(
            text,
            text_position,
        )


def draw_slider(surface, slider, resolution):
    absolute_position = resolution * slider.position
    absolute_dimensions = resolution * slider.scale

    ap = absolute_position
    ad = absolute_dimensions
    offset = glm.vec2(1, 1)

    # draw body
    pygame.draw.rect(
        surface,
        (100, 100, 100),
        (ap.to_tuple(), (ad).to_tuple()),
    )

    # draw body
    value_fraction = (slider.value - slider.minimum) / (
        slider.maximum - slider.minimum
    )  # range [0.0 , 1.0]
    rel_position_x = value_fraction * slider.scale.x  # [0.0, slider_rel_width]
    absolute_thumb_x = absolute_position.x + rel_position_x * resolution.x

    absolute_thumb_width = resolution.x * slider.thumb_width
    half_thumb_width = absolute_thumb_width / 2.0

    thumb_position = glm.vec2(absolute_thumb_x - half_thumb_width, absolute_position.y)
    absolute_thumb_dimensions = glm.vec2(absolute_thumb_width, absolute_dimensions.y)

    tp = thumb_position
    td = absolute_thumb_dimensions
    offset = glm.vec2(1, 1)

    # shadow
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        (tp.to_tuple(), (td + offset).to_tuple()),
    )

    # highlight
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (tp.to_tuple(), (td).to_tuple()),
    )

    # slider center
    pygame.draw.rect(
        surface,
        slider.color,
        ((tp + offset).to_tuple(), (td - offset).to_tuple()),
    )


def draw_vertical_slider(surface, slider, resolution):
    absolute_position = resolution * slider.position
    absolute_dimensions = resolution * slider.scale

    ap = absolute_position
    ad = absolute_dimensions
    offset = glm.vec2(1, 1)

    # draw body
    pygame.draw.rect(
        surface,
        (100, 100, 100),
        (ap.to_tuple(), ad.to_tuple()),
    )

    # calculate value fraction for the vertical slider
    value_fraction = (slider.value - slider.minimum) / (slider.maximum - slider.minimum)
    rel_position_y = value_fraction * slider.scale.y  # for vertical slider
    absolute_thumb_y = absolute_position.y + rel_position_y * resolution.y

    absolute_thumb_height = resolution.y * slider.thumb_height
    half_thumb_height = absolute_thumb_height / 2.0

    thumb_position = glm.vec2(absolute_position.x, absolute_thumb_y - half_thumb_height)
    absolute_thumb_dimensions = glm.vec2(absolute_dimensions.x, absolute_thumb_height)

    tp = thumb_position
    td = absolute_thumb_dimensions
    offset = glm.vec2(1, 1)

    # shadow
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        (tp.to_tuple(), (td + offset).to_tuple()),
    )

    # highlight
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (tp.to_tuple(), td.to_tuple()),
    )

    # slider center
    pygame.draw.rect(
        surface,
        slider.color,
        ((tp + offset).to_tuple(), (td - offset).to_tuple()),
    )


def draw_draggable(surface, draggable, resolution):
    absolute_position = resolution * draggable.position
    absolute_dimensions = resolution * draggable.scale

    ap = absolute_position
    ad = absolute_dimensions
    min_dim = min(ad.x, ad.y)
    offset = glm.vec2(1, 1)

    if not draggable.hovered:
        # shadow
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (ap.to_tuple(), (ad + offset).to_tuple()),
        )

        # highlight
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (ap.to_tuple(), (ad).to_tuple()),
        )

        # draggable
        pygame.draw.rect(
            surface,
            draggable.color,
            ((ap + offset).to_tuple(), (ad - offset).to_tuple()),
        )

        # draw 2 lines to indicate the draggable is grabbable
        # draw one line 30% from the top, and one 30% from the bottom
        line_start_x = ad.x * 0.3 + ap.x
        line_end_x = ad.x * 0.7 + ap.x

        upper_line_height = ad.y * 0.3 + ap.y
        lower_line_height = ad.y * 0.7 + ap.y

        line_thickness = 2

        color_mod = 0.3
        line_color = [ce * color_mod for ce in draggable.color]
        pygame.draw.line(
            surface,
            line_color,
            (line_start_x, upper_line_height),
            (line_end_x, upper_line_height),
            line_thickness,
        )
        pygame.draw.line(
            surface,
            line_color,
            (line_start_x, lower_line_height),
            (line_end_x, lower_line_height),
            line_thickness,
        )

    else:  # draggable hovered
        # shadow
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (ap.to_tuple(), (ad + offset).to_tuple()),
        )

        # highlight
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (ap.to_tuple(), (ad).to_tuple()),
        )

        # button
        pygame.draw.rect(
            surface,
            (
                draggable.color[0] * 0.65,
                draggable.color[1] * 0.65,
                draggable.color[2] * 0.65,
            ),
            ((ap + offset).to_tuple(), (ad - offset).to_tuple()),
        )

    if draggable.image:
        # scale the image to fit the button
        # scale both dimensions by the same amount, but scale the larger dimension to fit the button
        image_dimensions = glm.vec2(
            draggable.image.get_width(), draggable.image.get_height()
        )
        larger_dimension = max(image_dimensions.x, image_dimensions.y)
        scale_factor = (ad * 0.9) / larger_dimension
        scaled_dimensions = image_dimensions * scale_factor
        centered_offset = scaled_dimensions * 0.05

        image_position = offset + ap + ad / 2 - scaled_dimensions / 2

        # draw the image
        surface.blit(
            pygame.transform.scale(
                draggable.image,
                (int(scaled_dimensions.x), int(scaled_dimensions.y)),
            ),
            image_position.to_tuple(),
        )

    elif draggable.label:
        font_offset = 0

        font = pygame.font.SysFont("Arial", 24)
        text = font.render(draggable.label, True, (0, 0, 0))
        text_position = (
            ap.x + ad.x / 2 - text.get_width() / 2,
            ap.y + ad.y / 2 - text.get_height() / 2,
        )

        surface.blit(
            text,
            text_position,
        )


def draw_move_and_resize_thumbs(surface, move_and_resize_thumbs, resolution):
    draw_draggable(surface, move_and_resize_thumbs.move_thumb, resolution)
    draw_draggable(surface, move_and_resize_thumbs.resize_thumb, resolution)


def draw_left_right_selector(surface, left_right_selector, resolution):
    draw_button(surface, left_right_selector.left_button, resolution)
    draw_button(surface, left_right_selector.right_button, resolution)

    font = pygame.font.SysFont("Arial", 24)
    text = font.render(left_right_selector.selected_option, True, (0, 0, 0))

    ap = resolution * left_right_selector.position
    ad = resolution * left_right_selector.scale

    text_position = (
        ap.x + ad.x / 2 - text.get_width() / 2,
        ap.y + ad.y / 2 - text.get_height() / 2,
    )

    surface.blit(
        text,
        text_position,
    )

    surface.blit(
        text,
        text_position,
    )


def draw_button_toggle(surface, button_toggle, resolution):
    draw_button(surface, button_toggle.left_button, resolution)
    draw_button(surface, button_toggle.right_button, resolution)

    # figure out which one is selected
    if button_toggle.toggled_option == button_toggle.left_option:
        left_button_position = resolution * button_toggle.left_button.position
        left_button_scale = resolution * button_toggle.left_button.scale
        # draw a big green circle in the button
        smaller_dimension = min(left_button_scale.x, left_button_scale.y)
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (
                int(left_button_position.x + left_button_scale.x / 2),
                int(left_button_position.y + left_button_scale.y / 2),
            ),
            int(smaller_dimension / 2.0),
            4,
        )

    elif button_toggle.toggled_option == button_toggle.right_option:
        right_button_position = resolution * button_toggle.right_button.position
        right_button_scale = resolution * button_toggle.right_button.scale
        # draw a big circle in the button
        smaller_dimension = min(right_button_scale.x, right_button_scale.y)
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (
                int(right_button_position.x + right_button_scale.x / 2),
                int(right_button_position.y + right_button_scale.y / 2),
            ),
            int(smaller_dimension / 2.0),
            4,
        )


def draw_label(surface, label, resolution):
    """label is a non interactable, static thing."""
    ap = resolution * label.position
    ad = resolution * label.scale
    ad.x = max(ad.x, 0.0)
    ad.y = max(ad.y, 0.0)

    # draw body
    """ if label has a texture, draw that, else draw a rectangle."""
    if not label.no_background:
        if label.background_texture:
            surface.blit(
                pygame.transform.scale(
                    label.background_texture,
                    (int(ad.x), int(ad.y)),
                ),
                ap.to_tuple(),
            )
        else:
            pygame.draw.rect(
                surface,
                label.color,
                (ap.to_tuple(), (ad).to_tuple()),
            )

    # draw image or text
    if label.image:
        # scale the image to fit the button
        # scale both dimensions by the same amount, but scale the larger dimension to fit the button
        image_dimensions = glm.vec2(label.image.get_width(), label.image.get_height())
        larger_dimension = max(image_dimensions.x, image_dimensions.y)
        scale_factor = (ad * 0.9) / larger_dimension
        scaled_dimensions = image_dimensions * scale_factor
        centered_offset = scaled_dimensions * 0.05

        image_position = ap + ad / 2 - scaled_dimensions / 2

        # draw the image
        surface.blit(
            pygame.transform.scale(
                label.image,
                (int(scaled_dimensions.x), int(scaled_dimensions.y)),
            ),
            image_position.to_tuple(),
        )
    elif label.text:
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(label.text, True, label.text_color)
        text_position = (
            ap.x + ad.x / 2 - text.get_width() / 2,
            ap.y + ad.y / 2 - text.get_height() / 2,
        )

        surface.blit(
            text,
            text_position,
        )

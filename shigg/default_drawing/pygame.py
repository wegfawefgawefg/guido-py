################ DEFAULT PYGAME DRAWING ################
import glm
import pygame


def draw_button(surface, button, resolution):
    absolute_position = resolution * button.position
    absolute_dimensions = resolution * button.scale

    ap = absolute_position
    ad = absolute_dimensions
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

        font = pygame.font.SysFont("Arial", 16)
        text = font.render(button.label, False, (0, 0, 0))
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

from magnumapi.geometry.blocks.CosThetaBlock import CosThetaBlock
from magnumapi.geometry.primitives.Area import Area
from magnumapi.geometry.primitives.Line import Line


class GeometryCheck:
    @staticmethod
    def is_outside_of_first_quadrant(geometry, eps=1e-30) -> True:
        """ Method checking whether a geometry is fully positioned in the first quadrant.

        :param eps: a machine precision for comparison of 0 value
        :return: True if an Area instance is in the first quadrant, False otherwise
        """
        for layer_def in geometry.layer_defs:
            for block_index in layer_def.blocks:
                if geometry.blocks[block_index - 1].is_outside_of_first_quadrant(eps=eps):
                    return True

        return False

    @staticmethod
    def are_turns_overlapping(geometry) -> bool:
        """Method checking whether turns from neighbouring blocks are overlapping.

        :return: True, if at least two neighbouring turns are overlapping, otherwise False
        """
        for layer_def in geometry.layer_defs:
            for block_index in layer_def.blocks[1:]:
                area_prev = geometry.blocks[block_index - 2].areas[-1]
                area_curr = geometry.blocks[block_index - 1].areas[0]

                if Area.are_areas_overlapping(area_prev, area_curr):
                    return True

        return False

    @classmethod
    def is_wedge_tip_too_sharp(cls, geometry, min_value_in_mm: float) -> bool:
        """ Method checking whether wedge tip is too sharp. Method computes the wedge tip arc length, by finding an
        intersection of two neighbouring turns with an inner radius

        :param min_value_in_mm: minimum value of  the wedge tip arc
        :return: True if wedge length is below the minimum value
        """
        for layer_def in geometry.layer_defs:
            for block_index in layer_def.blocks[1:]:
                block_curr = geometry.blocks[block_index - 1]
                block_prev = geometry.blocks[block_index - 2]
                if isinstance(block_curr, CosThetaBlock) and isinstance(block_prev, CosThetaBlock):
                    if cls.is_wedge_arc_of_two_blocks_too_short(block_curr, block_prev, min_value_in_mm):
                        return True

        return False

    @staticmethod
    def is_wedge_arc_of_two_blocks_too_short(block_curr: "CosThetaBlock",
                                             block_prev: "CosThetaBlock",
                                             min_value_in_mm: float) -> bool:
        """ Static method calculating a wedge arc length between two neighbouring blocks of a given layer

        :param block_curr: current block
        :param block_prev: previous block
        :param min_value_in_mm: minimum arc length in millimeters
        :return: True if the wedge arc length is too short, otherwise False
        """
        area_curr = block_curr.areas[0]
        area_prev = block_prev.areas[-1]

        line_first_area = area_curr.get_line(0)
        line_last_area = area_prev.get_line(2)

        radius = block_curr.block_def.radius
        l_arc = Line.calc_arc_length_between_two_lines(radius, line_last_area, line_first_area)

        return l_arc < min_value_in_mm

import math
import numpy as np


class HoughCluster:
    """Clasterize and merge each cluster of cv2.HoughLinesP() output

    This was taken from https://stackoverflow.com/questions/45531074/how-to-merge-lines-after-houghlinesp
    and modified.

    >>> a = HoughCluster()
    >>> foo = a.process_lines(houghP_lines, binary_image)
    """

    def get_orientation(self, line):
        # Get orientation of a line, using its length https://en.wikipedia.org/wiki/Atan2
        # orientation = math.atan2(abs((line[0] - line[2])), abs((line[1] - line[3])))
        orientation = math.atan2((line[0] - line[2]), (line[1] - line[3]))
        return math.degrees(orientation)

    def checker(self, line_new, groups, min_distance_to_merge, min_angle_to_merge):
        # Check if line have enough distance and angle to be count as similar
        for group in groups:
            # walk through existing line groups
            for line_old in group:
                # check distance
                if self.get_distance(line_old, line_new) < min_distance_to_merge:
                    # check the angle between lines
                    orientation_new = self.get_orientation(line_new)
                    orientation_old = self.get_orientation(line_old)
                    # if all is ok -- line is similar to others in group
                    if abs(orientation_new - orientation_old) < min_angle_to_merge:
                        group.append(line_new)
                        return False
        # if it is totally different line
        return True

    def distance_to_line(self, point, line):
        """Get distance between point and line
        https://stackoverflow.com/questions/40970478/python-3-5-2-distance-from-a-point-to-a-line
        """
        px, py = point
        x1, y1, x2, y2 = line
        x_diff = x2 - x1
        y_diff = y2 - y1
        num = abs(y_diff * px - x_diff * py + x2 * y1 - y2 * x1)
        den = math.sqrt(y_diff ** 2 + x_diff ** 2)
        return num / den


    def get_distance(self, a_line, b_line):
        """Get all possible distances between each dot of two lines and second line
        return the shortest
        """
        dist1 = self.distance_to_line(a_line[:2], b_line)
        dist2 = self.distance_to_line(a_line[2:], b_line)
        dist3 = self.distance_to_line(b_line[:2], a_line)
        dist4 = self.distance_to_line(b_line[2:], a_line)

        return min(dist1, dist2, dist3, dist4)


    def merge_lines_pipeline_2(self, lines):
        #Clusterize (group) lines
        groups = []  # all lines groups are here
        # Parameters to play with
        min_distance_to_merge = 30
        min_angle_to_merge = 10
        # first line will create new group every time
        groups.append([lines[0]])
        # if line is different from existing gropus, create a new group
        for line_new in lines[1:]:
            if self.checker(line_new, groups, min_distance_to_merge, min_angle_to_merge):
                groups.append([line_new])

        return groups

    def merge_lines_segments1(self, lines):
        """Sort lines cluster and return first and last coordinates
        """
        orientation = self.get_orientation(lines[0])

        # special case
        if (len(lines) == 1):
            return [lines[0][:2], lines[0][2:]]

        # [[1,2,3,4],[]] to [[1,2],[3,4],[],[]]
        points = []
        for line in lines:
            points.append(line[:2])
            points.append(line[2:])
        # if vertical
        if 0 < orientation < 180:
            # sort by y
            points = sorted(points, key=lambda point: point[1])
        else:
            # sort by x
            points = sorted(points, key=lambda point: point[0])

        # return first and last point in sorted group
        # [[x,y],[x,y]]
        return [points[0], points[-1]]

    def process_lines(self, lines, img):
        """Main function for lines from cv.HoughLinesP() output merging.
        """
        lines_x = []
        lines_y = []
        # for every line of cv2.HoughLinesP()
        for line_i in [l[0] for l in lines]:
            orientation = self.get_orientation(line_i)
            # if vertical

            if 0 < orientation < 180:
                lines_y.append(line_i)
            else:
                lines_x.append(line_i)

        lines_y = sorted(lines_y, key=lambda line: line[1])
        lines_x = sorted(lines_x, key=lambda line: line[0])
        merged_lines_all = []

        # for each cluster in vertical and horizantal lines leave only one line
        for i in [lines_x, lines_y]:
            if len(i) > 0:
                groups = self.merge_lines_pipeline_2(i)
                merged_lines = []
                for group in groups:
                    merged_lines.append(self.merge_lines_segments1(group))

                merged_lines_all.extend(merged_lines)

        return np.array(merged_lines_all).reshape((-1, 4))




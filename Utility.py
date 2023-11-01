import wx
import math

def print_matrix_values(matrix : 'wx.AffineMatrix2D'):
        
        tupledMatrix = matrix.Get()
        print("Affine Matrix:")
        print("|" + str(tupledMatrix[0].m_11) + " " + str(tupledMatrix[0].m_12) + "|")
        print("|" + str(tupledMatrix[0].m_21) + " " + str(tupledMatrix[0].m_22) + "|")

def print_point(point : 'wx.Point2D'):
    print("Point: (" + str(point.x) + ", " + str(point.y) + ")")
    
# BOTH VECTORS MUST BE 2D VECTORS
def get_angle_between_vectors(vec1, vec2):
        
        # dot product
        dot_product = vec1.x * vec2.x + vec1.y * vec2.y        
        
        # cross product
        cross_product = vec1.x * vec2.y - vec1.y * vec2.x
        
        # theta equals arctan of dot product divided by the product of the magnitudes
        theta = math.atan(cross_product / dot_product)
        return theta


#     Writes data to a file.
#     :param filename: Name of the file to write to.
#     :param data: The data to write to the file.
#     :param mode: Mode in which to open the file ('a' for append and 'w' for truncate/write).
def write_to_file(filename: str, data: any, mode: str = 'w'):

    # If the mode provided isn't 'a' or 'w', raise an error
    if mode not in ['a', 'w']:
        raise ValueError("Mode must be either 'a' (append) or 'w' (truncate/write)")

    # If the data is binary or a bytearray, open the file in binary mode
    if isinstance(data, (bytes, bytearray)):
        mode += 'b'

    with open(filename, mode) as file:
        file.write(data)
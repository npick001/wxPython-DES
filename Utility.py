import wx

def print_matrix_values(matrix : 'wx.AffineMatrix2D'):
        
        tupledMatrix = matrix.Get()
        print("Affine Matrix:")
        print("|" + str(tupledMatrix[0].m_11) + " " + str(tupledMatrix[0].m_12) + "|")
        print("|" + str(tupledMatrix[0].m_21) + " " + str(tupledMatrix[0].m_22) + "|")

def print_point(point : 'wx.Point2D'):
    print("Point: (" + str(point.x) + ", " + str(point.y) + ")")
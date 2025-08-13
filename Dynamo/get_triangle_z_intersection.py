# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import XYZ
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

def get_triangle_z_intersection(v1, v2, v3, x, y):
    # Calculate barycentric coordinates for point (x, y) relative to triangle
    denom = (v2[1] - v3[1]) * (v1[0] - v3[0]) + (v3[0] - v2[0]) * (v1[1] - v3[1])

    if abs(denom) < 1e-10:  # Triangle is degenerate
        return None

    a = ((v2[1] - v3[1]) * (x - v3[0]) + (v3[0] - v2[0]) * (y - v3[1])) / denom
    b = ((v3[1] - v1[1]) * (x - v3[0]) + (v1[0] - v3[0]) * (y - v3[1])) / denom
    c = 1 - a - b

    # Check if point is inside triangle
    if a >= 0 and b >= 0 and c >= 0 and a <= 1 and b <= 1 and c <= 1:
        # Interpolate Z coordinate using barycentric coordinates
        z = a * v1[2] + b * v2[2] + c * v3[2]
        return z

    return None



# Place your code below this line
p1 = XYZ(-10,10,5)
p2 = XYZ.Zero
p3 = XYZ(20,15,2)

x = 0
y = 8
z = get_triangle_z_intersection(p1,p2,p3, x,y)

if z:
    OUT = map(lambda x:x.ToPoint(),[p1,p2,p3, XYZ(x,y,z)])

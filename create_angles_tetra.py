import numpy as np
import math
import sys
from io import StringIO


def vec_to_out(vector):
    str_out = ""
    for i in vector:
        str_out += str(i) + " "
    return str_out + "A"


def rotation_matrix(theta, axis=None):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    if axis is None:
        axis = [0, 0, 1]
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


def print_to_file(cont, end='\n'):
    sys.stdout = stand_std
    print(cont, end=end)
    global result
    result = StringIO()
    sys.stdout = result


def new_std():
    global result
    result = StringIO()
    sys.stdout = result


result = StringIO()
stand_std = sys.stdout
sys.stdout = result
d = 1
d2 = 0.5
o1_pos = [0, 0, d]
rot_1 = rotation_matrix(np.deg2rad(109.4712 / 2), axis=[1, 0, 0])
rot_2 = rotation_matrix(np.deg2rad(-109.4712 / 2), axis=[1, 0, 0])
rot_3 = rotation_matrix(np.deg2rad(180 - 109.4712 / 2), axis=[0, 1, 0])
rot_4 = rotation_matrix(np.deg2rad(-(180 - 109.4712 / 2)), axis=[0, 1, 0])


h1_pos = [0, d2 * np.sin(np.deg2rad(104.5 / 2)), d + d2 * np.cos(np.deg2rad(104.5 / 2))]
h2_pos = [0, - d2 * np.sin(np.deg2rad(104.5 / 2)), d + d2 * np.cos(np.deg2rad(104.5 / 2))]
rot_ax = [0, 0, 1]

print("ai")
print("li")
print("0 0 0 A")
print("*")
print("o")
print(vec_to_out(rot_1.dot(o1_pos)))
print(vec_to_out(rot_2.dot(o1_pos)))
print(vec_to_out(rot_3.dot(o1_pos)))
print(vec_to_out(rot_4.dot(o1_pos)))
print("*")
print("h")
standard_begin = result.getvalue()

for a1 in np.linspace(0, 2 * np.pi, 6, endpoint=False):
    new_std()
    h1_pos = rot_1.dot(rotation_matrix(a1, axis=rot_ax).dot(h1_pos))
    h2_pos = rot_1.dot(rotation_matrix(a1, axis=rot_ax).dot(h2_pos))
    print(vec_to_out(h1_pos))
    print(vec_to_out(h2_pos))
    h1_tex = result.getvalue()
    for a2 in np.linspace(0, 2 * np.pi, 6, endpoint=False):
        new_std()
        h3_pos = rot_2.dot(rotation_matrix(a2, axis=rot_ax).dot(h1_pos))
        h4_pos = rot_2.dot(rotation_matrix(a2, axis=rot_ax).dot(h2_pos))
        print(vec_to_out(h3_pos))
        print(vec_to_out(h4_pos))
        h2_tex = result.getvalue()
        for a3 in np.linspace(0, 2 * np.pi, 6, endpoint=False):
            new_std()
            h5_pos = rot_3.dot(rotation_matrix(a3, axis=rot_ax).dot(h1_pos))
            h6_pos = rot_3.dot(rotation_matrix(a3, axis=rot_ax).dot(h2_pos))
            print(vec_to_out(h5_pos))
            print(vec_to_out(h6_pos))
            h3_tex = result.getvalue()
            for a4 in np.linspace(0, 2 * np.pi, 6, endpoint=False):
                name = str(np.rad2deg(a1)) + "_" + str(np.rad2deg(a2)) + "_" + str(np.rad2deg(a3)) + "_" + str(np.rad2deg(a4))
                new_std()
                h7_pos = rot_4.dot(rotation_matrix(a4, axis=rot_ax).dot(h1_pos))
                h8_pos = rot_4.dot(rotation_matrix(a4, axis=rot_ax).dot(h2_pos))
                print(vec_to_out(h7_pos))
                print(vec_to_out(h8_pos))
                print("*")
                print("w $root$/" + name + ".coord")
                header = "[(li_h2o_4), (" + name + \
                         ")deg_variation\n"
                print_to_file(header + standard_begin + h1_tex + h2_tex + h3_tex + result.getvalue() +
                              "]", end="")


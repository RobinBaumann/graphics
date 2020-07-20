# Copyright 2020 The TensorFlow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf

from tensorflow_graphics.projects.mesh_rcnn.branches.voxel_branch import cubify
from tensorflow_graphics.util import test_case


class CufifyTest(test_case.TestCase):

  def test_all_below_threshold(self):
    N, V = 32, 16
    voxels = tf.random.uniform((N, V, V, V), minval=0, maxval=0.5,
                               dtype=tf.float32)
    vertices, faces = cubify(voxels, threshold=0.7)
    self.assertEmpty(vertices[0])
    self.assertEmpty(faces[0])

  def test_cubify_on_cube(self):
    N, V = 2, 2

    # top left corner in front plane is 1, everything else empty
    one_voxel = tf.constant([[[1., 0.],
                              [0., 0.]],
                             [[0., 0.],
                              [0., 0.]]],
                            dtype=tf.float32)
    full_cube = tf.ones((V, V, V), dtype=tf.float32)

    test_data = tf.stack([one_voxel, full_cube])

    vertices, faces = cubify(test_data, 0.5)

    # ~~~~~~~~~~ Test first batch element ~~~~~~~~~~ #
    expected_vertices_topleftnear = tf.constant(
        [
            [-1.0, -1.0, -1.0],
            [-1.0, -1.0, 1.0],
            [1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0],
            [1.0, 1.0, 1.0],
        ], dtype=tf.float32
    )

    expected_faces_topleftnear = tf.constant(
        [
            [0, 1, 4],
            [1, 5, 4],
            [4, 5, 6],
            [5, 7, 6],
            [0, 4, 6],
            [0, 6, 2],
            [0, 3, 1],
            [0, 2, 3],
            [6, 7, 3],
            [6, 3, 2],
            [1, 7, 5],
            [1, 3, 7],
        ], dtype=tf.float32
    )

    self.assertAllClose(expected_vertices_topleftnear, vertices[0])
    self.assertAllClose(expected_faces_topleftnear, faces[0])

    # ~~~~~~~~~~ Test second batch element ~~~~~~~~~~ #
    expected_vertices_full = tf.constant(
        [
            [-1.0, -1.0, -1.0],
            [-1.0, -1.0, 1.0],
            [-1.0, -1.0, 3.0],
            [1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0],
            [1.0, -1.0, 3.0],
            [3.0, -1.0, -1.0],
            [3.0, -1.0, 1.0],
            [3.0, -1.0, 3.0],
            [-1.0, 1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, 1.0, 3.0],
            [1.0, 1.0, -1.0],
            [1.0, 1.0, 3.0],
            [3.0, 1.0, -1.0],
            [3.0, 1.0, 1.0],
            [3.0, 1.0, 3.0],
            [-1.0, 3.0, -1.0],
            [-1.0, 3.0, 1.0],
            [-1.0, 3.0, 3.0],
            [1.0, 3.0, -1.0],
            [1.0, 3.0, 1.0],
            [1.0, 3.0, 3.0],
            [3.0, 3.0, -1.0],
            [3.0, 3.0, 1.0],
            [3.0, 3.0, 3.0],
        ], dtype=tf.float32
    )

    expected_faces_full = tf.constant(
        [
            [0, 1, 9],
            [1, 10, 9],
            [0, 9, 12],
            [0, 12, 3],
            [0, 4, 1],
            [0, 3, 4],
            [1, 2, 10],
            [2, 11, 10],
            [1, 5, 2],
            [1, 4, 5],
            [2, 13, 11],
            [2, 5, 13],
            [3, 12, 14],
            [3, 14, 6],
            [3, 7, 4],
            [3, 6, 7],
            [14, 15, 7],
            [14, 7, 6],
            [4, 8, 5],
            [4, 7, 8],
            [15, 16, 8],
            [15, 8, 7],
            [5, 16, 13],
            [5, 8, 16],
            [9, 10, 17],
            [10, 18, 17],
            [17, 18, 20],
            [18, 21, 20],
            [9, 17, 20],
            [9, 20, 12],
            [10, 11, 18],
            [11, 19, 18],
            [18, 19, 21],
            [19, 22, 21],
            [11, 22, 19],
            [11, 13, 22],
            [20, 21, 23],
            [21, 24, 23],
            [12, 20, 23],
            [12, 23, 14],
            [23, 24, 15],
            [23, 15, 14],
            [21, 22, 24],
            [22, 25, 24],
            [24, 25, 16],
            [24, 16, 15],
            [13, 25, 22],
            [13, 16, 25],
        ], dtype=tf.float32
    )

    self.assertAllClose(expected_vertices_full, vertices[1])
    self.assertAllClose(expected_faces_full, faces[1])
